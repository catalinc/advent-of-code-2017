# Solution to http://adventofcode.com/2017/day/15

import unittest
import sys


def random_gen(seed, constant):
    value = seed
    while True:
        value = (value * constant) % 2147483647
        yield value


def random_gen_wrapper(seed, constant, factor):
    rnd = random_gen(seed, constant)
    while True:
        for v in rnd:
            if v % factor == 0:
                yield v


def lsb16(n):
    return n & 0x0000ffff


def judge(rnd1, rnd2, rounds):
    matches = 0
    for _ in range(rounds):
        v1 = next(rnd1)
        v2 = next(rnd2)
        if lsb16(v1) == lsb16(v2):
            matches += 1
    return matches


class Test(unittest.TestCase):

    def test_random_gen(self):
        test_data = [
            (65, 16807, [1092455, 1181022009, 245556042, 1744312007, 1352636452])]
        for seed, constant, expected_values in test_data:
            rnd = random_gen(seed, constant)
            actual_values = []
            for _ in range(len(expected_values)):
                actual_values.append(next(rnd))
            self.assertEqual(expected_values, actual_values)

    def test_random_gen_wrapper(self):
        test_data = [
            (65, 16807, 4, [1352636452, 1992081072, 530830436, 1980017072, 740335192])]
        for seed, constant, factor, expected_values in test_data:
            rnd = random_gen_wrapper(seed, constant, factor)
            actual_values = []
            for _ in range(len(expected_values)):
                actual_values.append(next(rnd))
            self.assertEqual(expected_values, actual_values)

    def test_random_gen_matches(self):
        rnd1 = random_gen(65, 16807)
        rnd2 = random_gen(8921, 48271)
        self.assertEqual(588, judge(rnd1, rnd2, 40000000))

    def test_random_gen_wrapper_matches(self):
        rnd1 = random_gen_wrapper(65, 16807, 4)
        rnd2 = random_gen_wrapper(8921, 48271, 8)
        self.assertEqual(309, judge(rnd1, rnd2, 5000000))


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == '-run':
        rnd1 = random_gen(277, 16807)
        rnd2 = random_gen(349, 48271)
        print(judge(rnd1, rnd2, 40000000))
        rnd1 = random_gen_wrapper(277, 16807, 4)
        rnd2 = random_gen_wrapper(349, 48271, 8)
        print(judge(rnd1, rnd2, 5000000))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
