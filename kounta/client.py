import urllib2
import base64
import json
from kounta.objects import Company

class BasicClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def _fetchURL(self, url):
        """
        :rtype : dict
        :param url: string
        """
        encoded = base64.b64encode(self.client_id + ':' + self.client_secret)
        headers = {
            "Authorization": "Basic " + encoded
        }
        request = urllib2.Request(url, headers=headers)
        return json.loads(urllib2.urlopen(request).read())

    @property
    def company(self):
        url = 'https://api.kounta.com/v1/companies/me.json'
        return Company(self._fetchURL(url))
