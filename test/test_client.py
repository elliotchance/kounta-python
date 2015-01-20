from unittest import TestCase
from kounta.client import BasicClient, URLCache
from kounta.objects import Company
from mock import MagicMock
import json
import os

class TestBasicClient(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        config = json.load(open("config.json", 'r'))['basic']
        self.client = BasicClient(
            client_id = config['client_id'],
            client_secret = config['client_secret']
        )

    def test_company(self):
        if not os.environ.get('INTEGRATION'):
            return

        company = self.client.company
        self.assertTrue(isinstance(company, Company))
        self.assertEqual(company.id, 5735)

    def test_company_is_cached(self):
        self.client._fetch_url = MagicMock(return_value='{}')
        # noinspection PyStatementEffect
        self.client.company
        # noinspection PyStatementEffect
        self.client.company
        url = '/v1/companies/me.json'
        # noinspection PyUnresolvedReferences
        self.client._fetch_url.assert_called_once_with(url)

    def test_cache_is_initialised_with_object(self):
        self.assertTrue(isinstance(self.client._cache, URLCache))

    def test_company_uses_urlcache(self):
        self.client._fetch_url = MagicMock(return_value='{}')
        # noinspection PyStatementEffect
        self.client.company
        url = '/v1/companies/me.json'
        self.assertEqual(self.client._cache[url], {})


class TestURLCache(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.cache = URLCache()

    def test_fetching_a_cache_item_that_doesnt_exist_returns_none(self):
        self.assertEqual(self.cache['foo'], None)

    def test_setting_an_item_can_be_retrieved(self):
        self.cache['foo'] = 'bar'
        self.assertEqual(self.cache['foo'], 'bar')

    def test_setting_multiple_items_can_be_retrieved(self):
        self.cache['foo'] = 'bar'
        self.cache['bar'] = 'baz'
        self.assertEqual(self.cache['foo'], 'bar')
