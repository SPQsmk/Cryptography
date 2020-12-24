def vernam(_bytes, key):
    if not len(key):
        raise ValueError('Empty key')

    res = bytearray()

    for i, b in enumerate(_bytes):
        res.append(b ^ key[i % len(key)])

    return res