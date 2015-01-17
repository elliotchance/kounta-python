from unittest import TestCase
from kounta import Company
import json

class TestCompany(TestCase):
    def setUp(self):
        obj = json.loads(open('test/company.json', 'r').read())
        self.company = Company(obj)

    def test_id(self):
        self.assertEqual(self.company.id, 5678)
