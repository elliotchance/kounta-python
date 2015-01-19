from unittest import TestCase
from kounta.objects import *
from kounta.client import BasicClient
from mock import MagicMock
import json


class BaseObjectTestCase(TestCase):
    def setUp(self):
        self.client = BasicClient('', '')


class TestBaseObject(BaseObjectTestCase):
    def test_nonexistent_property(self):
        obj = json.loads('{"foo":"bar"}')
        address = BaseObject(obj, self.client)
        self.assertEqual(address.foo, "bar")


class TestAddress(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/address.json', 'r').read())
        self.address = Address(obj, self.client)

    def test_id(self):
        self.assertEqual(self.address.id, 198109)

    def test_city(self):
        self.assertEqual(self.address.city, "Beeftown")

    def test_lines(self):
        self.assertEqual(len(self.address.lines), 2)
        self.assertEqual(self.address.lines[0], "Suite 5, Level 12")
        self.assertEqual(self.address.lines[1], "44 Mutton Street")

    def test_zone(self):
        self.assertEqual(self.address.zone, "NSW")

    def test_postal_code(self):
        self.assertEqual(self.address.postal_code, "2112")

    def test_country(self):
        self.assertEqual(self.address.country, "AU")


class TestCompany(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/company.json', 'r').read())
        self.company = Company(obj, self.client)

    def test_id(self):
        self.assertEqual(self.company.id, 5678)

    def test_name(self):
        self.assertEqual(self.company.name, "Rockin' & Rollin' Again")

    def test_shipping_address(self):
        self.assertEqual(self.company.shipping_address, None)

    def test_postal_address(self):
        postal_address = self.company.postal_address
        self.assertTrue(isinstance(postal_address, Address))
        self.assertEqual(postal_address.id, 198109)

    def test_business_number(self):
        self.assertEqual(self.company.business_number, "63 987 012 468")

    def test_contact_staff_member(self):
        contact_staff_member = self.company.contact_staff_member
        self.assertTrue(isinstance(contact_staff_member, Staff))
        self.assertEqual(contact_staff_member.id, 92402)

    def test_image(self):
        image = ("http://www.gravatar.com/avatar/"
            "b8e42a8b1eb5967f80bf085adb97d613.jpg")
        self.assertEqual(self.company.image, image)

    def test_website(self):
        self.assertEqual(self.company.website, "http://rara.kom")

    def test_currency(self):
        self.assertEqual(self.company.currency, "AUD")

    def test_timezone(self):
        timezone = self.company.timezone
        self.assertTrue(isinstance(timezone, Timezone))
        self.assertEqual(timezone.offset, '+10:00')
        self.assertEqual(timezone.name, 'Australia/Melbourne')

    def test_created_at(self):
        self.assertEqual(self.company.created_at,
                         parse("2013-05-08T13:56:02+10:00"))

    def test_updated_at(self):
        self.assertEqual(self.company.updated_at,
                         parse("2013-05-22T16:21:40+10:00"))

    def test_sites_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        self.company.sites
        url = '/v1/companies/5678/sites.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_registers_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        self.company.registers
        url = '/v1/companies/5678/registers.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_addresses_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        self.company.addresses
        url = '/v1/companies/5678/addresses.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)


class TestCategory(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/category.json', 'r').read())
        self.category = Category(obj, self.client)

    def test_id(self):
        self.assertEqual(self.category.id, 8263)

    def test_name(self):
        self.assertEqual(self.category.name, "Fruit & Vegetables")

    def test_description(self):
        self.assertEqual(self.category.description, "Fresh fruit and veg from local and imported sources")

    def test_image(self):
        self.assertEqual(self.category.image, None)


class TestProduct(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/product.json', 'r').read())
        self.product = Product(obj, self.client)

    def test_id(self):
        self.assertEqual(self.product.id, 3928147)

    def test_name(self):
        self.assertEqual(self.product.name, "Egg Carton")

    def test_description(self):
        self.assertEqual(self.product.description, "12 \"Free Range\" Eggs in a carton.")

    def test_code(self):
        self.assertEqual(self.product.code, 'egg298')

    def test_barcode(self):
        self.assertEqual(self.product.barcode, '1234567890')


class TestCheckin(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/checkin.json', 'r').read())
        self.checkin = Checkin(obj, self.client)

    def test_customer_id(self):
        self.assertEqual(self.checkin.customer_id, 389427)

    def test_start_time(self):
        self.assertEqual(self.checkin.start_time, parse("2014-05-21T17:23:52+10:00"))

    def test_duration(self):
        self.assertEqual(self.checkin.duration, 120)


class TestCustomer(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/customer.json', 'r').read())
        self.customer = Checkin(obj, self.client)

    def test_id(self):
        self.assertEqual(self.customer.id, 389427)

    def test_first_name(self):
        self.assertEqual(self.customer.first_name, 'Jamie')

    def test_last_name(self):
        self.assertEqual(self.customer.last_name, 'McDonald')

    def test_primary_email_address(self):
        self.assertEqual(self.customer.primary_email_address, 'jamie@kounta.kom')

    def test_image(self):
        image = 'http://www.gravatar.com/avatar/c.jpg'
        self.assertEqual(self.customer.image, image)

    def test_reference_id(self):
        self.assertEqual(self.customer.reference_id, '')


class TestInventory(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/inventory.json', 'r').read())
        self.inventory = Inventory(obj, self.client)

    def test_id(self):
        self.assertEqual(self.inventory.id, 829)

    def test_stock(self):
        self.assertEqual(self.inventory.stock, 12)
