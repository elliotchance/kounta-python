from unittest import TestCase
from kounta.client import BasicClient
from kounta.objects import Company
from mock import MagicMock
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

    def test_company_is_cached(self):
        config = json.load(open("config.json", 'r'))['basic']
        client = BasicClient(
            client_id = config['client_id'],
            client_secret = config['client_secret']
        )
        client._fetchURL = MagicMock(return_value='{}')
        client.company
        client.company
        url = 'https://api.kounta.com/v1/companies/me.json'
        client._fetchURL.assert_called_once_with(url)
