class Rijndael:
    def __init__(self, key, block_len):
        '''
        key_len = {4 / 6 / 8}
        block_len = {4 / 6 / 8}
        '''
        self.S = bytearray([0x63] * 256)
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
        keys = [[key[4 * i + j] for j in range(4)] for i in range(self.Nk)]

        for i in range(self.Nk, self.Nb * (self.Nr + 1)):
            if i % self.Nk == 0:
                temp = [self.S[x] for x in self.cycle_shift(keys[i - 1], -1)]
                temp[0] ^= self.R_CON[i // self.Nk]
            elif (i % self.Nk == 4) and (self.Nk > 6):
                temp = [self.S[x] for x in temp]
            keys.append([keys[i - self.Nk][j] ^ temp[j] for j in range(4)])

        return keys

    def sub_bytes(self, state, dec=False):
        if dec:
            S = self.INV_S
        else:
            S = self.S

        for i in range(4):
            for j in range(self.Nb):
                state[i][j] = S[state[i][j]]

    def shift_rows(self, state, dec=False):
        if dec:
            c = [-1, -2, -3]
        else:
            c = [1, 2, 3]

        for i in range(1, 4):
            state[i] = self.cycle_shift(state[i], c[i - 1])

    def mix_columns(self, state, dec=False):
        mul = self.gmul

        if dec:
            c = [0x0E, 0x0B, 0x0D, 0x09]
        else:
            c = [0x02, 0x03, 0x01, 0x01]

        for i in range(self.Nb):
            st = [state[j][i] for j in range(4)]
            for j in range(4):
                state[j][i] = mul(c[0], st[0]) ^ mul(c[1], st[1]) ^ mul(c[2], st[2]) ^ mul(c[3], st[3])
                c = self.cycle_shift(c, 1)

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
        return [[block[i + 4 * j] for j in range(self.Nb)] for i in range(4)]

    def to_block(self, state):
        block = bytearray(4 * self.Nb)

        for i in range(4):
            for j in range(self.Nb):
                block[i + 4 * j] = state[i][j]

        return block

    def gen_s(self):
        p = q = 1

        while True:
            if p & 0x80 != 0:
                p ^= (p << 1) ^ 0x11B
            else:
                p ^= p << 1

            for i in [1, 2, 4]:
                q ^= (q << i) & 0xFF

            if q & 0x80 != 0:
                q ^= 0x09

            for i in range(5):
                self.S[p] ^= self.cycle_byte(q, i)

            if p == 1:
                break

    def cycle_byte(self, x, shift):
        return ((x << shift) | (x >> (8 - shift))) & 0xFF

    def gen_inv_s(self):
        for i in range(256):
            self.INV_S[self.S[i]] = i

    def gen_r_con(self):
        self.R_CON[0] = 0x01

        for i in range(1, 32):
            self.R_CON[i] = self.gmul(self.R_CON[i - 1], 0x02)

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
        blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')

        return [self._aes.encode_block(block) for block in blocks]

    def decode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')

        return [self._aes.decode_block(block) for block in blocks]


class CBC():
    def __init__(self, aes, c0):
        self._aes = aes
        self._c0 = c0
        self.bs = self._aes.get_block_size()

    def encode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')
        prev = self._c0

        enc = []
        for block in blocks:
            enc.append(self._aes.encode_block(xor_bytes(block, prev, self.bs)))
            prev = enc[-1]

        return enc

    def decode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
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
        blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')
        prev = self._c0

        enc = []
        for block in blocks:
            enc.append(xor_bytes(self._aes.encode_block(prev), block, self.bs))
            prev = enc[-1]

        return enc

    def decode(self, b_arr):
        blocks = [b_arr[i: i + self.bs] for i in range(0, len(b_arr), self.bs)]
        blocks[-1] = int.from_bytes(blocks[-1], byteorder='little').to_bytes(self.bs, byteorder='little')
        prev = self._c0

        dec = []
        for block in blocks:
            dec.append(xor_bytes(self._aes.encode_block(prev), block, self.bs))
            prev = block

        return dec


def xor_bytes(a, b, size):
    return (int.from_bytes(a, byteorder='little') ^ int.from_bytes(b, byteorder='little')).to_bytes(size, byteorder='little')