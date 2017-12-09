# Solution to http://adventofcode.com/2017/day/8

import unittest
import collections
import sys

operator_map = {'>': (lambda x, y: x > y),
                '<': (lambda x, y: x < y),
                '<=': (lambda x, y: x <= y),
                '>=': (lambda x, y: x >= y),
                '!=': (lambda x, y: x != y),
                '==': (lambda x, y: x == y),
                'inc': (lambda x, y: x + y),
                'dec': (lambda x, y: x - y)}


class CPU(object):
    def __init__(self):
        self.registers = collections.defaultdict(int)
        self.max_ever = None

    def execute(self, instruction):
        tokens = instruction.split()
        name = tokens[0]
        operation = operator_map[tokens[1]]
        value = int(tokens[2])
        left = self._value(tokens[4])
        condition = operator_map[tokens[5]]
        right = self._value(tokens[6])
        if condition(left, right):
            self.registers[name] = operation(self.registers[name], value)
            if self.max_ever is None or self.max_ever < self.registers[name]:
                self.max_ever = self.registers[name]

    def _value(self, identifier):
        try:
            return int(identifier)
        except ValueError:
            return self.registers[identifier]

    def get(self, name):
        return self.registers[name]

    def set(self, name, value):
        self.registers[name] = value
        if self.max_ever is None or self.max_ever < value:
            self.max_ever = value

    def max(self):
        return max(self.registers.itervalues())


class Test(unittest.TestCase):

    def test_execute_simple(self):
        cpu = CPU()
        cpu.set('a', 2)
        cpu.set('b', 3)
        cpu.execute('b inc 5 if a > 1')
        self.assertEqual(8, cpu.get('b'))

    def test_max(self):
        test_data = ('b inc 5 if a > 1',
                     'a inc 1 if b < 5',
                     'c dec -10 if a >= 1',
                     'c inc -20 if c == 10')
        cpu = CPU()
        for instruction in test_data:
            cpu.execute(instruction)
        self.assertEqual(1, cpu.max())
        self.assertEqual(10, cpu.max_ever)


def main():
    if len(sys.argv) >= 2:
        for fname in sys.argv[1:]:
            with open(fname, 'r') as infile:
                cpu = CPU()
                for line in infile:
                    cpu.execute(line)
                print('%s -> %d %d' % (fname, cpu.max(), cpu.max_ever))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
