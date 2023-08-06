from hashlib import sha256


class RandomGenerator:
    def __init__(self, key):
        self.seed = sha256(key).digest()
        self.count = 0

    def next(self):
        self.count += 1
        return sha256(self.seed + bytes([self.count])).digest()

    def get_string(self, length):
        return bytes((self.next()[0] for _ in range(length)))

    def __getitem__(self, item):
        return sha256(self.seed + bytes([item])).digest()


if __name__ == '__main__':
    rnd = RandomGenerator(b'0')
    s0 = bytes((rnd.next()[0] for i in range(100)))

    rnd = RandomGenerator(b'0')
    s1 = rnd.get_string(100)

    print(s0, '='*100, s1, sep='\n\n')
