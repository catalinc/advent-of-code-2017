# Solution to http://adventofcode.com/2017/day/21


class Matrix(object):

    def __init__(self, size=0):
        self.data = [[0 for _ in range(size)] for _ in range(size)]

    @staticmethod
    def load_from_pattern(pattern):
        result = Matrix()
        result.data = [[1 if c == '#' else 0 for c in r]
                  for r in pattern.split('/')]
        return result

    def size(self):
        return len(self.data)

    def split(self, matrix_size):
        result = []
        for r in range(0, self.size() - matrix_size, matrix_size):
            for c in range(0, self.size() - matrix_size, matrix_size):
                m = Matrix(matrix_size)
                for i in range(matrix_size):
                    for j in range(matrix_size):
                        m.data[i][j] = self.data[r + i][c + j]
                result.append(m)
        return result

    @staticmethod
    def load_from_matrices(matrices):
        matrix_size = matrices[0].size()
        result = Matrix(matrix_size * 2)
        for i, m in enumerate(matrices):
            for r in range(i, i + matrix_size):
                for c in range(i, i + matrix_size):
                    pass
        return result

    def __eq__(self, other):
        return self.data == other.data


class Rule(object):

    def __init__(self, pattern, output):
        self.pattern = Matrix.load_from_pattern(pattern)
        self.output = Matrix.load_from_pattern(output)

    def match(self, matrix):
        return True
