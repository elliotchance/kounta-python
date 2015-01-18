from dateutil.parser import parse
import json


class BaseObject:
    """
    Used as the parent for all objects returned from the API. It main purpose is
    to allow documentation to be built into the object instead of using plain
    `dict`s.
    """

    def __init__(self, obj):
        """
        :type obj: dict
        """
        self.obj = obj

    def __getattr__(self, item):
        return self.obj[item]

    def __str__(self):
        return json.dumps(self.obj)


class Address(BaseObject):
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


class Company(BaseObject):
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

    @property
    def name(self):
        """
        Company name.
        :return: string
        """
        return self.obj['name']

    @property
    def shipping_address(self):
        """
        Shipping address.
        :return: Address
        """
        shipping_address = self.obj['shipping_address']
        return Address(shipping_address) if shipping_address else None

    @property
    def postal_address(self):
        """
        Postal address.
        :return: Address
        """
        postal_address = self.obj['postal_address']
        return Address(postal_address) if postal_address else None

    @property
    def addresses(self):
        """
        Total addresses available.
        :return: object
        """
        addresses = self.obj['addresses']
        addresses['updated_at'] = parse(addresses['updated_at'])
        return addresses

    @property
    def business_number(self):
        """
        ABN, ACN or whatever is applicable as the business number.
        :return: string
        """
        return self.obj['business_number']

    @property
    def contact_staff_member(self):
        """
        Contact staff member.
        :return: Staff
        """
        return Staff(self.obj['contact_staff_member'])

    @property
    def image(self):
        """
        Avatar image.
        :return: string
        """
        return self.obj['image']

    @property
    def website(self):
        """
        Website.
        :return: string
        """
        return self.obj['website']

    @property
    def currency(self):
        """
        Currency code.
        :return: string
        """
        return self.obj['currency']

    @property
    def timezone(self):
        """
        Timezone information.
        :return: Timezone
        """
        return Timezone(self.obj['timezone'])

    @property
    def sites(self):
        """
        Sites.
        :return: object
        """
        sites = self.obj['sites']
        sites['updated_at'] = parse(sites['updated_at'])
        return sites

    @property
    def registers(self):
        """
        Registers.
        :return: object
        """
        registers = self.obj['registers']
        registers['updated_at'] = parse(registers['updated_at'])
        return registers

    @property
    def created_at(self):
        """
        When the company was created.
        :return: datetime
        """
        return parse(self.obj['created_at'])

    @property
    def updated_at(self):
        """
        When the company was last modified.
        :return: datetime
        """
        return parse(self.obj['updated_at'])


class Permission(BaseObject):
    @property
    def code(self):
        """
        :rtype : string
        """
        return self.obj['code']

    @property
    def name(self):
        """
        :rtype : string
        """
        return self.obj['name']

    @property
    def domain(self):
        """
        :rtype : string
        """
        return self.obj['domain']


class Timezone(BaseObject):
    @property
    def offset(self):
        return self.obj['offset']

    @property
    def name(self):
        return self.obj['name']


class Staff(BaseObject):
    @property
    def offset(self):
        return self.obj['offset']
