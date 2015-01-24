class CashupUrlGenerator:
    def get_url(self, **kwargs):
        if 'unprocessed' in kwargs.keys() and kwargs['unprocessed']:
            return 'cashups/unprocessed.json'
        return 'cashups.json'
