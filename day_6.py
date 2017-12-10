# Solution to http://adventofcode.com/2017/day/6

import unittest
import sys


def reallocation_cycles(mem):
    count = 0
    history = make_history()
    while True:
        cycle = record_memory(mem, history, count)
        if cycle is not None:
            return count - cycle, count
        bank = find_bank_to_redistribute(mem)
        redistribute_bank(bank, mem)
        count += 1


def make_history():
    return {'hashes': set(), 'cycles': {}}


def find_bank_to_redistribute(mem):
    bank, max_blocks = 0, mem[0]
    for i, blocks in enumerate(mem):
        if blocks > max_blocks:
            bank = i
            max_blocks = blocks
    return bank


def redistribute_bank(bank, mem):
    blocks = mem[bank]
    mem[bank] = 0
    i = bank + 1
    while blocks:
        i = i % len(mem)
        mem[i] += 1
        blocks -= 1
        i += 1


def record_memory(mem, history, count):
    h = mem_hash(mem)
    if h in history['hashes']:
        return history['cycles'][h]
    history['hashes'].add(h)
    history['cycles'][h] = count
    return None


def mem_hash(mem):
    h = 0
    for n in mem:
        h = h * 17 + n
    return h


class Test(unittest.TestCase):

    def test_find_bank_to_redistribute(self):
        mem = [0, 2, 7, 0]
        self.assertEqual(2, find_bank_to_redistribute(mem))

    def test_redistribute_bank(self):
        mem = [0, 2, 7, 0]
        redistribute_bank(2, mem)
        self.assertEqual([2, 4, 1, 2], mem)

    def test_record_memory(self):
        mem = [0, 2, 7, 0]
        history = make_history()
        self.assertEqual(None, record_memory(mem, history, 0))
        self.assertEqual(0, record_memory(mem, history, 1))
        mem = [1, 2, 3, 4]
        self.assertEqual(None, record_memory(mem, history, 2))
        self.assertEqual(2, len(history['hashes']))

    def test_reallocation_cycles(self):
        self.assertEqual((4, 5), reallocation_cycles([0, 2, 7, 0]))


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == '-run':
        print(reallocation_cycles(
            [4, 10, 4, 1, 8, 4, 9, 14, 5, 1, 14, 15, 0, 15, 3, 5]))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
