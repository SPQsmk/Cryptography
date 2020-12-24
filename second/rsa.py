import random


def euclid_ex_bin(a, b):
    g = 1

    while (a & 1) == 0 and (b & 1) == 0:
        a >>= 1
        b >>= 1
        g <<= 1

    u, v = a, b
    A, B, C, D = 1, 0, 0, 1

    while u != 0:
        while (u & 1) == 0:
            u >>= 1

            if (A & 1) == 0 and (B & 1) == 0:
                A >>= 1
                B >>= 1
            else:
                A = (A + b) >> 1
                B = (B - a) >> 1

        while (v & 1) == 0:
            v >>= 1

            if (C & 1) == 0 and (D & 1) == 0:
                C >>= 1
                D >>= 1
            else:
                C = (C + b) >> 1
                D = (D - a) >> 1

        if u >= v:
            u -= v
            A -= C
            B -= D
        else:
            v -= u
            C -= A
            D -= B

    x = C
    y = D

    return g * v, x, y


def mult_inverse(a, m):
    g, x, _ = euclid_ex_bin(a, m)

    if g != 1:
        raise Exception('Not exist')

    return x % m


def is_prime(n):
    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False

    if n == 2 or n == 3 or n == 5 or n == 7:
        return True

    if n & 1 == 0:
        return False

    s = 0
    d = n - 1

    while d & 1 == 0:
        d >>= 1
        s += 1

    assert(2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for _ in range(8):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
    return True


class RSA:
    def __init__(self):
        p = RSA.gen()
        q = RSA.gen()
        self.n = p * q

        f = (p - 1) * (q - 1)
        E = [3, 5, 17, 257, 65537]

        i = 4
        while True:
            try:
                self.e = E[i]
                self.d = mult_inverse(self.e, f)
                break
            except:
                i -= 1
                if i == -1:
                    p = RSA.gen()
                    q = RSA.gen()
                    self.n = p * q
                    f = (p - 1) * (q - 1)
                    i = 4

    def encode(self, message):
        enc = pow(int.from_bytes(message, byteorder='little'), self.e, self.n)
        return enc.to_bytes(256, byteorder='little')

    @staticmethod
    def decode(message, d, n):
        dec = pow(int.from_bytes(message, byteorder='little'), d, n)
        return dec.to_bytes(255, byteorder='little')

    def get_key(self):
        return self.d, self.n

    @staticmethod
    def gen():
        x = RSA.rand_num(128)

        if not (x & 1):
            x |= 1

        while not is_prime(x):
            x += 2
            x &= ((1 << 1024) - 1)

        return x

    @staticmethod
    def rand_num(length):
        res = 0

        for _ in range(length):
            res <<= 8
            res |= random.randint(1, 255)

        return res