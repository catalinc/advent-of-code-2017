# Solution to http://adventofcode.com/2017/day/20

import unittest
import sys
import re


class Vector3(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __str__(self):
        return "<%d, %d, %d>" % (self.x, self.y, self.z)


class Particle(object):

    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    def move(self):
        self.v.add(self.a)
        self.p.add(self.v)

    def distance_from_origin(self):
        return abs(self.p.x) + abs(self.p.y) + abs(self.p.z)

    def __str__(self):
        return "p=%s v=%s a=%s" % (self.p, self.v, self.a)


class System(object):

    def __init__(self, filename):
        with open(filename, 'r') as infile:
            self.particles = []
            for line in infile:
                self.particles.append(self.parse_particle(line))

    @staticmethod
    def parse_particle(s):
        ns = [int(t) for t in re.findall('[-]?\d+', s)]
        p = Vector3(ns[0], ns[1], ns[2])
        v = Vector3(ns[3], ns[4], ns[5])
        a = Vector3(ns[6], ns[7], ns[8])
        return Particle(p, v, a)

    def run(self, times=1000):
        for _ in range(times):
            for p in self.particles:
                p.move()
        min_d = self.particles[0].distance_from_origin()
        min_i = 0
        for i, p in enumerate(self.particles):
            d = p.distance_from_origin()
            if d < min_d:
                min_d = d
                min_i = i
        return min_i


class Test(unittest.TestCase):

    def test_closest_to_origin(self):
        system = System('day_20.test')
        self.assertEqual(0, system.run())


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            system = System(name)
            print("%s -> %d" % (name, system.run()))
    else:
        unittest.main()
