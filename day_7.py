# Solution to http://adventofcode.com/2017/day/7

import unittest
import sys
import collections


class Tower(object):

    def __init__(self):
        self.programs = {}

    def put_program(self, program):
        if program.name in self.programs:
            existing = self.programs[program.name]
            if program.weight:
                existing.weight = program.weight
                existing.total_weight = program.weight
            if program.parent:
                existing.parent = program.parent
            if program.children:
                existing.children = program.children
        else:
            self.programs[program.name] = program

    def parse_program(self, s):
        tokens = s.split()
        name, weight, children = tokens[0], int(tokens[1][1:-1]), []
        if len(tokens) > 3:
            children = [token.rstrip(',') for token in tokens[3:]]
        program = Program(name=name, weight=weight, children=children)
        self.put_program(program)
        for child_name in program.children:
            child = Program(name=child_name, parent=program.name)
            self.put_program(child)

    def root_program(self):
        for program in self.programs.values():
            if program.parent is None:
                return program

    def compute_total_weights(self):
        root = str(self.root_program())
        return self._compute_total_weights(root)

    def _compute_total_weights(self, name):
        program = self.programs[name]
        for child_name in program.children:
            program.total_weight += self._compute_total_weights(child_name)
        return program.total_weight

    def balanced_weight(self):
        children = self.children(self.root_program())
        weights = [child.total_weight for child in children]
        counter = collections.Counter(weights)
        balanced, unbalanced = counter.most_common()
        diff = balanced[0] - unbalanced[0]
        if diff != 0:
            return self._balanced_weight(self.root_program(), diff)
        else:
            return 0

    def _balanced_weight(self, program, diff):
        children = self.children(program)
        weights = [child.total_weight for child in children]
        if weights:
            d = max(weights) - min(weights)
            if d != 0:
                counter = collections.Counter(weights)
                balanced, unbalanced = counter.most_common()
                unbalanced = unbalanced[0]
                for child in children:
                    if child.total_weight == unbalanced:
                        return self._balanced_weight(child, diff)
        return program.weight + diff

    def children(self, program):
        return [self.programs[name] for name in program.children]


class Program(object):

    def __init__(self, name, weight=0, parent=None, children=None):
        self.name = name
        self.weight = weight
        self.parent = parent
        self.children = set(children or [])
        self.total_weight = weight

    def __str__(self):
        return self.name


class Test(unittest.TestCase):

    def test_build_tower(self):
        tower = Tower()
        test_data = ["ktlj (57)", "fwft (72) -> ktlj, cntj", "cntj (47)"]
        for s in test_data:
            tower.parse_program(s)

        tower.compute_total_weights()

        self.assertEqual(3, len(tower.programs))

        ktlj = tower.programs['ktlj']
        self.assertEqual("fwft", ktlj.parent)
        self.assertEqual(0, len(ktlj.children))
        self.assertEqual(57, ktlj.weight)

        cntj = tower.programs['cntj']
        self.assertEqual("fwft", cntj.parent)
        self.assertEqual(0, len(cntj.children))
        self.assertEqual(47, cntj.weight)

        fwft = tower.programs['fwft']
        self.assertEqual(None, fwft.parent)
        self.assertEqual(2, len(fwft.children))
        self.assertTrue('cntj' in fwft.children)
        self.assertTrue('ktlj' in fwft.children)
        self.assertEqual(72, fwft.weight)
        self.assertEqual(176, fwft.total_weight)

        self.assertEqual('fwft', str(tower.root_program()))

    def test_unbalanced_tower(self):
        test_data = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""
        tower = Tower()
        for line in test_data.split('\n'):
            tower.parse_program(line)

        tower.compute_total_weights()

        root = tower.root_program()
        self.assertEqual('tknk', str(root))
        self.assertEqual(3, len(root.children))

        ugml = tower.programs['ugml']
        self.assertEqual(251, ugml.total_weight)

        padx = tower.programs['padx']
        self.assertEqual(243, padx.total_weight)

        fwft = tower.programs['fwft']
        self.assertEqual(243, fwft.total_weight)

        self.assertEqual('tknk', str(fwft.parent))
        self.assertEqual(251 + 243 + 243 + 41, root.total_weight)

        self.assertEqual(60, tower.balanced_weight())


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            with open(name, 'r') as infile:
                tower = Tower()
                for line in infile:
                    tower.parse_program(line)
                tower.compute_total_weights()
                print('%s -> %s %d' % (name, tower.root_program(), tower.balanced_weight()))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
