from collections import namedtuple


class Mode:
    def encode(self, message):
        pass

    def decode(self, code):
        pass

    @staticmethod
    def _bytes_to_block(b_arr):
        return int.from_bytes(b_arr, 'little')

    @staticmethod
    def bytes_to_blocks(b_arr):
        res = []

        for i in range(0, len(b_arr), 8):
            cur_bytes = b_arr[i:i + 8]
            res.append(Mode._bytes_to_block(cur_bytes))

        return res

    @staticmethod
    def _block_to_bytes(block):
        return block.to_bytes(8, byteorder='little')

    @staticmethod
    def blocks_to_bytes(l_arr):
        b_arr = bytearray()

        for long in l_arr:
            b_arr.extend(Mode._block_to_bytes(long))

        return b_arr


Pair = namedtuple("Pair", ["left", "right"])


IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25
]

E = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]

P = [
    16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

S_BLOCKS = [
    [
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
         0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
         4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    ],
    [
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
         3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
         0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
    ],
    [
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
         1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
    ],
    [
         7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
         3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    ],
    [
         2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
         4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    ],
    [
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
         9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
         4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    ],
    [
         4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
         1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
         6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    ],
    [
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
         1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
         7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
         2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    ]
]

PC_1 = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
]

PC_2 = [
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]


class DES:
    def __init__(self, key):
        if key != key & 0xFFFFFFFFFFFFFFFF:
            raise ValueError("Invalid DES key size. Key must be exactly 8 bytes long.")
        self._key = key

    def encode_block(self, block):
        ip = DES._permute(block, IP)
        keys = self._unwrapping_key()

        pair = Pair(
            (ip & 0xFFFFFFFF),
            ((ip >> 32) & 0xFFFFFFFF)
        )

        for i in range(16):
            pair = Pair(
                pair.right,
                pair.left ^ self._func(pair.right, keys[i])
            )

        joined = ((pair.left << 32) | pair.right)

        return DES._permute(joined, FP)

    def decode_block(self, block):
        ip = DES._permute(block, IP)
        keys = self._unwrapping_key()

        pair = Pair(
            ((ip >> 32) & 0xFFFFFFFF),
            (ip & 0xFFFFFFFF)
        )

        for i in range(15, -1, -1):
            pair = Pair(
                (pair.right ^ self._func(pair.left, keys[i])),
                pair.left
            )

        joined = ((pair.right << 32) | pair.left)

        return DES._permute(joined, FP)

    def _func(self, right, key):
        e = DES._permute(right, E)
        x = e ^ key

        boxes = []
        for _ in range(8):
            b = x & 0x3F
            boxes.append(b)
            x >>= 6

        k = 0
        for i in range(7, -1, -1):
            box = boxes[i]
            row = ((box & 1) << 1) | ((box & 32) >> 5)
            col = ((box & 2) << 2) | (box & 4) | ((box & 8) >> 2) | ((box & 16) >> 3)
            val = S_BLOCKS[i][(row << 4) + col]
            k <<= 4
            k |= val

        res = DES._permute(k, P)

        return res

    def _unwrapping_key(self):
        p = DES._permute(self._key, PC_1)
        c0 = DES._left_28(p)
        d0 = DES._right_28(p)

        cd = [Pair(c0, d0)]
        shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

        for i in range(16):
            cd.append(Pair(
                DES._left_shift_28(cd[i].left, shifts[i]),
                DES._left_shift_28(cd[i].right, shifts[i])
            ))

        res = []
        for i in range(1, 17):
            joined = DES._join_28_to_56(cd[i].left, cd[i].right)
            permutation = DES._permute(joined, PC_2)
            res.append(permutation)

        return res

    @staticmethod
    def _join_28_to_56(c, d):
        return ((d << 28) | c)  & 0xFFFFFFFFFFFFFF

    @staticmethod
    def _left_28(a):
        return (a & 0xFFFFFFF)

    @staticmethod
    def _right_28(a):
        return ((a >> 28) & 0xFFFFFFF)

    @staticmethod
    def _left_shift_28(a, k):
        return ((a >> k) | ((a & (1 << k) - 1) << (28 - k))) & 0xFFFFFFF

    @staticmethod
    def _permute(a, arr):
        res = 0

        for k in reversed(arr):
            res <<= 1
            res |= ((a >> (k - 1)) & 1)

        return res


class ECB(Mode):
    def __init__(self, des):
        self.des = des

    def encode(self, b_arr):
        blocks = self.bytes_to_blocks(b_arr)
        res = [self.des.encode_block(block) for block in blocks]

        return self.blocks_to_bytes(res)

    def decode(self, b_arr):
        blocks = self.bytes_to_blocks(b_arr)
        res = [self.des.decode_block(block) for block in blocks]

        return self.blocks_to_bytes(res)


class CBC(Mode):
    def __init__(self, des, c0):
        self.des = des
        self.c0 = c0

    def encode(self, b_arr):
        blocks = self.bytes_to_blocks(b_arr)
        prev = self.c0
        res = []

        for block in blocks:
            res.append(self.des.encode_block(block ^ prev))
            prev = res[-1]

        return self.blocks_to_bytes(res)

    def decode(self, b_arr):
        blocks = self.bytes_to_blocks(b_arr)
        prev = self.c0
        res = []

        for block in blocks:
            res.append(self.des.decode_block(block) ^ prev)
            prev = blocks[-1]

        return self.blocks_to_bytes(res)


class OFB(Mode):
    def __init__(self, des, c0):
        self.des = des
        self.c0 = c0

    def encode(self, b_arr):
        blocks = self.bytes_to_blocks(b_arr)
        prev = self.c0
        res = []

        for block in blocks:
            prev = self.des.encode_block(prev)
            res.append(block ^ prev)

        return self.blocks_to_bytes(res)

    def decode(self, b_arr):
        return self.encode(b_arr)


class CFB(Mode):
    def __init__(self, des, c0):
        self.des = des
        self.c0 = c0

    def encode(self, b_arr):
        blocks = self.bytes_to_blocks(b_arr)
        prev = self.c0
        res = []

        for block in blocks:
            res.append(self.des.encode_block(prev) ^ block)
            prev = res[-1]

        return self.blocks_to_bytes(res)

    def decode(self, b_arr):
        blocks = self.bytes_to_blocks(b_arr)
        prev = self.c0
        res = []

        for block in blocks:
            res.append(self.des.encode_block(prev) ^ block)
            prev = block

        return self.blocks_to_bytes(res)