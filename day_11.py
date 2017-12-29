# Solution to http://adventofcode.com/2017/day/11

import unittest
import sys


class Cube(object):
    DIRECTIONS = {
        'n': (0, 1, -1),
        'ne': (1, 0, -1),
        'se': (1, -1, 0),
        's': (0, -1, 1),
        'sw': (-1, 0, 1),
        'nw': (-1, 1, 0)
    }

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def move(self, direction):
        c = Cube.DIRECTIONS[direction]
        self.x += c[0]
        self.y += c[1]
        self.z += c[2]

    def distance(self, other):
        return max(abs(self.x - other.x),
                   abs(self.y - other.y),
                   abs(self.z - other.z))


class HexWalker(object):

    def __init__(self):
        self.hex = Cube(0, 0, 0)
        self.furthest = 0

    def walk(self, directions):
        for direction in directions.split(','):
            self.hex.move(direction)
            steps = self.steps()
            if steps > self.furthest:
                self.furthest = steps

    def steps(self):
        return self.hex.distance(Cube(0, 0, 0))


class Test(unittest.TestCase):

    def test_steps(self):
        test_data = [('ne,ne,ne', 3),
                     ('ne,ne,sw,sw', 0),
                     ('ne,ne,s,s', 2),
                     ('se,sw,se,sw,sw', 3)]
        for directions, steps in test_data:
            walker = HexWalker()
            walker.walk(directions)
            self.assertEqual(steps, walker.steps())


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            with open(name, 'r') as infile:
                walker = HexWalker()
                for directions in infile:
                    walker.walk(directions)
                print("'%s' -> %d %d" % (name, walker.steps(), walker.furthest))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
