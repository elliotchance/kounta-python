import urllib2
import base64
import json
from kounta.objects import Company

class BasicClient:
    _company = None

    def __init__(self, client_id, client_secret):
        """
        :type client_secret: str
        :type client_id: str
        """
        self.client_id = client_id
        self.client_secret = client_secret

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
        :type url: string
        """
        return json.loads(self._fetch_url(url))

    @property
    def company(self):
        if self._company is None:
            url = '/v1/companies/me.json'
            self._company = Company(self.get_url(url), self)
        return self._company
