# Solution to http://adventofcode.com/2017/day/1

import unittest
import sys


def captcha(sequence):
    total = 0
    for i in range(len(sequence)):
        digit = sequence[i]
        j = i + 1
        if j == len(sequence):
            j = 0
        next_digit = sequence[j]
        if digit == next_digit:
            total += int(digit)
    return total


def captcha2(sequence):
    total = 0
    size = len(sequence)
    offset = size // 2
    for i in range(size):
        digit = sequence[i]
        j = (i + offset) % size
        next_digit = sequence[j]
        if digit == next_digit:
            total += int(digit)
    return total


class Test(unittest.TestCase):

    def test_captcha(self):
        test_data = [("1122", 3), ("1111", 4), ("1234", 0), ("91212129", 9)]
        for sequence, expected in test_data:
            self.assertEqual(expected, captcha(sequence),
                             "failed for %s" % sequence)

    def test_captcha2(self):
        test_data = [("1212", 6),
                     ("1221", 0),
                     ("123425", 4),
                     ("123123", 12),
                     ("12131415", 4)]
        for sequence, expected in test_data:
            actual = captcha2(sequence)
            self.assertEqual(expected, actual,
                             "failed for %s - expected %d got %d" %
                             (sequence, expected, actual))


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            with open(name, 'r') as infile:
                for i, line in enumerate(infile):
                    sequence = line.rstrip()
                    print('%s: line %d -> %d %d' %
                          (name, i, captcha(sequence), captcha2(sequence)))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
