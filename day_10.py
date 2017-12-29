# Solution to http://adventofcode.com/2017/day/10

import unittest
import sys


def hash_round(array, key, pos=0, skip=0):
    for k in key:
        reverse(array, pos, pos + k)
        pos += (k + skip) % len(array)
        skip += 1
    return pos, skip, array


def reverse(array, start, end):
    i, j, size = start, end - 1, len(array)
    i, j = i % size, j % size
    swaps, max_swaps = 0, (end - start) / 2
    while swaps < max_swaps:
        array[i], array[j] = array[j], array[i]
        i = (i + 1) % size
        j = (j - 1) % size
        swaps += 1


def make_key(s):
    return [ord(c) for c in s]


def knot_hash(key, rounds=64):
    key = make_key(key)
    key.extend([17, 31, 73, 47, 23])
    array = list(range(256))
    pos, skip = 0, 0
    for _ in range(rounds):
        pos, skip, array = hash_round(array, key, pos=pos, skip=skip)
    blocks = []
    for i in range(0, len(array), 16):
        b = array[i]
        for j in range(i + 1, i + 16):
            b ^= array[j]
        blocks.append(b)
    return ''.join([format(b, '02x') for b in blocks])


class Test(unittest.TestCase):

    def test_hash_round(self):
        _, _, actual = hash_round([0, 1, 2, 3, 4], [3, 4, 1, 5])
        self.assertEqual([3, 4, 2, 1, 0], actual)

    def test_knot_hash(self):
        test_data = [("", "a2582a3a0e66e6e86e3812dcb672a272"),
                     ("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
                     ("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
                     ("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e")]
        for key, expected in test_data:
            actual = knot_hash(key)
            self.assertEqual(expected, actual)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == '-run':
        array = list(range(256))
        key = [106, 16, 254, 226, 55, 2, 1,
               166, 177, 247, 93, 0, 255, 228, 60, 36]
        print(hash_round(array, key))
        key = ','.join([str(n) for n in key])
        print(knot_hash(key))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
