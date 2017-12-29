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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return "<%d, %d, %d>" % (self.x, self.y, self.z)


class Particle(object):

    def __init__(self, i, p, v, a):
        self.i = i
        self.p = p
        self.v = v
        self.a = a

    def move(self):
        self.v.add(self.a)
        self.p.add(self.v)

    def distance_from_origin(self):
        return abs(self.p.x) + abs(self.p.y) + abs(self.p.z)

    def collide(self, other):
        return self.p == other.p

    def __eq__(self, other):
        return self.i == other.i

    def __hash__(self):
        return hash(self.i)

    def __str__(self):
        return "i=%d p=%s v=%s a=%s" % (self.i, self.p, self.v, self.a)


class System(object):

    def __init__(self, filename):
        with open(filename, 'r') as infile:
            self.particles = set()
            for i, line in enumerate(infile):
                self.particles.add(self.parse_particle(i, line))

    @staticmethod
    def parse_particle(i, s):
        ns = [int(t) for t in re.findall('[-]?\d+', s)]
        p = Vector3(ns[0], ns[1], ns[2])
        v = Vector3(ns[3], ns[4], ns[5])
        a = Vector3(ns[6], ns[7], ns[8])
        return Particle(i, p, v, a)

    def run(self, times=1000, collision_check=False):
        for _ in range(times):
            for p in self.particles:
                p.move()
            if collision_check:
                collided = set()
                for p in self.particles:
                    if p not in collided:
                        for o in self.particles:
                            if o not in collided and p != o and p.collide(o):
                                collided.add(p)
                                collided.add(o)
                self.particles -= collided

    def closest_to_origin(self):
        min_d, closest = None, None
        for p in self.particles:
            d = p.distance_from_origin()
            if min_d is None or d < min_d:
                min_d = d
                closest = p
        return closest


class Test(unittest.TestCase):

    def test_closest_to_origin(self):
        system = System('day_20.test')
        system.run()
        self.assertEqual(0, system.closest_to_origin().i)

    def test_collision(self):
        p0 = Particle(0, Vector3(1, 2, 3), Vector3(0, 1, 2), Vector3(1, 1, 1))
        p1 = Particle(1, Vector3(1, 2, 3), Vector3(3, 0, 2), Vector3(0, 1, 1))
        self.assertTrue(p0.collide(p1))


def main():
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            system = System(name)
            system.run(times=500, collision_check=True)
            print("%s -> %s | %d" % (name, system.closest_to_origin(), len(system.particles)))
    else:
        unittest.main()


if __name__ == '__main__':
    main()
