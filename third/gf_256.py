def to_polynom_form(b):
    res = ''

    for i in range(7, -1, -1):
        if get_bit(b, i) == 1:
            res += f'x^{i}+'

    res = res.replace('x^0', '1')
    res = res.replace('x^1', 'x')
    res = res[:-1]

    return res


def get_bit(a, k):
    return (a >> k) & 1


def mul(a, b):
    aa, bb, r, t = a, b, 0, 0

    while aa != 0:
        if (aa & 1) != 0:
            r ^= bb

        t = bb & 0x80
        bb <<= 1

        if t != 0:
            bb ^= 0x1B

        aa >>= 1

    return r & 0xFF


def inv(a):
    return _pow(a, 254)


def _pow(a, n):
    res = a

    while n > 1:
        n -= 1
        res = mul(res, a)

    return res
