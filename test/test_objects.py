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


class TestLine(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/line.json', 'r').read())
        self.line = Line(obj, self.client)

    def test_number(self):
        self.assertEqual(self.line.number, 1)

    def test_product_id(self):
        self.assertEqual(self.line.product_id, 8710)

    def test_quantity(self):
        self.assertEqual(self.line.quantity, 1)

    def test_notes(self):
        self.assertEqual(self.line.notes, '15% surcharge for public holiday')

    def test_unit_price(self):
        self.assertEqual(self.line.unit_price, 1.3636)

    def test_price_variation(self):
        self.assertEqual(self.line.price_variation, 1.15)

    def test_modifiers(self):
        self.assertEqual(self.line.modifiers, [-67])


class TestOrder(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/order.json', 'r').read())
        self.order = Order(obj, self.client)

    def test_id(self):
        self.assertEqual(self.order.id, 912387093)

    def test_status(self):
        self.assertEqual(self.order.status, 'PENDING')

    def test_total(self):
        self.assertEqual(self.order.total, 45.65)

    def test_total_tax(self):
        self.assertEqual(self.order.total_tax, 4.15)

    def test_paid(self):
        self.assertEqual(self.order.paid, 0)

    def test_created_at(self):
        self.assertEqual(self.order.created_at,
                         parse("2013-06-02T14:22:08+10:00"))

    def test_updated_at(self):
        self.assertEqual(self.order.updated_at,
                         parse("2013-06-02T14:22:08+10:00"))


class TestPaymentMethod(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/payment_method.json', 'r').read())
        self.payment_method = PaymentMethod(obj, self.client)

    def test_id(self):
        self.assertEqual(self.payment_method.id, 1)

    def test_name(self):
        self.assertEqual(self.payment_method.name, 'Cash')

    def test_ledger_code(self):
        self.assertEqual(self.payment_method.ledger_code, '200')


class TestPayment(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/payment.json', 'r').read())
        self.payment = Payment(obj, self.client)

    def test_method_id(self):
        self.assertEqual(self.payment.method_id, 12)

    def test_amount(self):
        self.assertEqual(self.payment.amount, 14.25)

    def test_ref(self):
        self.assertEqual(self.payment.ref, 'INV2-8M9F-B8UN-YQ5S-2G7K')


class TestPriceList(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/price_list.json', 'r').read())
        self.price_list = PriceList(obj, self.client)

    def test_id(self):
        self.assertEqual(self.price_list.id, 201)

    def test_name(self):
        self.assertEqual(self.price_list.name, 'Base Prices')

    def test_parent_id(self):
        self.assertEqual(self.price_list.parent_id, None)


class TestRegister(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/register.json', 'r').read())
        self.register = Register(obj, self.client)

    def test_id(self):
        self.assertEqual(self.register.id, 9091)

    def test_code(self):
        self.assertEqual(self.register.code, 'T1')

    def test_name(self):
        self.assertEqual(self.register.name, 'Terminal 1')

    def test_site_id(self):
        self.assertEqual(self.register.site_id, 985)
