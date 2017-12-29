# Solution to https://adventofcode.com/2017/day/5

import unittest
import sys


def count_jumps(program, max_offset=0):
    jumps, pc = 0, 0
    while 0 <= pc < len(program):
        offset = program[pc]
        if not max_offset:
            program[pc] += 1
        else:
            if abs(offset) >= max_offset:
                if offset > 0:
                    program[pc] -= 1
                else:
                    program[pc] += 1
            else:
                program[pc] += 1
        pc += offset
        jumps += 1
    return jumps


def load_program(name):
    program = []
    with open(name, 'r') as infile:
        for line in infile:
            program.append(int(line))
    return program


class Test(unittest.TestCase):

    def test_count_jumps(self):
        test_program = [0, 3, 0, 1, -3]
        self.assertEqual(5, count_jumps(test_program))
        test_program = [0, 3, 0, 1, -3]
        self.assertEqual(10, count_jumps(test_program, max_offset=3))


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            program = load_program(name)
            print("program '%s' -> %d" % (name, count_jumps(program, max_offset=3)))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
