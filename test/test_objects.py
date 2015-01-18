from unittest import TestCase
from kounta.objects import *
import json

class TestBaseObject(TestCase):
    def test_nonexistent_property(self):
        obj = json.loads('{"foo":"bar"}')
        address = BaseObject(obj)
        self.assertEqual(address.foo, "bar")

class TestAddress(TestCase):
    def setUp(self):
        obj = json.loads(open('test/address.json', 'r').read())
        self.address = Address(obj)

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

class TestCompany(TestCase):
    def setUp(self):
        obj = json.loads(open('test/company.json', 'r').read())
        self.company = Company(obj)

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

    def test_addresses(self):
        self.assertEqual(self.company.addresses['count'], 3)
        self.assertEqual(self.company.addresses['updated_at'],
                         parse('2013-05-22T16:21:40+10:00'))

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

    def test_sites(self):
        self.assertEqual(self.company.sites['count'], 3)
        self.assertEqual(self.company.sites['updated_at'],
                         parse('2013-05-24T16:24:13+10:00'))

    def test_registers(self):
        self.assertEqual(self.company.registers['count'], 12)
        self.assertEqual(self.company.registers['limit'], 15)
        self.assertEqual(self.company.registers['updated_at'],
                         parse('2013-05-22T12:18:44+10:00'))

    def test_created_at(self):
        self.assertEqual(self.company.created_at,
                         parse("2013-05-08T13:56:02+10:00"))

    def test_updated_at(self):
        self.assertEqual(self.company.updated_at,
                         parse("2013-05-22T16:21:40+10:00"))
