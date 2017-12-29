# Solution to http://adventofcode.com/2017/day/2
import unittest
import sys


def matrix_checksum(matrix, row_fn):
    total = 0
    for row in matrix:
        total += row_fn(row)
    return total


def min_max_diff(row):
    if not row:
        return 0
    min_val = row[0]
    max_val = row[0]
    for n in row:
        if n < min_val:
            min_val = n
        elif n > max_val:
            max_val = n
    return max_val - min_val


def even_divisible(row):
    for i in range(len(row) - 1):
        for j in range(i + 1, len(row)):
            a = row[i]
            b = row[j]
            if a < b:
                a, b = b, a
            q, r = divmod(a, b)
            if r == 0:
                return q
    return 0


def parse_matrix_from_file(filename):
    matrix = []
    with open(filename, 'r') as input_file:
        for line in input_file:
            row = [int(t) for t in line.split()]
            matrix.append(row)
    return matrix


class Test(unittest.TestCase):

    def test_min_max_diff(self):
        test_data = [([5, 1, 9, 5], 8), ([7, 5, 3], 4)]
        for row, expected in test_data:
            self.assertEqual(expected, min_max_diff(row))

    def test_even_divisible(self):
        test_data = [([5, 9, 2, 8], 4), ([9, 4, 7, 3], 3), ([3, 8, 6, 5], 2)]
        for row, expected in test_data:
            self.assertEqual(expected, even_divisible(row))

    def test_matrix_checksum(self):
        test_data = [[5, 1, 9, 5], [7, 5, 3], [2, 4, 6, 8]]
        self.assertEqual(18, matrix_checksum(test_data, row_fn=min_max_diff))
        test_data = [[5, 9, 2, 8], [9, 4, 7, 3], [3, 8, 6, 5]]
        self.assertEqual(9, matrix_checksum(test_data, row_fn=even_divisible))


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            matrix = parse_matrix_from_file(name)
            for fn in [min_max_diff, even_divisible]:
                print('Checksum.%s for %s is %d' %
                      (fn.__name__, name, matrix_checksum(matrix, row_fn=fn)))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
