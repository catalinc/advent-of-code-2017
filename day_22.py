# Solution to http://adventofcode.com/2017/day/22

import collections
import unittest
import sys


class Grid(object):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3

    def __init__(self):
        self.nodes = collections.defaultdict(lambda: Grid.CLEAN)

    def set(self, x, y, v):
        self.nodes[(x, y)] = v

    def get(self, x, y):
        return self.nodes[(x, y)]

    def center(self):
        max_x = max((x for x, _ in self.nodes))
        max_y = max((y for _, y in self.nodes))
        return max_x // 2, max_y // 2


Direction = collections.namedtuple('Direction', 'name, dx, dy')


class Virus(object):
    UP = Direction('U', 0, -1)
    DOWN = Direction('D', 0, 1)
    RIGHT = Direction('R', 1, 0)
    LEFT = Direction('L', -1, 0)

    RIGHT_TURNS = {UP.name: RIGHT,
                   DOWN.name: LEFT,
                   RIGHT.name: DOWN,
                   LEFT.name: UP}

    LEFT_TURNS = {UP.name: LEFT,
                  DOWN.name: RIGHT,
                  RIGHT.name: UP,
                  LEFT.name: DOWN}

    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.direction = Virus.UP
        self.infections = 0

    def burst(self):
        state = self.grid.get(self.x, self.y)
        if state == Grid.INFECTED:
            self.turn_right()
            self.mark(Grid.CLEAN)
        else:
            self.turn_left()
            self.mark(Grid.INFECTED)
            self.infections += 1
        self.move_forward()

    def turn_right(self):
        self.direction = Virus.RIGHT_TURNS[self.direction.name]

    def turn_left(self):
        self.direction = Virus.LEFT_TURNS[self.direction.name]

    def mark(self, state):
        self.grid.set(self.x, self.y, state)

    def move_forward(self):
        self.x += self.direction.dx
        self.y += self.direction.dy


def parse_grid(filename):
    with open(filename, 'r') as infile:
        grid = Grid()
        for y, line in enumerate(infile):
            for x, ch in enumerate(line):
                grid.set(x, y, Grid.INFECTED if ch == '#' else Grid.CLEAN)
        return grid


class MutatedVirus(Virus):
    REVERSE_DIRECTIONS = {Virus.UP.name: Virus.DOWN,
                          Virus.DOWN.name: Virus.UP,
                          Virus.RIGHT.name: Virus.LEFT,
                          Virus.LEFT.name: Virus.RIGHT}

    def __init__(self, x, y, grid):
        super().__init__(x, y, grid)

    def burst(self):
        state = self.grid.get(self.x, self.y)
        if state == Grid.CLEAN:
            self.mark(Grid.WEAKENED)
            self.turn_left()
        elif state == Grid.WEAKENED:
            self.mark(Grid.INFECTED)
            self.infections += 1
        elif state == Grid.INFECTED:
            self.turn_right()
            self.mark(Grid.FLAGGED)
        elif state == Grid.FLAGGED:
            self.reverse_direction()
            self.mark(Grid.CLEAN)
        self.move_forward()

    def reverse_direction(self):
        self.direction = MutatedVirus.REVERSE_DIRECTIONS[self.direction.name]


class Test(unittest.TestCase):

    def setUp(self):
        self.grid = parse_grid('day_22.test')
        self.start_x, self.start_y = self.grid.center()

    def test_infection_simple_virus(self):
        virus = Virus(self.start_x, self.start_y, self.grid)
        for _ in range(10_000):
            virus.burst()
        self.assertEqual(5587, virus.infections)

    def test_infection_mutated_virus(self):
        virus = MutatedVirus(self.start_x, self.start_y, self.grid)
        for _ in range(100):
            virus.burst()
        self.assertEqual(26, virus.infections)


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            grid = parse_grid(name)
            x, y = grid.center()
            virus = MutatedVirus(x, y, grid)  # Virus(x, y, grid)
            for _ in range(10_000_000):
                virus.burst()
            print('%s -> %d' % (name, virus.infections))


if __name__ == '__main__':
    main()
