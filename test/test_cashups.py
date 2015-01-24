from unittest import TestCase
from kounta.cashup import CashupUrlGenerator

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
