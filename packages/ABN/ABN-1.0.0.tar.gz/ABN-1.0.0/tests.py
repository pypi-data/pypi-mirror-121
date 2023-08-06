import doctest
import unittest

import abn

def load_tests(loader, tests, ignore):
    # Run doctests too.
    tests.addTests(doctest.DocFileSuite('README.rst'))
    return tests


class FormatABNTestCase(unittest.TestCase):
    def test_format(self):
        self.assertEqual(abn.format('12345678901'), '12 345 678 901')


class ValidateABNTestCase(unittest.TestCase):
    def test_valid_abn_passes(self):
        self.assertTrue(abn.validate('53 004 085 616'))

    def test_off_by_one_abn_fails(self):
        # Valid ABN with last digit modified.
        self.assertFalse(abn.validate('53 004 085 615'))

    def test_spacing_unnecessary(self):
        self.assertTrue(abn.validate('53004085616'))

    def test_punctuation_ok(self):
        self.assertTrue(abn.validate('53-004-085-616'))

    def test_too_long_abn_fails(self):
        self.assertFalse(abn.validate('53 004 085 6160'))

    def test_too_short_abn_fails(self):
        self.assertFalse(abn.validate('53 004 085 61'))

    def test_leading_zero_fails(self):
        # Using the ATO's algorithm, this ABN be generated as "98 002 928 323".
        # The check digits "09" also pass the validation algorithm, but would
        # never be generated.
        self.assertFalse(abn.validate('09 002 928 323'))


class ConvertACNTestCase(unittest.TestCase):
    def test_valid_acn_converted(self):
        self.assertTrue(abn.acn_to_abn('004085616'))

    def test_too_long_acn_fails(self):
        self.assertRaises(ValueError, abn.acn_to_abn, '0040856160')

    def test_too_short_acn_fails(self):
        self.assertRaises(ValueError, abn.acn_to_abn, '00408561')

    def test_acn_with_single_digit_remainder(self):
        self.assertTrue(abn.acn_to_abn('000000009'))


if __name__ == '__main__':
    unittest.main()
