# Solution to http://adventofcode.com/2017/day/16

import string
import unittest
import sys


class ProgramGroup(object):

    def __init__(self, size):
        self.programs = list(string.ascii_lowercase[0:size])

    def dance(self, moves, repeat=1):
        moves = [self._decode(m) for m in moves]
        seen = []
        for k in range(repeat):
            s = ''.join(self.programs)
            if s in seen:
                return seen[repeat % k]
            seen.append(s)
            for move in moves:
                if move[0] == 's':
                    i = move[1]
                    self.programs = self.programs[-i:] + self.programs[:-i]
                elif move[0] == 'x':
                    i = move[1]
                    j = move[2]
                    self.programs[i], self.programs[j] = self.programs[j], self.programs[i]
                elif move[0] == 'p':
                    a = move[1]
                    b = move[2]
                    i = self.programs.index(a)
                    j = self.programs.index(b)
                    self.programs[i], self.programs[j] = self.programs[j], self.programs[i]
        return ''.join(self.programs)

    @staticmethod
    def _decode(move):
        if move[0] == 's':
            return 's', int(move[1:])
        elif move[0] == 'x':
            k = move.index('/')
            i = int(move[1:k])
            j = int(move[k + 1:])
            return 'x', i, j
        elif move[0] == 'p':
            k = move.index('/')
            a = move[1:k]
            b = move[k + 1:]
            return 'p', a, b

    def __str__(self):
        return ''.join(self.programs)


class Test(unittest.TestCase):

    def test_dance(self):
        pg = ProgramGroup(5)
        moves = ['s1', 'x3/4', 'pe/b']
        d = pg.dance(moves)
        self.assertEqual('baedc', d)


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            with open(name, 'r') as infile:
                moves = []
                for line in infile:
                    moves.extend(line.split(','))
                pg = ProgramGroup(16)
                k = 1000000000
                d = pg.dance(moves, repeat=k)
                print("'%s' after %d dances -> %s" % (name, k, d))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
