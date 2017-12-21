# Solution to http://adventofcode.com/2017/day/18

import collections
import sys
import unittest

Instruction = collections.namedtuple('Instruction', 'code, op1, op2')


class Program(object):
    RUNNING = 0
    WAITING_FOR_IO = 1
    TERMINATED = 2

    def __init__(self, pid, inbox, outbox, filename):
        self.pc = 0
        self.instructions = []
        self.pid = pid
        self.registers = collections.defaultdict(int)
        self.registers['p'] = pid
        self.inbox = inbox
        self.outbox = outbox
        self.snd_count = 0
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
                self.snd_count += 1
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

    def terminated(self):
        return self.state == Program.TERMINATED

    def waiting_for_io(self):
        return self.state == Program.WAITING_FOR_IO

    def _value(self, s):
        if 'a' <= s <= 'z':
            return self.registers[s]
        return int(s)

    def __str__(self):
        return "pid=%d pc=%d state=%d snd_count=%d registers=%s" % \
               (self.pid, self.pc, self.state, self.snd_count, self.registers)


class System(object):

    def __init__(self, filename):
        inbox, outbox = [], []
        self.p0 = Program(0, inbox, outbox, filename)
        self.p1 = Program(1, outbox, inbox, filename)

    def run(self):
        while True:
            self.p0.run()
            self.p1.run()
            if self.p0.terminated() or self.p1.terminated():
                break
            if self.p0.waiting_for_io() and self.p1.waiting_for_io():
                break


class Test(unittest.TestCase):

    def test_run_system(self):
        system = System('day_18.test')
        system.run()
        self.assertEqual(3, system.p1.snd_count)


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            system = System(name)
            system.run()
            print("%s -> %s %s" % (name, system.p0, system.p1))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
