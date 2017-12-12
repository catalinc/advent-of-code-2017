# Solution to http://adventofcode.com/2017/day/12

import unittest
import sys
import collections
import re


class Graph(object):

    def __init__(self):
        self.nodes = collections.defaultdict(set)

    def add_node(self, node, connected):
        for n in connected:
            self.nodes[node].add(n)
            self.nodes[n].add(node)

    def reachable(self, node):
        explored = set()
        to_explore = [node]
        while to_explore:
            current = to_explore.pop(0)
            explored.add(current)
            for n in self.nodes[current]:
                if not n in explored:
                    to_explore.append(n)
        return explored

    def count_groups(self):
        count = 0
        group = self.reachable(0)
        to_explore = set(self.nodes.keys()) - group
        count += 1
        while to_explore:
            node = self._pick(to_explore)
            to_explore = to_explore - self.reachable(node)
            count += 1
        return count

    def _pick(self, group):
        for e in group:
            return e


def parse_node(s):
    tokens = re.split(' |,', s)
    return int(tokens[0]), [int(t) for t in tokens[2:] if len(t) > 0]


class Test(unittest.TestCase):

    def test_parse_node(self):
        node, connected = parse_node('0 <-> 1, 2')
        self.assertEqual(0, node)
        self.assertEqual([1, 2], connected)

    def test_node_group(self):
        g = Graph()
        test_data = ('0 <-> 2',
                     '1 <-> 1',
                     '2 <-> 0, 3, 4',
                     '3 <-> 2, 4',
                     '4 <-> 2, 3, 6',
                     '5 <-> 6',
                     '6 <-> 4, 5')
        for s in test_data:
            g.add_node(*parse_node(s))

        group = g.reachable(0)
        self.assertEqual(set([0, 2, 3, 4, 5, 6]), set(group))
        self.assertEqual(set([1]), g.reachable(1))
        self.assertEqual(2, g.count_groups())


def main():
    if len(sys.argv) >= 2:
        for fname in sys.argv[1:]:
            with open(fname, 'r') as infile:
                g = Graph()
                for line in infile:
                    g.add_node(*parse_node(line))
                print('%s -> %d %d' % (fname, len(g.reachable(0)), g.count_groups()))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
