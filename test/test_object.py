from unittest import TestCase
from kounta import Object
import json

class TestObject(TestCase):
    def test_nonexistent_property(self):
        obj = json.loads('{"foo":"bar"}')
        address = Object(obj)
        self.assertEqual(address.foo, "bar")
