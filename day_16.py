# Solution to http://adventofcode.com/2017/day/16

import unittest
import sys
import string
import time
from datetime import timedelta


def timing(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print("%s took %s" % (fn.__name__, timedelta(seconds=end - start)))
        return result
    return wrapper


class ProgramGroup(object):

    def __init__(self, size):
        self.programs = list(string.ascii_lowercase[0:size])

    def dance(self, moves, repeat=1):
        moves = [self._decode(m) for m in moves]
        size = len(self.programs)
        for _ in range(repeat):
            for move in moves:
                if move[0] == 's':
                    i = move[1]
                    self.programs = self.programs[-i:] + \
                        self.programs[0:size - i]
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

    def _decode(self, move):
        if move[0] == 's':
            return ('s', int(move[1:]))
        elif move[0] == 'x':
            k = move.index('/')
            i = int(move[1:k])
            j = int(move[k + 1:])
            return ('x', i, j)
        elif move[0] == 'p':
            k = move.index('/')
            a = move[1:k]
            b = move[k + 1:]
            return ('p', a, b)

    def __str__(self):
        return ''.join(self.programs)


class Test(unittest.TestCase):

    def test_dance(self):
        pg = ProgramGroup(5)
        moves = ['s1', 'x3/4', 'pe/b']
        pg.dance(moves)
        self.assertEqual('baedc', str(pg))


def main():
    if len(sys.argv) >= 2:
        for fname in sys.argv[1:]:
            with open(fname, 'r') as infile:
                moves = []
                for line in infile:
                    moves.extend(line.split(','))
                pg = ProgramGroup(16)
                pg.dance(moves)
                print("'%s' after first dance -> %s" % (fname, pg))
                k = 1000000000
                pg.dance(moves, repeat=k)
                print("'%s' after %d dances -> %s" % (fname, k, pg))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
