# Solution to http://adventofcode.com/2017/day/23

import collections
import sys
import unittest

Instruction = collections.namedtuple('Instruction', 'code, op1, op2')


class Cpu(object):

    def __init__(self):
        self.pc = 0
        self.registers = collections.defaultdict(int)
        self.stats = collections.defaultdict(int)

    def run(self, instructions):
        size = len(instructions)
        while 0 <= self.pc < size:
            instr = instructions[self.pc]
            jump = 1
            self.stats[instr.code] += 1
            if instr.code == 'set':
                self.registers[instr.op1] = self._value(instr.op2)
            elif instr.code == 'sub':
                self.registers[instr.op1] -= self._value(instr.op2)
            elif instr.code == 'mul':
                self.registers[instr.op1] *= self._value(instr.op2)
            elif instr.code == 'jnz':
                cond = self._value(instr.op1)
                if cond != 0:
                    jump = self._value(instr.op2)
            self.pc += jump

    def _value(self, s):
        if 'a' <= s <= 'z':
            return self.registers[s]
        return int(s)

    def __str__(self):
        return 'pc=%d registers={%s} stats={%s}' % \
               (self.pc, self.registers, self.stats)


def load_instructions(filename):
    with open(filename, 'r') as infile:
        instructions = []
        for line in infile:
            line = line.rstrip()
            code, op1, op2 = line.split(' ')
            instructions.append(Instruction(code=code, op1=op1, op2=op2))
        return instructions


class Test(unittest.TestCase):

    def setUp(self):
        self.instructions = load_instructions('day_23.test')

    def test_load_instructions(self):
        self.assertEqual(6, len(self.instructions))
        second = Instruction('sub', 'a', '1')
        self.assertEqual(second, self.instructions[1])

    def test_cpu_run(self):
        cpu = Cpu()
        cpu.run(self.instructions)
        self.assertEqual(8, cpu.registers['a'])
        self.assertEqual(64, cpu.registers['b'])
        self.assertEqual(2, cpu.stats['mul'])


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            cpu = Cpu()
            cpu.registers['a'] = 1  # part 2
            cpu.run(load_instructions(name))
            print("%s -> %s" % (name, cpu))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
