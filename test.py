import unittest
import numpy as np
from random import randint
from OPM_start import check_diff_sign, normalize_cc


class TestNormalizeCC(unittest.TestCase):
    
    def test_main(self):
        self.assertAlmostEqual(normalize_cc(float('nan')), 1.0)
        self.assertAlmostEqual(normalize_cc(-0.0000001), 0.001)


class TestCheckDiffSign(unittest.TestCase):

    def test_notdiff(self):
        self.assertFalse(check_diff_sign(-5.1, -5.1))
        self.assertFalse(check_diff_sign(5.1, 5.0))
        self.assertFalse(check_diff_sign(5.0, 0.00001))
        self.assertFalse(check_diff_sign(0.0000001, 0.000001))

    def test_diff(self):
        self.assertTrue(check_diff_sign(-0.00001, 0.00001))
        self.assertTrue(check_diff_sign(-5.0, 5.1))

    def test_zeroes(self):
        self.assertTrue(check_diff_sign(-5.0, 0.0))
        self.assertTrue(check_diff_sign(0.0, -0.000000001))
        self.assertTrue(check_diff_sign(5.0, -0.0))
        self.assertTrue(check_diff_sign(0.0, -0.0))


class TestData(unittest.TestCase):
    
    prices = [randint(1, 100) for i in range(100)]
    positive_cc = [i + 1 for i in prices]
    negative_cc = [i - (2 * i) for i in prices]
    no_cc = [randint(1, 100) for i in range(100)]

if __name__ == '__main__':
    unittest.main()
