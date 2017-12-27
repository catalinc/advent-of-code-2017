# Solution to http://adventofcode.com/2017/day/21

import unittest
import sys
import math


class Matrix(object):

    def __init__(self, size=0):
        self.data = [[0 for _ in range(size)] for _ in range(size)]

    def size(self):
        return len(self.data)

    def get(self, r, c):
        return self.data[r][c]

    def set(self, r, c, n):
        self.data[r][c] = n

    def clear(self):
        self.data.clear()

    def split(self, size):
        result = []
        for r in range(0, self.size() - size + 1, size):
            for c in range(0, self.size() - size + 1, size):
                m = Matrix(size)
                for i in range(size):
                    for j in range(size):
                        n = self.get(r + i, c + j)
                        m.set(i, j, n)
                result.append(m)
        return result

    @staticmethod
    def from_pattern(pattern):
        result = Matrix()
        result.data = [[1 if c == '#' else 0 for c in r]
                       for r in pattern.split('/')]
        return result

    @staticmethod
    def from_matrices(matrices):
        m_size = matrices[0].size()
        r_size = m_size * int(math.sqrt(len(matrices)))
        result = Matrix(r_size)
        k = 0
        for r in range(0, r_size - m_size + 1, m_size):
            for c in range(0, r_size - m_size + 1, m_size):
                m = matrices[k]
                for i in range(m_size):
                    for j in range(m_size):
                        d = m.get(i, j)
                        result.set(r + i, c + j, d)
                k += 1
        return result

    def sum(self):
        return sum([sum(r) for r in self.data])

    def rotate(self):
        result = Matrix()
        result.data = list([list(t) for t in zip(*self.data[::-1])])
        return result

    def flip_left(self):
        result = Matrix()
        for row in self.data:
            result.data.append(row[::-1])
        return result

    def flip_up(self):
        size = self.size()
        result = Matrix(size)
        for c in range(size):
            for r in range(size):
                result.set(r, c, self.get(size - r - 1, c))
        return result

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        return '/'.join([''.join(['#' if d == 1 else '.' for d in r])
                         for r in self.data])


class Test(unittest.TestCase):

    def test_build_matrix_from_pattern(self):
        p = '../#.'
        m = Matrix.from_pattern(p)
        self.assertEqual(2, m.size())
        self.assertEqual(0, m.get(0, 1))
        self.assertEqual(1, m.get(1, 0))

    def test_build_matrix_from_matrices(self):
        m1 = Matrix.from_pattern('../#.')
        m2 = Matrix.from_pattern('##/..')
        m3 = Matrix.from_pattern('../##')
        m4 = Matrix.from_pattern('../..')
        m = Matrix.from_matrices([m1, m2, m3, m4])
        self.assertEqual(4, m.size())
        self.assertEqual(0, m.get(0, 0))
        self.assertEqual(1, m.get(1, 0))
        self.assertEqual(1, m.get(0, 2))
        self.assertEqual('..##/#.../..../##..', str(m))

    def test_matrix_split(self):
        m = Matrix.from_pattern('..##/#.../..../##..')
        m1, m2, m3, m4 = m.split(2)
        self.assertEqual('../#.', str(m1))
        self.assertEqual('##/..', str(m2))
        self.assertEqual('../##', str(m3))
        self.assertEqual('../..', str(m4))

    def test_matrix_sum(self):
        m = Matrix.from_pattern('..##/#.../..../##..')
        self.assertEqual(5, m.sum())

    def test_matrix_transformations(self):
        m = Matrix.from_pattern('..#/#../###')
        self.assertEqual('##./#../#.#', str(m.rotate()))
        self.assertEqual('#../..#/###', str(m.flip_left()))
        self.assertEqual('###/#../..#', str(m.flip_up()))

    def test_build_rule_from_str(self):
        s = '../.# => ##./#../...'
        rule = Rule.from_str(s)
        self.assertEqual(6, len(rule.patterns))
        self.assertEqual(2, rule.size())
        self.assertEqual(3, rule.output.size())

    def test_run_fractal_program(self):
        fractal = FractalProgram('day_21.test')
        matrix = fractal.run(2)
        self.assertEqual(12, matrix.sum())


class Rule(object):

    def __init__(self, pattern, output):
        first = Matrix.from_pattern(pattern)
        self.patterns = [first]
        for _ in range(3):
            self.patterns.append(self.patterns[-1].rotate())
        self.patterns.append(first.flip_left())
        self.patterns.append(first.flip_up())
        self.output = Matrix.from_pattern(output)

    def match(self, matrix):
        if self.size() != matrix.size():
            return False
        for p in self.patterns:
            if p == matrix:
                return True
        return False

    def size(self):
        return self.patterns[0].size()

    @staticmethod
    def from_str(s):
        pattern, output = s.split(' => ')
        return Rule(pattern, output)

    def __str__(self):
        return '%s -> %s ' % (' | '.join([str(p) for p in self.patterns]), self.output)


class FractalProgram(object):

    def __init__(self, filename):
        with open(filename, 'r') as infile:
            self.rules = []
            for line in infile:
                self.rules.append(Rule.from_str(line))

    def run(self, iterations):
        matrix = Matrix.from_pattern('.#./..#/###')
        for _ in range(iterations):
            if matrix.size() % 2 == 0:
                in_matrices = matrix.split(2)
            else:
                in_matrices = matrix.split(3)
            out_matrices = []
            for m in in_matrices:
                for r in self.rules:
                    if r.match(m):
                        out_matrices.append(r.output)
                        break
            matrix = Matrix.from_matrices(out_matrices)
        return matrix


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            program = FractalProgram(name)
            matrix = program.run(5)
            print('%s -> %d', matrix.sum())
        pass
    else:
        unittest.main()
