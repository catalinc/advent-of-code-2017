# Solution to http://adventofcode.com/2017/day/10

import unittest
import sys


def hash_knot(size, lenghts):
    if len(lenghts) < 2:
        return 1, [1]
    array, pos, skip = list(range(size)), 0, 0
    for l in lenghts:
        reverse(array, pos, pos + l)
        pos += (l + skip) % size
        skip += 1
    return array[0] * array[1], array


def reverse(array, start, end):
    i, j, size = start, end - 1, len(array)
    i, j = i % size, j % size
    swaps, max_swaps = 0, (end - start) / 2
    while swaps < max_swaps:
        array[i], array[j] = array[j], array[i]
        i = (i + 1) % size
        j = (j - 1) % size
        swaps += 1


class Test(unittest.TestCase):

    def test_hash_knot(self):
        test_data = [(1, [1], (1, [1])),
                     (5, [3, 4, 1, 5], (12, [3, 4, 2, 1, 0]))]
        for size, lenghts, expected in test_data:
            actual = hash_knot(size, lenghts)
            self.assertEqual(expected, actual)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == '-run':
        lengths = [106, 16, 254, 226, 55, 2, 1,
                   166, 177, 247, 93, 0, 255, 228, 60, 36]
        print(hash_knot(256, lengths))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
