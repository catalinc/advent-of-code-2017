# Solution to http://adventofcode.com/2017/day/25

import unittest
import sys


class TuringMachine(object):

    def __init__(self, states, initial):
        self.tape = [0]
        self.cursor = 0
        self.states = states
        self.current = initial

    def step(self):
        value, action, next_ = self.states[self.current][self.read()]
        self.write(value)
        if action == 'R':
            self.move_cursor_right()
        else:
            self.move_cursor_left()
        self.current = next_

    def move_cursor_left(self):
        self.cursor -= 1
        if self.cursor == -1:
            self.tape.insert(0, 0)
            self.cursor = 0

    def move_cursor_right(self):
        self.cursor += 1
        if self.cursor == len(self.tape):
            self.tape.append(0)

    def write(self, v):
        self.tape[self.cursor] = v

    def read(self):
        return self.tape[self.cursor]

    def checksum(self):
        return sum(self.tape)


class Test(unittest.TestCase):

    def test_turing_machine(self):
        states = {'A': {0: (1, 'R', 'B'), 1: (0, 'L', 'B')},
                  'B': {0: (1, 'L', 'A'), 1: (1, 'R', 'A')}}
        tm = TuringMachine(states, 'A')
        for _ in range(6):
            tm.step()
        self.assertEqual(3, tm.checksum())


def main():
    if len(sys.argv) == 2 and sys.argv[1] == '-run':
        initial = 'A'
        steps = 12368930
        states = {'A': {0: (1, 'R', 'B'), 1: (0, 'R', 'C')},
                  'B': {0: (0, 'L', 'A'), 1: (0, 'R', 'D')},
                  'C': {0: (1, 'R', 'D'), 1: (1, 'R', 'A')},
                  'D': {0: (1, 'L', 'E'), 1: (0, 'L', 'D')},
                  'E': {0: (1, 'R', 'F'), 1: (1, 'L', 'B')},
                  'F': {0: (1, 'R', 'A'), 1: (1, 'R', 'E')}}
        tm = TuringMachine(states, initial)
        for _ in range(steps):
            tm.step()
        print(tm.checksum())
    else:
        unittest.main()


if __name__ == '__main__':
    main()
