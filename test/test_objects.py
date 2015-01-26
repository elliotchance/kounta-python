from unittest import TestCase
from kounta.objects import *
from kounta.client import BasicClient
from mock import MagicMock
import json
import datetime


class BaseObjectTestCase(TestCase):
    def setUp(self):
        self.client = BasicClient('', '')

    def get_company(self):
        """
        :rtype : Company
        """
        obj = json.loads(open('test/company.json', 'r').read())
        return Company(obj, self.client, None)


class TestBaseObject(BaseObjectTestCase):
    def test_nonexistent_property(self):
        obj = json.loads('{"foo":"bar"}')
        address = BaseObject(obj, self.client, None)
        self.assertEqual(address.foo, "bar")


class TestAddress(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/address.json', 'r').read())
        self.address = Address(obj, self.client, None)

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
        self.company = self.get_company()

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
        # noinspection PyStatementEffect
        self.company.sites
        url = '/v1/companies/5678/sites.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_registers_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.company.registers
        url = '/v1/companies/5678/registers.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_addresses_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.company.addresses
        url = '/v1/companies/5678/addresses.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_cashups_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.company.cashups()
        url = '/v1/companies/5678/cashups.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_cashups_uses_generator(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.company.cashups(unprocessed=True)
        url = '/v1/companies/5678/cashups/unprocessed.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_categories_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.company.categories
        url = '/v1/companies/5678/categories.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)


class TestCategory(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/category.json', 'r').read())
        self.category = Category(obj, self.client, None)

    def test_id(self):
        self.assertEqual(self.category.id, 8263)

    def test_name(self):
        self.assertEqual(self.category.name, "Fruit & Vegetables")

    def test_description(self):
        self.assertEqual(self.category.description,
                         "Fresh fruit and veg from local and imported sources")

    def test_image(self):
        self.assertEqual(self.category.image, None)


class TestProduct(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/product.json', 'r').read())
        self.product = Product(obj, self.client, None)

    def test_id(self):
        self.assertEqual(self.product.id, 3928147)

    def test_name(self):
        self.assertEqual(self.product.name, "Egg Carton")

    def test_description(self):
        self.assertEqual(self.product.description,
                         "12 \"Free Range\" Eggs in a carton.")

    def test_code(self):
        self.assertEqual(self.product.code, 'egg298')

    def test_barcode(self):
        self.assertEqual(self.product.barcode, '1234567890')


class TestCheckin(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/checkin.json', 'r').read())
        self.checkin = Checkin(obj, self.client, None)

    def test_customer_id(self):
        self.assertEqual(self.checkin.customer_id, 389427)

    def test_start_time(self):
        self.assertEqual(self.checkin.start_time,
                         parse("2014-05-21T17:23:52+10:00"))

    def test_duration(self):
        self.assertEqual(self.checkin.duration, 120)


class TestCustomer(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/customer.json', 'r').read())
        self.customer = Customer(obj, self.client, self.get_company())

    def test_id(self):
        self.assertEqual(self.customer.id, 389427)

    def test_first_name(self):
        self.assertEqual(self.customer.first_name, 'Jamie')

    def test_last_name(self):
        self.assertEqual(self.customer.last_name, 'McDonald')

    def test_primary_email_address(self):
        self.assertEqual(self.customer.primary_email_address,
                         'jamie@kounta.kom')

    def test_image(self):
        image = 'http://www.gravatar.com/avatar/c.jpg'
        self.assertEqual(self.customer.image, image)

    def test_reference_id(self):
        self.assertEqual(self.customer.reference_id, '')

    def test_addresses_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.customer.addresses
        url = '/v1/companies/5678/customer/389427/addresses.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)


class TestInventory(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/inventory.json', 'r').read())
        self.inventory = Inventory(obj, self.client, None)

    def test_id(self):
        self.assertEqual(self.inventory.id, 829)

    def test_stock(self):
        self.assertEqual(self.inventory.stock, 12)


class TestLine(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/line.json', 'r').read())
        self.line = Line(obj, self.client, None)

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
        self.order = Order(obj, self.client, None)

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
        self.payment_method = PaymentMethod(obj, self.client, None)

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
        self.payment = Payment(obj, self.client, None)

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
        self.price_list = PriceList(obj, self.client, None)

    def test_id(self):
        self.assertEqual(self.price_list.id, 201)

    def test_name(self):
        self.assertEqual(self.price_list.name, 'Base Prices')

    def test_parent_id(self):
        self.assertEqual(self.price_list.parent_id, None)


class TestRegister(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        company = self.get_company()
        obj = json.loads(open('test/register.json', 'r').read())
        self.register = Register(obj, self.client, company)

    def test_id(self):
        self.assertEqual(self.register.id, 9091)

    def test_code(self):
        self.assertEqual(self.register.code, 'T1')

    def test_name(self):
        self.assertEqual(self.register.name, 'Terminal 1')

    def test_site_id(self):
        self.assertEqual(self.register.site_id, 985)

    def test_cashups_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.register.cashups(unprocessed = True, since = '2013-04-29')
        url = '/v1/companies/5678/registers/9091/' + \
              'cashups/unprocessed/since/2013-04-29.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)


class TestShiftPeriod(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/shift_period.json', 'r').read())
        self.shift_period = ShiftPeriod(obj, self.client, None)

    def test_started_at(self):
        self.assertEqual(self.shift_period.started_at,
                         parse("2013-04-29T12:28:01+11:00"))

    def test_finished_at(self):
        self.assertEqual(self.shift_period.finished_at,
                         parse('2013-04-29T12:45:55+11:00'))

    def test_period(self):
        self.assertEqual(self.shift_period.period,
                         datetime.timedelta(-1, 85326))


class TestShift(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/shift.json', 'r').read())
        self.shift = Shift(obj, self.client, None)

    def test_staff_member(self):
        self.assertTrue(isinstance(self.shift.staff_member, Staff))
        self.assertEqual(self.shift.staff_member.id, 9022)

    def test_site(self):
        self.assertTrue(isinstance(self.shift.site, Site))
        self.assertEqual(self.shift.site.id, 208)

    def test_started_at(self):
        self.assertEqual(self.shift.started_at,
                         parse("2013-04-29T09:03:18+11:00"))

    def test_finished_at(self):
        self.assertEqual(self.shift.finished_at,
                         parse('2013-04-29T19:22:40+11:00'))

    def test_breaks(self):
        self.assertEqual(len(self.shift.breaks), 2)
        self.assertEqual(self.shift.breaks[0].started_at,
                         parse('2013-04-29T12:28:01+11:00'))


class TestSite(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/site.json', 'r').read())
        self.site = Site(obj, self.client, self.get_company())

    def test_id(self):
        self.assertEqual(self.site.id, 923)

    def test_name(self):
        self.assertEqual(self.site.name, 'Head Office')

    def test_code(self):
        self.assertEqual(self.site.code, 'AU-HO')

    def test_contact_person(self):
        self.assertTrue(isinstance(self.site.contact_person, Staff))
        self.assertEquals(self.site.contact_person.id, 92402)

    def test_business_number(self):
        self.assertEqual(self.site.business_number, '12 345 678 910')

    def test_shipping_address(self):
        self.assertTrue(isinstance(self.site.shipping_address, Address))
        self.assertEquals(self.site.shipping_address.id, 198109)

    def test_postal_address(self):
        self.assertEquals(self.site.postal_address, None)

    def test_email(self):
        self.assertEqual(self.site.email, 'au@kounta.com')

    def test_mobile(self):
        self.assertEqual(self.site.mobile, '412 555 0189')

    def test_phone(self):
        self.assertEqual(self.site.phone, '')

    def test_fax(self):
        self.assertEqual(self.site.fax, '')

    def test_location(self):
        self.assertTrue(isinstance(self.site.location, Location))
        self.assertEquals(self.site.location.latitude, 23.7861)

    def test_image(self):
        self.assertEqual(self.site.image,
                         'http://www.gravatar.com/avatar/c.jpg')

    def test_website(self):
        self.assertEqual(self.site.website, 'http://kounta.com')

    def test_register_level_reconciliation(self):
        self.assertEqual(self.site.register_level_reconciliation, True)

    def test_price_list(self):
        self.assertTrue(isinstance(self.site.price_list, PriceList))
        self.assertEquals(self.site.price_list.id, 3278)

    def test_created_at(self):
        self.assertEqual(self.site.created_at,
                         parse('2013-05-08T13:56:02+10:00'))

    def test_updated_at(self):
        self.assertEqual(self.site.updated_at,
                         parse('2013-05-22T16:21:40+10:00'))

    def test_addresses_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.site.addresses
        url = '/v1/companies/5678/sites/923/addresses.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_cashups_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.site.cashups(unprocessed = True, at = '2013-04-29')
        url = '/v1/companies/5678/sites/923/cashups/unprocessed/2013-04-29.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)

    def test_categories_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.site.categories
        url = '/v1/companies/5678/sites/923/categories.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)


class TestLocation(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/location.json', 'r').read())
        self.location = Location(obj, self.client, None)

    def test_latitude(self):
        self.assertEqual(self.location.latitude, 23.7861)

    def test_longitude(self):
        self.assertEqual(self.location.longitude, 14.927)


class TestStaff(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/staff.json', 'r').read())
        self.staff = Staff(obj, self.client, self.get_company())

    def test_id(self):
        self.assertEqual(self.staff.id, 389427)

    def test_first_name(self):
        self.assertEqual(self.staff.first_name, 'Jamie')

    def test_last_name(self):
        self.assertEqual(self.staff.last_name, 'McDonald')

    def test_is_admin(self):
        self.assertEqual(self.staff.is_admin, False)

    def test_primary_email_address(self):
        self.assertEqual(self.staff.primary_email_address, 'jamie@kounta.kom')

    def test_email_addresses(self):
        self.assertEqual(self.staff.email_addresses, [
            "jamie@kounta.kom",
            "jamie112783@hotmail.kom"
        ])

    def test_phone(self):
        self.assertEqual(self.staff.phone, '+612 8765 4321')

    def test_mobile(self):
        self.assertEqual(self.staff.mobile, '0405 060 708')

    def test_fax(self):
        self.assertEqual(self.staff.fax, None)

    def test_postal_address(self):
        self.assertTrue(isinstance(self.staff.postal_address, Address))
        self.assertEquals(self.staff.postal_address.id, 198109)

    def test_shipping_address(self):
        self.assertEquals(self.staff.shipping_address, None)

    def test_permissions(self):
        self.assertEquals(len(self.staff.permissions), 2)
        self.assertTrue(isinstance(self.staff.permissions[0], Permission))
        self.assertEquals(self.staff.permissions[0].code, 'FinishSale')

    def test_image(self):
        self.assertEqual(self.staff.image,
                         'http://www.gravatar.com/avatar/c.jpg')

    def test_created_at(self):
        self.assertEqual(self.staff.created_at,
                         parse('2013-05-08T13:56:02+10:00'))

    def test_updated_at(self):
        self.assertEqual(self.staff.updated_at,
                         parse('2013-05-22T16:21:40+10:00'))

    def test_addresses_calls_api(self):
        self.client.get_url = MagicMock(return_value='[]')
        # noinspection PyStatementEffect
        self.staff.addresses
        url = '/v1/companies/5678/staff/389427/addresses.json'
        # noinspection PyUnresolvedReferences
        self.client.get_url.assert_called_once_with(url)


class TestTax(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/tax.json', 'r').read())
        self.tax = Tax(obj, self.client, None)

    def test_id(self):
        self.assertEqual(self.tax.id, 829)

    def test_code(self):
        self.assertEqual(self.tax.code, 'GST')

    def test_name(self):
        self.assertEqual(self.tax.name, "Goods & Services Tax")

    def test_rate(self):
        self.assertEqual(self.tax.rate, 0.1)


class TestIncomeAccountAmount(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/income_account_amount.json', 'r').read())
        self.income_account_amount = IncomeAccountAmount(obj, self.client, None)

    def test_tax_id(self):
        self.assertEqual(self.income_account_amount.tax_id, 829)

    def test_net(self):
        self.assertEqual(self.income_account_amount.net, 45.45)

    def test_tax(self):
        self.assertEqual(self.income_account_amount.tax, 4.54)


class TestTakings(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/takings.json', 'r').read())
        self.takings = Takings(obj, self.client, None)

    def test_recorded(self):
        self.assertEqual(self.takings.recorded, 1424.65)

    def test_counted(self):
        self.assertEqual(self.takings.counted, 1415.8)


class TestAdjustments(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/adjustments.json', 'r').read())
        self.adjustments = Adjustments(obj, self.client, None)

    def test_cash_in(self):
        self.assertEqual(self.adjustments.cash_in, 20)

    def test_cash_out(self):
        self.assertEqual(self.adjustments.cash_out, 75.4)


class TestIncomeAccount(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/income_account.json', 'r').read())
        self.income_account = IncomeAccount(obj, self.client, None)

    def test_ledger_code(self):
        self.assertEqual(self.income_account.ledger_code, '200')

    def test_amounts(self):
        amounts = self.income_account.amounts
        self.assertEqual(len(amounts), 2)
        self.assertTrue(isinstance(amounts[0], IncomeAccountAmount))
        self.assertEqual(amounts[0].tax_id, 829)


class TestReconciliation(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/reconciliation.json', 'r').read())
        self.reconciliation = Reconciliation(obj, self.client, None)

    def test_payment_method(self):
        payment_method = self.reconciliation.payment_method
        self.assertTrue(isinstance(payment_method, PaymentMethod))
        self.assertEqual(payment_method.id, 1)

    def test_takings(self):
        takings = self.reconciliation.takings
        self.assertTrue(isinstance(takings, Takings))
        self.assertEqual(takings.recorded, 1424.65)

    def test_adjustments(self):
        adjustments = self.reconciliation.adjustments
        self.assertTrue(isinstance(adjustments, Adjustments))
        self.assertEqual(adjustments.cash_in, 20)


class TestCashup(BaseObjectTestCase):
    def setUp(self):
        BaseObjectTestCase.setUp(self)
        obj = json.loads(open('test/cashup.json', 'r').read())
        self.cashup = Cashup(obj, self.client, None)

    def test_id(self):
        self.assertEqual(self.cashup.id, 19762)

    def test_(self):
        self.assertEqual(self.cashup.number, 27)

    def test_processed(self):
        self.assertEqual(self.cashup.processed, False)

    def test_register_level_reconciliation(self):
        self.assertEqual(self.cashup.register_level_reconciliation, True)

    def test_register(self):
        register = self.cashup.register
        self.assertTrue(isinstance(register, Register))
        self.assertEqual(register.id, 9091)

    def test_site(self):
        site = self.cashup.site
        self.assertTrue(isinstance(site, Site))
        self.assertEqual(site.id, 985)

    def test_staff_member(self):
        staff_member = self.cashup.staff_member
        self.assertTrue(isinstance(staff_member, Staff))
        self.assertEqual(staff_member.id, 389427)

    def test_income_accounts(self):
        income_accounts = self.cashup.income_accounts
        self.assertEqual(len(income_accounts), 1)
        self.assertTrue(isinstance(income_accounts[0], IncomeAccount))
        self.assertEqual(income_accounts[0].ledger_code, '200')

    def test_reconciliations(self):
        reconciliations = self.cashup.reconciliations
        self.assertEqual(len(reconciliations), 2)
        self.assertTrue(isinstance(reconciliations[0], Reconciliation))
        self.assertEqual(reconciliations[0].payment_method.id, 1)

    def test_created_at(self):
        self.assertEqual(self.cashup.created_at,
                         parse('2013-04-29T20:08:21+11:00'))
