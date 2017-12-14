# Solution to http://adventofcode.com/2017/day/13

import unittest
import sys


class Layer(object):

    def __init__(self, depth, size):
        self.depth = depth
        self.size = size
        self.scanner = 0
        self.direction = 1

    def tick(self):
        if self.scanner == 0 and self.direction == -1:
            self.direction = 1
        elif self.scanner == self.size - 1 and self.direction == 1:
            self.direction = -1
        self.scanner = self.scanner + self.direction

    def is_scanner_at_top_after(self, nticks):
        position = self.scanner
        direction = self.direction
        for _ in range(nticks):
            if position == 0 and direction == -1:
                direction = 1
            elif position == self.size - 1 and direction == 1:
                direction = -1
            position += direction
        return position == 0

    def severity(self):
        return self.depth * self.size

    def reset(self):
        self.scanner = 0
        self.direction = 1


class Firewall(object):

    def __init__(self):
        self.layers = {}
        self.max_depth = 0

    def add_layer(self, layer):
        self.layers[layer.depth] = layer
        if layer.depth > self.max_depth:
            self.max_depth = layer.depth

    def get_layer(self, depth):
        return self.layers.get(depth)

    def tick(self):
        for l in self.layers.values():
            l.tick()

    def reset(self):
        for l in self.layers.values():
            l.reset()


class World(object):

    def __init__(self):
        self.packet = -1
        self.firewall = Firewall()
        self.severity = 0

    def tick(self):
        self.packet += 1
        layer = self.firewall.get_layer(self.packet)
        if layer and layer.scanner == 0:
            self.severity += layer.severity()
        self.firewall.tick()

    def packet_escaped(self):
        return self.packet > self.firewall.max_depth

    def run(self):
        while not self.packet_escaped():
            self.tick()
        return self.severity

    def reset(self):
        self.packet = -1
        self.severity = 0
        self.firewall.reset()

    def find_min_delay(self):
        self.reset()
        delay = 0
        while True:
            delay += 1
            self.firewall.tick()
            caught = False
            for depth, layer in self.firewall.layers.items():
                if layer.is_scanner_at_top_after(depth + 1):
                    caught = True
                    break
            if not caught:
                return delay + 1


class Test(unittest.TestCase):

    def setUp(self):
        self.test_data = ('0: 3',
                          '1: 2',
                          '4: 4',
                          '6: 4')
        self.world = World()
        for line in self.test_data:
            self.world.firewall.add_layer(parse_layer(line))

    def test_compute_severity(self):
        self.assertEqual(24, self.world.run())

    def test_compute_min_delay_to_escape_undetected(self):
        self.assertEqual(10, self.world.find_min_delay())


def parse_layer(s):
    depth, size = [int(t) for t in s.split(': ')]
    return Layer(depth, size)


def main():
    if len(sys.argv) >= 2:
        for fname in sys.argv[1:]:
            with open(fname, 'r') as infile:
                world = World()
                for line in infile:
                    world.firewall.add_layer(parse_layer(line))
                print("'%s' -> %d %d" %
                      (fname, world.run(), world.find_min_delay()))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
