class CashupUrlGenerator:
    def get_url(self, **kwargs):
        if 'at' in kwargs.keys():
            return 'cashups/%s.json' % str(kwargs['at'])[:10]
        if 'unprocessed' in kwargs.keys() and kwargs['unprocessed']:
            return 'cashups/unprocessed.json'
        return 'cashups.json'
