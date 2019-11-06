import unittest
import doctest

from . import decoders


def suite():
    suite = unittest.TestSuite()
    for m in decoders:
        suite.addTests(doctest.DocTestSuite(m))
    return suite


def load_tests(loader, tests, ignore):
    tests.addTests(suite())
    return tests


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
