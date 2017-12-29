# Solution to http://adventofcode.com/2017/day/17

import unittest
import sys


def spin_lock(steps, times):
    data = [0]
    i, j = 1, 0
    while i <= times:
        j = (j + 1 + steps) % len(data)
        data.insert(j, i)
        i += 1
    j = (j + 1) % len(data)
    return data[j]


def spin_lock_2(steps, times):
    i, j, size = 1, 0, 1
    result = 0
    while i <= times:
        j = (j + 1 + steps) % size
        if j == 0:
            result = i
        size += 1
        i += 1
    return result


class Test(unittest.TestCase):

    def test_spin_lock(self):
        self.assertEqual(638, spin_lock(3, 2017))

    def test_spin_lock_2(self):
        self.assertEqual(9, spin_lock_2(3, 9))


def main():
    if len(sys.argv) == 2 and sys.argv[1] == '-run':
        print(spin_lock(337, 2017))
        print(spin_lock_2(337, 50_000_000))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
