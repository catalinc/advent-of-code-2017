# Solution to http://adventofcode.com/2017/day/18

import unittest
import sys
import collections

Instruction = collections.namedtuple('Instruction', 'code, op1, op2')


class Program(object):

    def __init__(self):
        self.instructions = []

    def load(self, fname):
        with open(fname, 'r') as infile:
            for line in infile:
                tokens = line.split(' ')
                code = tokens[0]
                op1 = tokens[1]
                op2 = 0
                if len(tokens) == 3:
                    op2 = tokens[2]
                self.instructions.append(Instruction(
                    code=code, op1=op1, op2=op2))


class SoundVm(object):

    def __init__(self):
        self.registers = collections.defaultdict(int)
        self.pc = 0
        self.last_sound = -1

    def run(self, program):
        self.reset()
        for instr in program.instructions:
            jump = 1
            if instr.code == 'set':
                self.registers[instr.op1] = self._value(instr.op2)
            elif instr.code == 'add':
                self.registers[instr.op1] += self._value(instr.op2)
            elif instr.code == 'mul':
                self.registers[instr.op1] *= self._value(instr.op2)
            elif instr.code == 'mod':
                self.registers[instr.op1] %= self._value(instr.op2)
            elif instr.code == 'jgz':
                cond = self._value(instr.op1)
                if cond > 0:
                    jump = self._value(instr.op2)
            elif instr.code == 'snd':
                freq = self._value(instr.op1)
                if freq > 0:
                    self.last_sound = freq
            self.pc += jump
            if self.pc < 0 or self.pc >= len(program.instructions):
                return self.last_sound

    def _value(self, s):
        if 'a' <= s <= 'z':
            return self.registers[s]
        return int(s)

    def reset(self):
        self.registers.clear()
        self.pc = 0
        self.last_sound = -1


class Test(unittest.TestCase):

    def test_load_program(self):
        p = Program()
        p.load('day_18.test')
        self.assertEqual(10, len(p.instructions))
        first = Instruction(code='set', op1='a', op2='1')
        self.assertEqual(first, p.instructions[0])


def main():
    if len(sys.argv) >= 2:
        vm = SoundVm()
        for fname in sys.argv[1:]:
            p = Program()
            p.load(fname)
            print("%s -> %d" % (fname, vm.run(p)))


if __name__ == '__main__':
    main()
