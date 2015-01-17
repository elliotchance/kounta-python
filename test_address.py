from unittest import TestCase
from kounta import Address
import json

class TestAddress(TestCase):
    def test_id(self):
        obj = json.loads(open('test/address.json', 'r').read())
        address = Address(obj)
        self.assertEqual(address.id, 198109)
