# Solution to http://adventofcode.com/2017/day/9

import unittest
import sys

GROUP = 1
GARBAGE = 2
SKIP = 3

def score(stream):
    total, current, garbage = 0, 0, 0
    state, previous = GROUP, None
    for c in stream:
        if state == GROUP:
            if c == '}':
                total += current
                current -= 1
            elif c == '{':
                current += 1
            elif c == '<':
                state = GARBAGE
            elif c == '!':
                previous = state
                state = SKIP
        elif state == GARBAGE:
            if c == '>':
                state = GROUP
            elif c == '!':
                previous = state
                state = SKIP
            else:
                garbage += 1
        elif state == SKIP:
            state = previous
            previous = None
    return total, garbage


class Test(unittest.TestCase):

    def test_score_groups(self):
        test_data = (
            ('{}', 1),
            ('{{{}}}', 6),
            ('{{},{}}', 5),
            ('{{{},{},{{}}}}', 16),
            ('{<a>,<a>,<a>,<a>}', 1),
            ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
            ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
            ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3))
        for stream, expected in test_data:
            actual = score(stream)[0]
            self.assertEqual(expected, actual,
                             "failed for '%s' actual %d expected %d" %
                             (stream, actual, expected))

    def test_score_garbage(self):
        test_data = (
            ('{<>}', 0),
            ('{<random characters>}', 17),
            ('{<<<<>}', 3),
            ('<{!>}>', 2),
            ('{<!!>}', 0),
            ('{<!!!>>}', 0),
            ('{<{o"i!a,<{i<a>}', 10))
        for stream, expected in test_data:
            actual = score(stream)[1]
            self.assertEqual(expected, actual,
                             "failed for '%s' actual %d expected %d" %
                             (stream, actual, expected))

def reader(fname):
    with open(fname) as infile:
        while True:
            char = infile.read(1)
            if char:
                yield char
            else:
                return

def main():
    if len(sys.argv) >= 2:
        for fname in sys.argv[1:]:
            print('%s -> %s' % (fname, score(reader(fname))))
    else:
        unittest.main()

if __name__ == '__main__':
    main()
