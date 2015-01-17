class Object:
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, item):
        return self.obj[item]

class Address(Object):
    """
    Addresses are physical or postal locations belonging to a staff member,
    customer, company or site.
    """

    @property
    def id(self):
        """
        Address ID.
        :return: integer
        """
        return self.obj['id']

    @property
    def city(self):
        """
        City/suburb.
        :return: string
        """
        return self.obj['city']

    @property
    def lines(self):
        """
        Address lines.
        :return: string[]
        """
        return self.obj['lines']

    @property
    def zone(self):
        """
        Zone/state.
        :return: string
        """
        return self.obj['zone']

    @property
    def postal_code(self):
        """
        Postal code.
        :return: string
        """
        return self.obj['postal_code']

    @property
    def country(self):
        """
        Country.
        :return: string
        """
        return self.obj['country']

class Company(Object):
    """
    Companies are businesses who use Kounta at their points of sale. A company
    may have one or more registers running Kounta on one or more sites.
    """

    @property
    def id(self):
        """
        Company ID.
        :return: integer
        """
        return self.obj['id']
