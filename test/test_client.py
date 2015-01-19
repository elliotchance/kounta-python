from unittest import TestCase
from kounta.client import BasicClient
from kounta.objects import Company
from mock import MagicMock
import json
import os

class TestBasicClient(TestCase):
    def test_company(self):
        if not os.environ.get('INTEGRATION'):
            return

        config = json.load(open("config.json", 'r'))['basic']
        client = BasicClient(
            client_id = config['client_id'],
            client_secret = config['client_secret']
        )
        company = client.company
        self.assertTrue(isinstance(company, Company))
        self.assertEqual(company.id, 5735)

    def test_company_is_cached(self):
        if not os.environ.get('INTEGRATION'):
            return

        config = json.load(open("config.json", 'r'))['basic']
        client = BasicClient(
            client_id = config['client_id'],
            client_secret = config['client_secret']
        )
        client._fetch_url = MagicMock(return_value='{}')
        client.company
        client.company
        url = '/v1/companies/me.json'
        # noinspection PyUnresolvedReferences
        client._fetch_url.assert_called_once_with(url)
