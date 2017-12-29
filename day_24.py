# Solution to http://adventofcode.com/2017/day/24

import unittest
import sys
import operator


class Component(object):

    def __init__(self, ident, in_pins, out_pins):
        self.ident = ident
        self.in_pins = in_pins
        self.out_pins = out_pins

    def __str__(self) -> str:
        return '%d/%d' % (self.in_pins, self.out_pins)

    def __eq__(self, other):
        return self.ident == other.ident

    def __hash__(self):
        return hash(self.ident)


class Bridge(object):

    def __init__(self, components=None, strength=0):
        self.components = components
        self.strength = strength

    def extend(self, c):
        tail = self.components[-1]
        ext = None
        if tail.out_pins == c.in_pins:
            ext = Component(c.ident, c.in_pins, c.out_pins)
        elif tail.out_pins == c.out_pins:
            ext = Component(c.ident, c.out_pins, c.in_pins)
        if ext:
            components = self.components[:]
            components.append(ext)
            strength = self.strength + ext.in_pins + ext.out_pins
            return Bridge(components, strength)
        return None

    def __str__(self):
        cs = [str(c) for c in self.components]
        return '%s | %d' % ('->'.join(cs), self.strength)

    def __len__(self):
        return len(self.components)


def load_components(filename):
    with open(filename, 'r') as infile:
        result = []
        for ident, line in enumerate(infile):
            in_pins, out_pins = map(int, line.split('/'))
            result.append(Component(ident, in_pins, out_pins))
        return result


def strongest_bridge(components):
    b = Bridge([Component(0, 0, 0)], 0)
    cs = frozenset(components)
    return _strongest_bridge(b, cs)


def _strongest_bridge(b, cs):
    results = [b.strength]
    for c in cs:
        new_b = b.extend(c)
        if new_b:
            new_cs = cs - frozenset([c])
            results.append(_strongest_bridge(new_b, new_cs))
    return max(results)


def longest_strongest_bridge(components):
    b = Bridge([Component(0, 0, 0)], 0)
    cs = frozenset(components)
    return _longest_strongest_bridge(b, cs)


def _longest_strongest_bridge(b, cs):
    results = [(len(b), b.strength)]
    for c in cs:
        new_b = b.extend(c)
        if new_b:
            new_cs = cs - frozenset([c])
            results.append(_longest_strongest_bridge(new_b, new_cs))
    m = max(results, key=operator.itemgetter(0))
    for x in results:
        if x[0] == m[0] and x[1] > m[1]:
            m = x
    return m


class Test(unittest.TestCase):

    def setUp(self):
        self.test_data = load_components('day_24.test')

    def test_build_bridge(self):
        b = Bridge([Component(0, 0, 0)], 0)
        c1 = Component(0, 0, 2)
        c2 = Component(1, 2, 3)
        c3 = Component(2, 5, 3)
        c4 = Component(3, 3, 7)
        b = b.extend(c1)
        self.assertTrue(b)
        b = b.extend(c2)
        self.assertTrue(b)
        b = b.extend(c3)
        self.assertTrue(b)
        self.assertFalse(b.extend(c4))
        self.assertEqual(4, len(b))
        self.assertEqual(15, b.strength)

    def test_load_components(self):
        self.assertEqual(8, len(self.test_data))
        self.assertEqual(Component(0, 0, 2), self.test_data[0])
        self.assertEqual(Component(7, 9, 10), self.test_data[-1])

    def test_strongest_bridge(self):
        self.assertEqual(31, strongest_bridge(self.test_data))

    def test_longest_strongest_bridge(self):
        self.assertEqual((5, 19), longest_strongest_bridge(self.test_data))


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            components = load_components(name)
            print('%s -> %d %s' %
                  (name,
                   strongest_bridge(components),
                   longest_strongest_bridge(components)))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
