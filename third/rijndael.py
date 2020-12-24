class Rijndael:
    def __init__(self, key, block_len):
        '''
        key_len = {4 / 6 / 8}
        block_len = {4 / 6 / 8}
        '''
        self.S = bytearray(256)
        self.INV_S = bytearray(256)
        self.R_CON = bytearray(32)
        self.gen_s()
        self.gen_inv_s()
        self.gen_r_con()

        self.Nb = block_len
        self.Nk = len(key) // 4
        self.Nr = self.r_count()

        if not self.Nb in [4, 6, 8]:
            raise ValueError('Incorrect block size')

        if not self.Nk in [4, 6, 8]:
            raise ValueError('Incorrect key size')

        self.w = self.key_expansion(key)

    def get_block_size(self):
        return self.Nb * 4

    def encode_block(self, block):
        state = self.to_state(block)
        self.add_round_key(state, self.w[:self.Nb])

        for i in range(1, self.Nr):
            self.sub_bytes(state)
            self.shift_rows(state)
            self.mix_columns(state)
            self.add_round_key(state, self.w[self.Nb * i: (self.Nb * (i + 1))])

        self.sub_bytes(state)
        self.shift_rows(state)
        self.add_round_key(state, self.w[self.Nb * self.Nr:])

        return self.to_block(state)

    def decode_block(self, block):
        state = self.to_state(block)
        self.add_round_key(state, self.w[self.Nb * self.Nr:])

        for i in range(self.Nr - 1, 0, -1):
            self.shift_rows(state, dec=True)
            self.sub_bytes(state, dec=True)
            self.add_round_key(state, self.w[(self.Nb * i): self.Nb * (i + 1)])
            self.mix_columns(state, dec=True)

        self.shift_rows(state, dec=True)
        self.sub_bytes(state, dec=True)
        self.add_round_key(state, self.w[:self.Nb])

        return self.to_block(state)

    def key_expansion(self, key):
        keys = [[] for i in range(self.Nb * (self.Nr + 1))]

        for i in range(self.Nk):
            keys[i] = [key[4 * i + j] for j in range(4)]

        for i in range(self.Nk, self.Nb * (self.Nr + 1)):
            word = keys[i - 1]
            if i % self.Nk == 0:
                temp = [self.S[x] for x in self.cycle_shift(word, -1)]
                temp[0] ^= self.R_CON[i // self.Nk]
            elif self.Nk > 6 and i % self.Nk == 4:
                temp = [self.S[x] for x in temp]
            keys[i] = [keys[i - self.Nk][j] ^ temp[j] for j in range(4)]

        return keys

    def sub_bytes(self, state, dec=False):
        for i in range(4):
            for j in range(self.Nb):
                if dec:
                    state[i][j] = self.INV_S[state[i][j]]
                else:
                    state[i][j] = self.S[state[i][j]]

    def shift_rows(self, state, dec=False):
        if dec:
            c = [-1, -2, -3]
        else:
            c = [1, 2, 3]

        for i in range(1, 4):
            state[i] = self.cycle_shift(state[i], c[i - 1])

    def mix_columns(self, state, dec=False):
        b = [0 for _ in range(4)]

        for i in range(self.Nb):
            if dec:
                b[0] = self.gmul(0x0E, state[0][i]) ^ self.gmul(0x0B, state[1][i]) ^ self.gmul(0x0D, state[2][i]) ^ self.gmul(0x09, state[3][i])
                b[1] = self.gmul(0x09, state[0][i]) ^ self.gmul(0x0E, state[1][i]) ^ self.gmul(0x0B, state[2][i]) ^ self.gmul(0x0D, state[3][i])
                b[2] = self.gmul(0x0D, state[0][i]) ^ self.gmul(0x09, state[1][i]) ^ self.gmul(0x0E, state[2][i]) ^ self.gmul(0x0B, state[3][i])
                b[3] = self.gmul(0x0B, state[0][i]) ^ self.gmul(0x0D, state[1][i]) ^ self.gmul(0x09, state[2][i]) ^ self.gmul(0x0E, state[3][i])
            else:
                b[0] = self.gmul(0x02, state[0][i]) ^ self.gmul(0x03, state[1][i]) ^ state[2][i] ^ state[3][i]
                b[1] = state[0][i] ^ self.gmul(0x02, state[1][i]) ^ self.gmul(0x03, state[2][i]) ^ state[3][i]
                b[2] = state[0][i] ^ state[1][i] ^ self.gmul(0x02, state[2][i]) ^ self.gmul(0x03, state[3][i])
                b[3] = self.gmul(0x03, state[0][i]) ^ state[1][i] ^ state[2][i] ^ self.gmul(0x02, state[3][i])

            for j in range(4):
                state[j][i] = b[j]

    def add_round_key(self, state, w):
        for i in range(4):
            for j in range(self.Nb):
                state[i][j] ^= w[j][i]

    def cycle_shift(self, row, shift):
        return row[-shift:] + row[:-shift]

    def r_count(self):
        if self.Nb == 8 or self.Nk == 8:
            return 14
        if self.Nb == 6 or self.Nk == 6:
            return 12
        return 10

    def to_state(self, block):
        state = []

        for i in range(4):
            state.append([block[i + 4 * j] for j in range(self.Nb)])

        return state

    def to_block(self, state):
        block = bytearray(4 * self.Nb)

        for i in range(4):
            for j in range(self.Nb):
                block[i + 4 * j] = state[i][j]

        return block

    def gen_s(self):
        p, q = 1, 1

        while True:
            if p & 0x80 == 0x80:
                p ^= ((p << 1) ^ 0x11B) & 0xFF
            else:
                p ^= (p << 1) & 0xFF

            for i in [1, 2, 4]:
                q ^= (q << i)

            if q & 0x80 == 0x80:
                q ^= 0x09
            q &= 0xFF

            self.S[p] = ((q ^ self.cycle_byte(q, 1) ^ self.cycle_byte(q, 2) ^ self.cycle_byte(q, 3) ^ self.cycle_byte(q, 4)) ^ 0x63) & 0xFF

            if p == 1:
                break

        self.S[0] = 0x63

    def cycle_byte(self, x, shift):
        return ((x << shift) | (x >> (8 - shift))) & 0xFF

    def gen_inv_s(self):
        for i in range(256):
            self.INV_S[self.S[i]] = i

    def gen_r_con(self):
        x = 0x02

        self.R_CON[0], self.R_CON[1] = 1, x

        for i in range(2, 32):
            self.R_CON[i] = self.gmul(self.R_CON[i - 1], x)

    def gmul(self, a, b):
        p = 0

        for _ in range(8):
            if (b & 1) != 0:
                p ^= a
            is_high = (a & 0x80) != 0
            a <<= 1
            a &= 0xFF
            if is_high:
                a ^= 0x1B
            b >>= 1
        return p


class ECB():
    def __init__(self, aes):
        self._aes = aes
        self.bs = self._aes.get_block_size()

    def encode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        if len(blocks) > 0:
            blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')

        enc = []
        for block in blocks:
            enc.append(self._aes.encode_block(block))

        return enc

    def decode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        if len(blocks) > 0:
            blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')

        dec = []
        for block in blocks:
            dec.append(self._aes.decode_block(block))

        return dec


class CBC():
    def __init__(self, aes, c0):
        self._aes = aes
        self._c0 = c0
        self.bs = self._aes.get_block_size()

    def encode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        if len(blocks) > 0:
            blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')
        prev = self._c0

        enc = []
        for block in blocks:
            enc.append(self._aes.encode_block(xor_bytes(block, prev, self.bs)))
            prev = enc[-1]

        return enc

    def decode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        if len(blocks) > 0:
            blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')
        prev = self._c0

        dec = []
        for block in blocks:
            dec.append(xor_bytes(self._aes.decode_block(block), prev, self.bs))
            prev = block

        return dec


class OFB():
    def __init__(self, aes, c0):
        self._aes = aes
        self._c0 = c0
        self.bs = self._aes.get_block_size()

    def encode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        if len(blocks) > 0:
            blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')
        prev = self._c0

        enc = []
        for block in blocks:
            prev = self._aes.encode_block(prev)
            enc.append(xor_bytes(prev, block, self.bs))

        return enc

    def decode(self, b_arr):
        return self.encode(b_arr)


class CFB():
    def __init__(self, aes, c0):
        self._aes = aes
        self._c0 = c0
        self.bs = self._aes.get_block_size()

    def encode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        if len(blocks) > 0:
            blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')
        prev = self._c0

        enc = []
        for block in blocks:
            enc.append(xor_bytes(self._aes.encode_block(prev), block, self.bs))
            prev = enc[-1]

        return enc

    def decode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        if len(blocks) > 0:
            blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')
        prev = self._c0

        dec = []
        for block in blocks:
            dec.append(xor_bytes(self._aes.encode_block(prev), block, self.bs))
            prev = block

        return dec


def xor_bytes(a, b, size):
    return (int.from_bytes(a, byteorder='little') ^ int.from_bytes(b, byteorder='little')).to_bytes(size, byteorder='little')