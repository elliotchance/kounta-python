from unittest import TestCase
from kounta.cashup import CashupUrlGenerator
from dateutil.parser import parse

class TestCashupUrlGenerator(TestCase):
    def test_no_filter(self):
        generator = CashupUrlGenerator()
        self.assertEqual(generator.get_url(), 'cashups.json')

    def test_unprocessed(self):
        generator = CashupUrlGenerator()
        self.assertEqual(generator.get_url(unprocessed=True),
                         'cashups/unprocessed.json')

    def test_unprocessed_false(self):
        generator = CashupUrlGenerator()
        self.assertEqual(generator.get_url(unprocessed=False),
                         'cashups.json')

    def test_at(self):
        generator = CashupUrlGenerator()
        self.assertEqual(generator.get_url(at='2013-04-29'),
                         'cashups/2013-04-29.json')

    def test_at_with_datetime(self):
        generator = CashupUrlGenerator()
        self.assertEqual(generator.get_url(at=parse('2013-04-28')),
                         'cashups/2013-04-28.json')

    def test_since(self):
        generator = CashupUrlGenerator()
        self.assertEqual(generator.get_url(since='2013-04-29'),
                         'cashups/since/2013-04-29.json')

    def test_since_with_datetime(self):
        generator = CashupUrlGenerator()
        self.assertEqual(generator.get_url(since=parse('2013-04-28')),
                         'cashups/since/2013-04-28.json')

    def test_at_invalid_string(self):
        generator = CashupUrlGenerator()
        self.assertRaises(ValueError, generator.get_url, **{'at': 'foo'})

    def test_at_invalid_type(self):
        generator = CashupUrlGenerator()
        self.assertRaises(ValueError, generator.get_url, **{'at': {}})
