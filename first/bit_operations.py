from math import log2


def get_bit(a, k):
    return (a >> k) & 1


def change_bit(a, k):
    return a ^ (1 << k)


def swap_bits(a, i, j):
    b1 = get_bit(a, i)
    b2 = get_bit(a, j)

    if b1 == b2:
        return a

    mask = (1 << i) | (1 << j)

    return a ^ mask


def zero_bits(a, m):
    return (a >> m) << m


def glue_bits(a, i, length):
    return (a >> (length - i) << i) | (a & ((1 << i) - 1))


def get_middle_bits(a, i, length):
    return (a >> i) & ((1 << (length - 2 * i)) - 1)


def swap_bytes(a, i, j):
    if i == j:
        return a

    bi = (a & ((1 << (8 * (i + 1))) - 1)) >> (8 * i)
    bj = (a & ((1 << (8 * (j + 1))) - 1)) >> (8 * j)

    if bi == bj:
        return a

    a = a ^ (bi << (i * 8))
    a = a ^ (bj << (j * 8))
    a = (a | (bi << (j * 8)) | (bj << (i * 8)))

    return a


def max_div_pow2(a):
    return int(log2(a & -a))


def within_range(a):
    p = 0

    while a > 1:
        a >>= 1
        p += 1

    return p


def xor_all_bits(a):
    p = 1 << (within_range(a) + 1)

    while p > 1:
        p >>= 1
        a = (a >> p) ^ (a & ((1 << (p)) - 1))

    return a


def cycle_left(a, p, n):
    p = p % n

    return ((a << p) | (a >> (n - p))) & ((1 << n) - 1)


def cycle_right(a, p, n):
    p = p % n

    return (a >> p) | ((a & (1 << p) - 1) << (n - p))


def transpose_bits(a, arr):
    res = 0

    for item in reversed(arr):
        res <<= 1
        res |= get_bit(a, item)

    return res