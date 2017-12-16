# Solution to http://adventofcode.com/2017/day/16

import unittest
import sys
import string


class ProgramGroup(object):

    def __init__(self, size):
        self.programs = list(string.ascii_lowercase[0:size])

    def dance(self, move):
        if move[0] == 's':
            n = int(move[1:])
            self.spin(n)
        elif move[0] == 'x':
            k = move.index('/')
            i = int(move[1:k])
            j = int(move[k + 1:])
            self.exchange(i, j)
        elif move[0] == 'p':
            k = move.index('/')
            a = move[1:k]
            b = move[k + 1:]
            self.partner(a, b)

    def spin(self, n):
        size = len(self.programs)
        self.programs = self.programs[-n:] + self.programs[0:size - n]

    def exchange(self, i, j):
        self.programs[i], self.programs[j] = self.programs[j], self.programs[i]

    def partner(self, a, b):
        i = self.programs.index(a)
        j = self.programs.index(b)
        self.exchange(i, j)

    def __str__(self):
        return ''.join(self.programs)


class Test(unittest.TestCase):

    def test_dance(self):
        pg = ProgramGroup(5)
        moves = [('s1', 'eabcd'), ('x3/4', 'eabdc'), ('pe/b', 'baedc')]
        for m, e in moves:
            pg.dance(m)
            self.assertEqual(e, str(pg))


def main():
    if len(sys.argv) >= 2:
        for fname in sys.argv[1:]:
            with open(fname, 'r') as infile:
                pg = ProgramGroup(16)
                moves = []
                for line in infile:
                    moves.extend(line.split(','))
                for move in moves:
                    pg.dance(move)
                print("'%s' -> %s" % (fname, pg))
                for _ in range(1000000000):
                    for move in moves:
                        pg.dance(move)                    
                print("'%s' -> %s" % (fname, pg))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
