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
