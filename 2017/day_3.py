# Solution to http://adventofcode.com/2017/day/3

import unittest
import sys
import collections

directions = [(1, 0),
              (0, 1),
              (-1, 0),
              (0, -1)]


def coordinates(n):
    x, y = 0, 0
    i, j = 1, 0
    while i < n:
        d = directions[j]
        x += d[0]
        y += d[1]
        i += 1
        if abs(x) == abs(y) or i == 2:        # corner || 2 -> change direction
            j = (j + 1) % len(directions)
            if j == 1 and i != 2:             # bottom right != 2 -> step right
                x += 1
                i += 1
    return x, y


def distance(n):
    x, y = coordinates(n)
    return abs(x) + abs(y)


def memory_test(n):
    mem = collections.defaultdict(int)
    mem[(0, 0)] = 1
    mem[(1, 0)] = 1
    x, y = 1, 0
    i = 1
    j = 1
    while i <= n:
        d = directions[j]
        x += d[0]
        y += d[1]
        i = mem_sum(x, y, mem)
        mem[(x, y)] = i
        if abs(x) == abs(y):
            j = (j + 1) % len(directions)
            if j == 1:
                x += 1
                if i > n:
                    return i
                i = mem_sum(x, y, mem)
                mem[(x, y)] = i
    return i


def mem_sum(x, y, mem):
    s = 0
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            s += mem[(x + i, y + j)]
    return s


class Test(unittest.TestCase):

    def test_coordinates(self):
        test_data = [(1, (0, 0)), (2, (1, 0)), (4, (0, 1)),
                     (10, (2, -1)), (13, (2, 2)), (23, (0, -2))]
        for n, expected in test_data:
            actual = coordinates(n)
            self.assertEqual(expected, actual,
                             "failed for %d, expected %s got %s" %
                             (n, expected, actual))

    def test_distance(self):
        test_data = [(1, 0), (2, 1), (13, 4), (12, 3), (23, 2), (1024, 31)]
        for n, expected in test_data:
            actual = distance(n)
            self.assertEqual(expected, actual,
                             "failed for %d, expected %s got %s" %
                             (n, expected, actual))

    def test_mem_test(self):
        test_data = [(5, 10), (23, 25), (59, 122), (122, 133)]
        for n, expected in test_data:
            actual = memory_test(n)
            self.assertEqual(expected, actual,
                             "failed for %d, expected %s got %s" %
                             (n, expected, actual))


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        for x in sys.argv[1:]:
            n = int(x)
            print("%d -> distance:%d memory-test:%d" %
                  (n, distance(n), memory_test(n)))
    else:
        unittest.main()
