# Solution to http://adventofcode.com/2017/day/14

import unittest
import sys
from day_10 import knot_hash


def nibble(n):
    bits, i = [], 0
    while i < 4:
        if n & 0x1:
            bits.insert(0, 1)
        else:
            bits.insert(0, 0)
        n >>= 1
        i += 1
    return bits


def build_disk_map(key):
    m = []
    for i in range(128):
        r = []
        h = knot_hash(key + '-' + str(i))
        for c in h:
            n = int(c, base=16)
            r.extend(nibble(n))
        m.append(r)
    return m


def count_used_blocks(m):
    used = 0
    for r in m:
        for c in r:
            if c == 1:
                used += 1
    return used


def count_regions(m):
    region, rows, cols = 2, len(m), len(m[0])
    for i in range(rows):
        for j in range(cols):
            if m[i][j] == 1:
                mark_region(m, region, i, j)
                region += 1
    return region - 2


def mark_region(m, region, i, j):
    rows = len(m)
    cols = len(m[0])
    m[i][j] = region
    if i >= 1 and m[i - 1][j] == 1:
        mark_region(m, region, i - 1, j)
    if i < rows - 1 and m[i + 1][j] == 1:
        mark_region(m, region, i + 1, j)
    if j >= 1 and m[i][j - 1] == 1:
        mark_region(m, region, i, j - 1)
    if j < cols - 1 and m[i][j + 1] == 1:
        mark_region(m, region, i, j + 1)


class Test(unittest.TestCase):

    def test_count_bits(self):
        test_data = [(0, [0, 0, 0, 0]),
                     (4, [0, 1, 0, 0]),
                     (5, [0, 1, 0, 1]),
                     (7, [0, 1, 1, 1])]
        for n, e in test_data:
            self.assertEqual(e, nibble(n))

    def test_count_used_blocks(self):
        m = build_disk_map('flqrgnkx')
        self.assertEqual(8108, count_used_blocks(m))

    def test_count_regions(self):
        m = build_disk_map('flqrgnkx')
        self.assertEqual(1242, count_regions(m))


def main():
    if len(sys.argv) >= 2:
        for key in sys.argv[1:]:
            m = build_disk_map(key)
            print('%s -> %d %d' %
                  (key, count_used_blocks(m), count_regions(m)))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
