from unittest import TestCase
from kounta.client import BasicClient
from kounta.objects import Company
import json

class TestBasicClient(TestCase):
    def test_company(self):
        config = json.load(open("config.json", 'r'))['basic']
        client = BasicClient(
            client_id = config['client_id'],
            client_secret = config['client_secret']
        )
        company = client.company
        self.assertTrue(isinstance(company, Company))
        self.assertEqual(company.id, 5735)
