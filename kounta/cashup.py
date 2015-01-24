class CashupUrlGenerator:
    def _date_string(self, date):
        return str(date)[:10]

    def get_url(self, **kwargs):
        if 'since' in kwargs.keys():
            return 'cashups/since/%s.json' % self._date_string(kwargs['since'])
        if 'at' in kwargs.keys():
            return 'cashups/%s.json' % self._date_string(kwargs['at'])
        if 'unprocessed' in kwargs.keys() and kwargs['unprocessed']:
            return 'cashups/unprocessed.json'
        return 'cashups.json'
