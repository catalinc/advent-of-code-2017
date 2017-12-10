# Solution to http://adventofcode.com/2017/day/4

import unittest
import sys


def valid_no_duplicates(str):
    words = set()
    for w in str.split():
        if w in words:
            return False
        words.add(w)
    return True


def valid_no_anagrams(str):
    words = [''.join(sorted(w)) for w in str.split()]
    seen = set()
    for w in words:
        if w in seen:
            return False
        seen.add(w)
    return True


class Test(unittest.TestCase):

    def test_valid_no_duplicate(self):
        test_data = [('aa bb cc dd ee', True),
                     ('aa bb cc dd aaa', True),
                     ('aa bb cc dd aa', False),
                     ('aa bb cc bb aaa', False)]
        for str, expected in test_data:
            self.assertEqual(expected, valid_no_duplicates(str),
                             "failed for %s" % str)

    def test_valid_no_anagrams(self):
        test_data = [("abcde fghij", True),
                     ("abcde xyz ecdab", False),
                     ("a ab abc abd abf abj", True),
                     ("iiii oiii ooii oooi oooo", True),
                     ("oiii ioii iioi iiio", False)]
        for str, expected in test_data:
            self.assertEqual(expected, valid_no_anagrams(str),
                             "failed for %s" % str)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        for filename in sys.argv[1:]:
            with open(filename) as inputfile:
                count = 0
                for line in inputfile:
                    if valid_no_anagrams(line):
                        count += 1
                print("%d valid passwords in %s" % (count, filename))
    else:
        unittest.main()
