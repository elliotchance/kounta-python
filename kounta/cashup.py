class CashupUrlGenerator:
    def get_url(self, **kwargs):
        if 'at' in kwargs.keys():
            return 'cashups/2013-04-29.json'
        if 'unprocessed' in kwargs.keys() and kwargs['unprocessed']:
            return 'cashups/unprocessed.json'
        return 'cashups.json'
