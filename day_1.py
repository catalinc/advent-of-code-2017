# Solution to http://adventofcode.com/2017/day/1

import unittest


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


class Test(unittest.TestCase):

    def test_captcha(self):
        test_data = [("1122", 3), ("1111", 4), ("1234", 0), ("91212129", 9)]
        for sequence, expected in test_data:
            self.assertEqual(expected, captcha(sequence),
                             "failed for %s" % sequence)


if __name__ == '__main__':
    sequence = raw_input("Enter sequence: ")
    print(captcha(sequence))
