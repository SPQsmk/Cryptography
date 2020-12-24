class RC4:
    def __init__(self):
        self.i = 0
        self.j = 0

    def encode(self, text, key):
        if not len(key):
            raise ValueError('Empty key')

        s = self.s_init(key)
        res = bytearray()
        self.i = 0
        self.j = 0

        for b in text:
            res.append(self.generate_key(s) ^ b)

        return res

    @staticmethod
    def s_init(key):
        s = list(range(256))
        j = 0

        for i in range(256):
            j = (j + s[i] + key[i % len(key)]) % 256
            s[i], s[j] = s[j], s[i]

        return s

    def generate_key(self, s):
        self.i = (self.i + 1) % 256
        self.j = (self.j + s[self.i]) % 256
        s[self.i], s[self.j] = s[self.j], s[self.i]
        k = s[(s[self.i] + s[self.j]) % 256]

        return k