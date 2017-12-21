# Solution to http://adventofcode.com/2017/day/19

import sys
import unittest


def load_map(filename):
    with open(filename, 'r') as infile:
        m = []
        for line in infile:
            m.append(list(line))
        return m


directions = {'d': (1, 0, ('l', 'r')),
              'u': (-1, 0, ('l', 'r')),
              'l': (0, -1, ('d', 'u')),
              'r': (0, 1, ('d', 'u'))}


def walk_map(m):
    r, c, d = 0, m[0].index('|'), 'd'
    msg = []
    steps = 0
    while True:
        ch = m[r][c]
        if ch == ' ':
            break
        elif ch == '+':
            for k in directions[d][2]:
                if k != d:
                    new_r = r + directions[k][0]
                    new_c = c + directions[k][1]
                    if new_r < 0 or new_r >= len(m):
                        continue
                    if new_c < 0 or new_c >= len(m[r]):
                        continue
                    if m[new_r][new_c] != ' ':
                        r, c = new_r, new_c
                        d = k
                        break
        else:
            if 'A' <= ch <= 'Z':
                msg.append(ch)
            r += directions[d][0]
            c += directions[d][1]
        steps += 1
    return ''.join(msg), steps


class Test(unittest.TestCase):

    def test_load_map(self):
        m = load_map('day_19.test')
        self.assertEqual('|', m[0][5])
        self.assertEqual('F', m[3][1])

    def test_walk_map(self):
        m = load_map('day_19.test')
        self.assertEqual(('ABCDEF', 38), walk_map(m))


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        for name in sys.argv[1:]:
            m = load_map(name)
            print('%s -> %s' % (name, walk_map(m)))
    else:
        unittest.main()
