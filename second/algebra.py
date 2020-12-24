def get_prime_numbers(m):
    if m < 2:
        return []

    res = [2]

    for i in range(3, m + 1, 2):
        if i > 10 and i % 10 == 5:
            continue

        for j in res:
            if j ** 2 - 1 > i:
                res.append(i)
                break

            if i % j == 0:
                break
        else:
            res.append(i)

    return res


def euclid(a, b):
    while b > 0:
        a %= b
        a, b = b, a

    return a


def euler(n):
    res = n - 1

    for i in range(1, n):
        if euclid(i, n) != 1:
            res -= 1

    return res


def rds(n):
    res = []

    for i in range(1, n):
        if euclid(i, n) == 1:
            res.append(i)

    return res


def factorization(n):
    res = []
    i = 1

    while i <= n:
        i += 1
        if n % i == 0:
            while n % i == 0:
                n //= i
                res.append(i)

    return res


def pow_mod(a, b, m):
    res = 1

    while b > 0:
        if b & 1:
            res = (res * a) % m
        a = (a ** 2) % m
        b >>= 1

    return res