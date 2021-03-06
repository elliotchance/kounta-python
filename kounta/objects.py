from dateutil.parser import parse
import os
import json

"""
We must prevent CashupUrlGenerator from being imported when we only want to
generated documentation of the classes in this file.
"""
if not os.environ.get('DOC'):
    from kounta.cashup import CashupUrlGenerator


class BaseObject:
    """
    Used as the parent for all objects returned from the API. It main purpose is
    to allow documentation to be built into the object instead of using plain
    `dict`s.
    """

    def __init__(self, obj, client, company):
        """
        :type company: Company|None
        :type client: kounta.client.BasicClient
        :type obj: dict
        """

        assert isinstance(company, Company) or company is None

        self.obj = obj
        self._client = client
        self._company = company

    def __getattr__(self, item):
        """
        Returns an attribute as it was originally set in the raw object.
        :type item: str
        """
        return self.obj[item]

    def __str__(self):
        """
        When converting any API object to a string the original JSON fetched
        will be returned.

        It is important to recognise that this JSON may not represent the actual
        state of the object behind it because some calls may make further API
        requests.
        """
        return json.dumps(self.obj)

    def _make_address(self, field):
        """
        Test if a `field` is not None and return an Address object. Otherwise
        return None
        :type field: str
        """
        address = self.obj[field]
        if address:
            return Address(address, self._client, self._company)
        return None

    def _get_addresses(self, url):
        """
        :return: Address[]
        """
        url = '/v1/companies/%d/%s' % (self._company.id, url)
        addresses = self._client.get_url(url)
        return [Address(address, self._client, self._company) for address in
                addresses]

    def _get_cashups(self, url, **kwargs):
        """
        :return: Cashup[]
        """
        generator = CashupUrlGenerator()
        url = '%s/%s' % (url, generator.get_url(**kwargs))
        cashups = self._client.get_url(url)
        return [Cashup(cashup, self._client, self._company) for cashup
                in cashups]

    def _get_categories(self, url):
        """
        :return: Category[]
        """
        categories = self._client.get_url(url)
        return [Category(category, self._client, self._company) for category in
                categories]


class Address(BaseObject):
    """
    Addresses are physical or postal locations belonging to a staff member,
    customer, company or site.
    """

    @property
    def id(self):
        """
        Address ID.
        :return: int
        """
        return self.obj['id']

    @property
    def city(self):
        """
        City/suburb.
        :return: str
        """
        return self.obj['city']

    @property
    def lines(self):
        """
        Address lines.
        :return: str[]
        """
        return self.obj['lines']

    @property
    def zone(self):
        """
        Zone/state.
        :return: str
        """
        return self.obj['zone']

    @property
    def postal_code(self):
        """
        Postal code.
        :return: str
        """
        return self.obj['postal_code']

    @property
    def country(self):
        """
        Country.
        :return: str
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
        :return: int
        """
        return self.obj['id']

    @property
    def name(self):
        """
        Company name.
        :return: str
        """
        return self.obj['name']

    @property
    def shipping_address(self):
        """
        Shipping address.
        :return: Address
        """
        return self._make_address('shipping_address')

    @property
    def postal_address(self):
        """
        Postal address.
        :return: Address
        """
        return self._make_address('postal_address')

    @property
    def addresses(self):
        """
        All addresses attached to this company.
        :return: Address[]
        """
        url = '/v1/companies/%d/addresses.json' % self.id
        addresses = self._client.get_url(url)
        return [Address(address, self._client, self) for address in addresses]

    @property
    def business_number(self):
        """
        ABN, ACN or whatever is applicable as the business number.
        :return: str
        """
        return self.obj['business_number']

    @property
    def contact_staff_member(self):
        """
        Contact staff member.
        :return: Staff
        """
        return Staff(self.obj['contact_staff_member'], self._client, self)

    @property
    def image(self):
        """
        Avatar image.
        :return: str
        """
        return self.obj['image']

    @property
    def website(self):
        """
        Website.
        :return: str
        """
        return self.obj['website']

    @property
    def currency(self):
        """
        Currency code.
        :return: str
        """
        return self.obj['currency']

    @property
    def timezone(self):
        """
        Timezone information.
        :return: Timezone
        """
        return Timezone(self.obj['timezone'], self._client, self)

    @property
    def sites(self):
        """
        Fetch all sites for this company.
        :return: Site[]
        """
        sites = self._client.get_url('/v1/companies/%d/sites.json' % self.id)
        return [Site(site, self._client, self) for site in sites]

    @property
    def registers(self):
        """
        Fetch all registers for this company.
        :return: Register[]
        """
        url = '/v1/companies/%d/registers.json' % self.id
        registers = self._client.get_url(url)
        return [Register(register, self._client, self._company) for register in
                registers]

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

    def cashups(self, **kwargs):
        """
        Fetch cashups for a company. Refer to documentation for Cashups for more
        information.
        :rtype : Cashup[]
        """
        return self._get_cashups('/v1/companies/%d' % self.id, **kwargs)

    @property
    def categories(self):
        """
        All categories for this company.
        :rtype : Category[]
        """
        url = '/v1/companies/%d/categories.json' % self.id
        return self._get_categories(url)


class Permission(BaseObject):
    @property
    def code(self):
        """
        :rtype : str
        """
        return self.obj['code']

    @property
    def name(self):
        """
        :rtype : str
        """
        return self.obj['name']

    @property
    def domain(self):
        """
        :rtype : str
        """
        return self.obj['domain']


class Timezone(BaseObject):
    """
    A timezone represents a time offset at a geographical location.
    """

    @property
    def offset(self):
        """
        :rtype : str
        """
        return self.obj['offset']

    @property
    def name(self):
        """
        :rtype : str
        """
        return self.obj['name']


class Staff(BaseObject):
    """
    Staff members are people who work for the authenticated company.
    """

    @property
    def id(self):
        """
        :rtype: int
        """
        return self.obj['id']

    @property
    def first_name(self):
        """
        :rtype: str
        """
        return self.obj['first_name']

    @property
    def last_name(self):
        """
        :rtype: str
        """
        return self.obj['last_name']

    @property
    def is_admin(self):
        """
        :rtype: boolean
        """
        return self.obj['is_admin']

    @property
    def primary_email_address(self):
        """
        :rtype: str
        """
        return self.obj['primary_email_address']

    @property
    def email_addresses(self):
        """
        :rtype: str[]
        """
        return self.obj['email_addresses']

    @property
    def phone(self):
        """
        :rtype: str
        """
        return self.obj['phone']

    @property
    def mobile(self):
        """
        :rtype: str
        """
        return self.obj['mobile']

    @property
    def fax(self):
        """
        :rtype: str
        """
        return self.obj['fax']

    @property
    def shipping_address(self):
        """
        :return: Address
        """
        return self._make_address('shipping_address')

    @property
    def postal_address(self):
        """
        :return: Address
        """
        return self._make_address('postal_address')

    @property
    def permissions(self):
        """
        :return: Permission[]
        """
        return [Permission(p, self._client, self._company) for p in
                self.obj['permissions']]

    @property
    def image(self):
        """
        :rtype: str
        """
        return self.obj['image']

    @property
    def created_at(self):
        """
        :rtype: str
        """
        return parse(self.obj['created_at'])

    @property
    def updated_at(self):
        """
        :rtype: str
        """
        return parse(self.obj['updated_at'])

    @property
    def addresses(self):
        """
        All addresses attached to this staff member.
        :return: Address[]
        """
        return self._get_addresses('staff/%d/addresses.json' % self.id)


class Site(BaseObject):
    """
    Sites are physical locations, such as outlets, offices etc, at which one or
    more Kountas will be used.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def name(self):
        """
        :return: str
        """
        return self.obj['name']

    @property
    def code(self):
        """
        :return: str
        """
        return self.obj['code']

    @property
    def contact_person(self):
        """
        :return: Staff
        """
        return Staff(self.obj['contact_person'], self._client, self._company)

    @property
    def business_number(self):
        """
        :return: str
        """
        return self.obj['business_number']

    @property
    def shipping_address(self):
        """
        :return: Address
        """
        return self._make_address('shipping_address')

    @property
    def postal_address(self):
        """
        :return: Address
        """
        return self._make_address('postal_address')

    @property
    def email(self):
        """
        :return: str
        """
        return self.obj['email']

    @property
    def mobile(self):
        """
        :return: str
        """
        return self.obj['mobile']

    @property
    def phone(self):
        """
        :return: str
        """
        return self.obj['phone']

    @property
    def fax(self):
        """
        :return: str
        """
        return self.obj['fax']

    @property
    def location(self):
        """
        :return: Location
        """
        return Location(self.obj['location'], self._client, self._company)

    @property
    def image(self):
        """
        :return: str
        """
        return self.obj['image']

    @property
    def website(self):
        """
        :return: str
        """
        return self.obj['website']

    @property
    def register_level_reconciliation(self):
        """
        :return: boolean
        """
        return self.obj['register_level_reconciliation']

    @property
    def price_list(self):
        """
        :return: PriceList
        """
        return PriceList(self.obj['price_list'], self._client, self._company)

    @property
    def created_at(self):
        """
        :return: datetime
        """
        return parse(self.obj['created_at'])

    @property
    def updated_at(self):
        """
        :return: datetime
        """
        return parse(self.obj['updated_at'])

    @property
    def addresses(self):
        """
        All addresses attached to this site.
        :return: Address[]
        """
        return self._get_addresses('sites/%d/addresses.json' % self.id)

    def cashups(self, **kwargs):
        """
        Fetch cashups for a register. Refer to documentation for Cashups for
        more information.
        :rtype : Cashup[]
        """
        url = '/v1/companies/%d/sites/%d' % (self._company.id, self.id)
        return self._get_cashups(url, **kwargs)

    @property
    def categories(self):
        """
        All categories for this site.
        :rtype : Category[]
        """
        url = '/v1/companies/%d/sites/%d/categories.json' % (self._company.id,
                                                            self.id)
        return self._get_categories(url)

    @property
    def checkins(self):
        """
        All checkins for this site.
        :rtype : Checkin[]
        """
        url = '/v1/companies/%d/sites/%d/checkins.json' % (self._company.id, self.id)
        checkins = self._client.get_url(url)
        return [Checkin(checkin, self._client, self._company) for checkin in
                checkins]


class Category(BaseObject):
    """
    Each product will belong to one or more categories.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def name(self):
        """
        :return: int
        """
        return self.obj['name']

    @property
    def description(self):
        """
        :return: str
        """
        return self.obj['description']

    @property
    def image(self):
        """
        :return: str
        """
        return self.obj['image']


class Product(BaseObject):
    """
    Products are saleable items in your inventory, including modifier products.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def name(self):
        """
        :return: int
        """
        return self.obj['name']

    @property
    def description(self):
        """
        :return: str
        """
        return self.obj['description']

    @property
    def code(self):
        """
        :return: str
        """
        return self.obj['code']

    @property
    def barcode(self):
        """
        :return: str
        """
        return self.obj['barcode']

    @property
    def categories(self):
        """
        All categories for this product.
        :rtype : Category[]
        """
        url = '/v1/companies/%d/products/%d/categories.json' % \
              (self._company.id, self.id)
        return self._get_categories(url)


class Checkin(BaseObject):
    """
    Authenticated customers can use checkin service.
    """

    @property
    def customer_id(self):
        """
        :return: int
        """
        return self.obj['customer_id']

    @property
    def start_time(self):
        """
        :return: datetime
        """
        return parse(self.obj['start_time'])

    @property
    def duration(self):
        """
        :return: int
        """
        return self.obj['duration']


class Customer(BaseObject):
    """
    Customers are people who buy from the authenticated company.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def first_name(self):
        """
        :return: str
        """
        return self.obj['first_name']

    @property
    def last_name(self):
        """
        :return: str
        """
        return self.obj['last_name']

    @property
    def primary_email_address(self):
        """
        :return: str
        """
        return self.obj['primary_email_address']

    @property
    def image(self):
        """
        :return: str
        """
        return self.obj['image']

    @property
    def reference_id(self):
        """
        :return: str
        """
        return self.obj['reference_id']

    @property
    def addresses(self):
        """
        All addresses attached to this customer.
        :return: Address[]
        """
        return self._get_addresses('customer/%d/addresses.json' % self.id)


class Inventory(BaseObject):
    """
    Inventory indicates the quantity for a given product.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def stock(self):
        """
        :return: int
        """
        return self.obj['stock']


class Line(BaseObject):
    """
    Lines (also called order lines, sale lines or line items) describe the
    products included in an order.
    """

    @property
    def number(self):
        """
        The line number. This will start with `1`.
        :return: int
        """
        return self.obj['number']

    @property
    def product_id(self):
        """
        :return: int
        """
        return self.obj['product_id']

    @property
    def quantity(self):
        """
        :return: int
        """
        return self.obj['quantity']

    @property
    def notes(self):
        """
        :return: str
        """
        return self.obj['notes']

    @property
    def unit_price(self):
        """
        :return: float
        """
        return self.obj['unit_price']

    @property
    def price_variation(self):
        """
        :return: float
        """
        return self.obj['price_variation']

    @property
    def modifiers(self):
        """
        :return: int[]
        """
        return self.obj['modifiers']


class Order(BaseObject):
    """
    Orders are also sometimes called sales or invoices.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def status(self):
        """
        :return: str
        """
        return self.obj['status']

    @property
    def total(self):
        """
        :return: float
        """
        return self.obj['total']

    @property
    def total_tax(self):
        """
        :return: float
        """
        return self.obj['total_tax']

    @property
    def paid(self):
        """
        :return: float
        """
        return self.obj['paid']

    @property
    def created_at(self):
        """
        :return: datetime
        """
        return parse(self.obj['created_at'])

    @property
    def updated_at(self):
        """
        :return: datetime
        """
        return parse(self.obj['updated_at'])


class PaymentMethod(BaseObject):
    """
    Payment methods are assigned to order payments.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def name(self):
        """
        :return: str
        """
        return self.obj['name']

    @property
    def ledger_code(self):
        """
        :return: str
        """
        return self.obj['ledger_code']


class Payment(BaseObject):
    """
    Payments (also called transactions) are financial transactions related to an
    order.
    """

    @property
    def method_id(self):
        """
        :return: int
        """
        return self.obj['method_id']

    @property
    def amount(self):
        """
        :return: float
        """
        return self.obj['amount']

    @property
    def ref(self):
        """
        :return: str
        """
        return self.obj['ref']


class PriceList(BaseObject):
    """
    Each site will be assigned a price list that determines ex tax unit prices
    of each item on sale.

    Price lists work by overriding prices in their parent lists (just like
    subclassing in object-oriented programming). The base price list has a
    parent_id of null.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def name(self):
        """
        :return: str
        """
        return self.obj['name']

    @property
    def parent_id(self):
        """
        :return: int
        """
        return self.obj['parent_id']


class Register(BaseObject):
    """
    Registers are iPads or other computers running Kounta.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def code(self):
        """
        :return: str
        """
        return self.obj['code']

    @property
    def name(self):
        """
        :return: str
        """
        return self.obj['name']

    @property
    def site_id(self):
        """
        :return: int
        """
        return self.obj['site_id']

    def cashups(self, **kwargs):
        """
        Fetch cashups for a register. Refer to documentation for Cashups for
        more information.
        :rtype : Cashup[]
        """
        url = '/v1/companies/%d/registers/%d' % (self._company.id, self.id)
        return self._get_cashups(url, **kwargs)


class ShiftPeriod(BaseObject):
    """
    Represents a block of time when dealing with `Shift`s.
    """

    @property
    def started_at(self):
        """
        :return: datetime
        """
        return parse(self.obj['started_at'])

    @property
    def finished_at(self):
        """
        :return: datetime
        """
        return parse(self.obj['finished_at'])

    @property
    def period(self):
        """
        The timedelta between the start anf finish time.
        :return: timedelta
        """
        return self.started_at - self.finished_at


class Shift(ShiftPeriod):
    """
    Shifts record staff check-ins, check-outs and breaks.
    """

    @property
    def staff_member(self):
        """
        :return: Staff
        """
        return Staff(self.obj['staff_member'], self._client, self._company)

    @property
    def site(self):
        """
        :return: Site
        """
        return Site(self.obj['site'], self._client, self._company)

    @property
    def breaks(self):
        """
        :return: Shift[]
        """
        return [Shift(shift, self._client, self._company) for shift in
                self.obj['breaks']]


class Location(BaseObject):
    """
    A geographical location with a latitude and longitude.
    """

    @property
    def latitude(self):
        """
        :return: float
        """
        return self.obj['latitude']

    @property
    def longitude(self):
        """
        :return: float
        """
        return self.obj['longitude']


class Tax(BaseObject):
    """
    Each product can be assigned one or more tax, defined as a code, name, and
    rate.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def code(self):
        """
        :return: str
        """
        return self.obj['code']

    @property
    def name(self):
        """
        :return: str
        """
        return self.obj['name']

    @property
    def rate(self):
        """
        :return: float
        """
        return self.obj['rate']


class IncomeAccountAmount(BaseObject):
    """
    An amount for a given tax type.
    """

    @property
    def tax_id(self):
        """
        :return: int
        """
        return self.obj['tax_id']

    @property
    def net(self):
        """
        :return: float
        """
        return self.obj['net']

    @property
    def tax(self):
        """
        :return: float
        """
        return self.obj['tax']


class Takings(BaseObject):
    """
    Daily takings.
    """

    @property
    def recorded(self):
        """
        :return: float
        """
        return self.obj['recorded']

    @property
    def counted(self):
        """
        :return: float
        """
        return self.obj['counted']


class Adjustments(BaseObject):
    """
    Adjustments to a reconciliation.
    """

    @property
    def cash_in(self):
        """
        :return: float
        """
        return self.obj['cash_in']

    @property
    def cash_out(self):
        """
        :return: float
        """
        return self.obj['cash_out']


class IncomeAccount(BaseObject):
    """
    Income account.
    """

    @property
    def ledger_code(self):
        """
        :return: string
        """
        return self.obj['ledger_code']

    @property
    def amounts(self):
        """
        :return: IncomeAccountAmount[]
        """
        return [IncomeAccountAmount(amount, self._client, self._company)
                for amount in self.obj['amounts']]


class Reconciliation(BaseObject):
    """
    End-of-day reconciliation.
    """

    @property
    def payment_method(self):
        """
        :return: PaymentMethod
        """
        return PaymentMethod(self.obj['payment_method'], self._client,
                             self._company)

    @property
    def takings(self):
        """
        :return: Takings
        """
        return Takings(self.obj['takings'], self._client, self._company)

    @property
    def adjustments(self):
        """
        :return: Adjustments
        """
        return Adjustments(self.obj['adjustments'], self._client, self._company)


class Cashup(BaseObject):
    """
    Cash-ups are end-of-day cash reconcilliations.
    """

    @property
    def id(self):
        """
        :return: int
        """
        return self.obj['id']

    @property
    def number(self):
        """
        :return: int
        """
        return self.obj['number']

    @property
    def processed(self):
        """
        :return: boolean
        """
        return self.obj['processed']

    @property
    def register_level_reconciliation(self):
        """
        :return: boolean
        """
        return self.obj['register_level_reconciliation']

    @property
    def register(self):
        """
        :return: Register
        """
        return Register(self.obj['register'], self._client, self._company)

    @property
    def site(self):
        """
        :return: Site
        """
        return Site(self.obj['site'], self._client, self._company)

    @property
    def staff_member(self):
        """
        :return: Staff
        """
        return Staff(self.obj['staff_member'], self._client, self._company)

    @property
    def income_accounts(self):
        """
        :return: IncomeAccount[]
        """
        return [IncomeAccount(account, self._client, self._company) for account
                in self.obj['income_accounts']]

    @property
    def reconciliations(self):
        """
        :return: Reconciliation[]
        """
        return [Reconciliation(account, self._client, self._company) for account
                in self.obj['reconciliations']]

    @property
    def created_at(self):
        """
        :return: datetime
        """
        return parse(self.obj['created_at'])
