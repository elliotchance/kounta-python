class CashupUrlGenerator:
    def get_url(self, **kwargs):
        if 'since' in kwargs.keys():
            return 'cashups/since/2013-04-29.json'
        if 'at' in kwargs.keys():
            return 'cashups/%s.json' % str(kwargs['at'])[:10]
        if 'unprocessed' in kwargs.keys() and kwargs['unprocessed']:
            return 'cashups/unprocessed.json'
        return 'cashups.json'
