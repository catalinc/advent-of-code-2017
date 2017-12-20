# Solution to http://adventofcode.com/2017/day/18

import unittest
import sys
import collections

Instruction = collections.namedtuple('Instruction', 'code, op1, op2')


class Program(object):
    RUNNING = 0
    WAITING_FOR_IO = 1
    TERMINATED = 2

    def __init__(self, pid, filename):
        self.pc = 0
        self.instructions = []
        self.pid = pid
        self.registers = collections.defaultdict(int)
        self.registers['p'] = pid
        self.inbox = []
        self.outbox = []
        self.state = Program.RUNNING
        with open(filename, 'r') as infile:
            for line in infile:
                line = line.rstrip()
                tokens = line.split(' ')
                code = tokens[0]
                op1 = tokens[1]
                op2 = 0
                if len(tokens) == 3:
                    op2 = tokens[2]
                self.instructions.append(Instruction(code=code, op1=op1, op2=op2))

    def run(self):
        if 0 <= self.pc < len(self.instructions):
            self.state = Program.RUNNING
            instr = self.instructions[self.pc]
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
                v = self._value(instr.op1)
                self.outbox.append(v)
            elif instr.code == 'rcv':
                if self.inbox:
                    v = self.inbox.pop(0)
                    r = instr.op1
                    self.registers[r] = v
                else:
                    jump = 0
                    self.state = Program.WAITING_FOR_IO
            self.pc += jump
        else:
            self.state = Program.TERMINATED

    def _value(self, s):
        if 'a' <= s <= 'z':
            return self.registers[s]
        return int(s)


class System(object):

    def __init__(self, filename):
        self.program_0 = Program(0, filename)
        self.program_1 = Program(1, filename)

    def run(self):
        pass

class Test(unittest.TestCase):

    def test_load_program(self):
        p = Program()
        p.load('day_18.test')
        self.assertEqual(10, len(p.instructions))
        first = Instruction(code='set', op1='a', op2='1')
        self.assertEqual(first, p.instructions[0])

    def test_run_program(self):
        p = Program()
        p.load('day_18.test')
        vm = Program()
        self.assertEqual(4, vm.run(p))


def main():
    if len(sys.argv) >= 2:
        vm = Program()
        for fname in sys.argv[1:]:
            p = Program()
            p.load(fname)
            print("%s -> %d" % (fname, vm.run(p)))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
