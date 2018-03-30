from bitarray import bitarray
import bitstring as bs


# noinspection PyMethodMayBeStatic
class SHA1(object):
    def __init__(self):
        self.block_size = 512
        self.t = 0
        self.H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    def k(self, t):
        if 0 <= t <= 19:
            return 0x5A827999
        elif 20 <= t <= 39:
            return 0x6ED9EBA1
        elif 40 <= t <= 59:
            return 0x8F1BBCDC
        elif 60 <= t <= 79:
            return 0xCA62C1D6

    def f(self, t, b, c, d):
        if 0 <= t <= 19:
            return (b & c) | ((~ b) & d)
        elif 20 <= t <= 39:
            return b ^ c ^ d
        elif 40 <= t <= 59:
            return (b & c) | (b & d) | (c & d)
        elif 60 <= t <= 79:
            return b ^ c ^ d

    def prepare_file(self, file_address):
        operator = bitarray()
        operator.fromfile(open(file_address, 'rb'))

        size = len(operator)
        binary_size = format(size, "064b")
        multiplier = size / self.block_size
        last_block_size = size - self.block_size * multiplier

        if last_block_size <= 447:
            zero_count = size - last_block_size - 1 - 64
            last_block_append = '1' + '0' * zero_count + binary_size
        else:
            zero_count = self.block_size - last_block_size - 1
            last_block_append = '1' + '0' * (zero_count + 448) + binary_size
        operator.extend(last_block_append)
        operator.tofile(open('./file_in', 'wb'))
        return len(operator)

    def digest(self, file_address):
        block_count = self.prepare_file(file_address) / self.block_size
        file_in = bs.ConstBitStream(filename='./file_in')

        for i in range(0, block_count):
            block = file_in.read(self.block_size)

            w = []
            for j in range(0, 16):
                w.append(block[j * 32: (j + 1) * 32 - 1])

            for t in range(16, 80):
                token = w[t - 3] ^ w[t - 8] ^ w[t - 14] ^ w[t - 16]
                w.append(token << 1)

            a = self.H[0]
            b = self.H[1]
            c = self.H[2]
            d = self.H[3]
            e = self.H[4]

            for t in range(0, 80):
                temp = ((a << 5) + self.f(t, b, c, d) + e + w[t] + self.k(t)) % (2 ** 32)
                e = d
                d = c
                c = b << 30
                b = a
                a = temp

            self.H[0] = (self.H[0] + a) % (2 ** 32)
            self.H[1] = (self.H[1] + b) % (2 ** 32)
            self.H[2] = (self.H[2] + c) % (2 ** 32)
            self.H[3] = (self.H[3] + d) % (2 ** 32)
            self.H[4] = (self.H[3] + e) % (2 ** 32)

            print self.H


# input_file = open('./src.txt', 'rb+')
lol = SHA1()
lol.digest('./src.txt')
