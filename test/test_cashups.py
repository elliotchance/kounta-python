from unittest import TestCase
from kounta.cashup import CashupUrlGenerator

class TestCashupUrlGenerator(TestCase):
    def test_no_filter(self):
        generator = CashupUrlGenerator()
        self.assertEqual(generator.get_url(), 'cashups.json')
