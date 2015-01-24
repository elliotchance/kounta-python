from dateutil.parser import parse
from datetime import date

class CashupUrlGenerator:
    def _date_string(self, the_date):
        if not isinstance(the_date, date) and not isinstance(the_date, str):
            raise ValueError('must be a date or string representing a date')
        if not isinstance(the_date, date):
            the_date = parse(the_date)
        return str(the_date)[:10]

    def get_url(self, **kwargs):
        if 'since' in kwargs.keys():
            return 'cashups/since/%s.json' % self._date_string(kwargs['since'])
        if 'at' in kwargs.keys():
            return 'cashups/%s.json' % self._date_string(kwargs['at'])
        if 'unprocessed' in kwargs.keys() and kwargs['unprocessed']:
            return 'cashups/unprocessed.json'
        return 'cashups.json'
