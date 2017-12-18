# Solution to http://adventofcode.com/2017/day/17

import unittest
import sys


def spinlock(steps, times):
    data = [0]
    i, j = 1, 0
    while i <= times:
        j = (j + 1 + steps) % len(data)
        data.insert(j, i)
        i += 1
    j = (j + 1) % len(data)
    return data[j]


class Test(unittest.TestCase):

    def test_spinlock(self):
        self.assertEqual(638, spinlock(3, 2017))


def main():
    if len(sys.argv) == 2 and sys.argv[1] == '-run':
        print(spinlock(337, 50000000))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
