import base64
import json
from kounta.objects import Company

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

class BasicClient:
    """
    BasicClient makes sure the same URL requested will not make another external
    request by caching the results of that URL for the lifetime of the client.

    This is particularly useful when doing lots of calls on the same or similar
    data. However, this may cause an issue when you update data through the API
    and get the old cached data returned the next time that endpoint is
    requested. So you can erase all cache with the reset_cache() method.
    """
    def __init__(self, client_id, client_secret):
        """
        :type client_secret: str
        :type client_id: str
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self._cache = URLCache()

    def _fetch_url(self, url):
        """
        This is an internal method, if you need to download an arbitrary
        endpoint, see get_url()

        :rtype : dict
        :param url: str
        """
        encoded = base64.b64encode(self.client_id + ':' + self.client_secret)
        headers = {
            "Authorization": "Basic " + encoded
        }
        request = urllib2.Request('https://api.kounta.com' + url,
                                  headers=headers)
        return urllib2.urlopen(request).read()

    def get_url(self, url):
        """
        Get a URL (API endpoint). This makes use of URL caching (see class
        description).
        :type url: string
        :rtype: dict
        """
        if self._cache[url] is None:
            self._cache[url] = json.loads(self._fetch_url(url))
        return self._cache[url]

    @property
    def company(self):
        """
        Fetch the company. This is the starting point for all API requests. The
        Company object will expose more methods to fetch further endpoints.
        :rtype : Company
        """
        return Company(self.get_url('/v1/companies/me.json'), self)

    def reset_cache(self):
        """
        This is a crude way or handling the dropping of all cache.

        In this future there should be a way of selectively deleting cache.
        """
        self._cache = URLCache()


class URLCache:
    def __init__(self):
        self.cache = {}

    def __getitem__(self, item):
        return self.cache.get(item, None)

    def __setitem__(self, key, value):
        self.cache[key] = value
