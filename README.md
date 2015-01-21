Kounta
======

Python client library for Kounta.com

```python
from kounta.client import BasicClient

kounta = BasicClient('client_id', 'client_secret')
for site in kounta.company.sites:
    print site.name
```

Objects
-------

### Address

Addresses are physical or postal locations belonging to a staff member,
customer, company or site.

 * `city` - str: City/suburb.
 * `country` - str: Country.
 * `id` - int: Address ID.
 * `lines` - str\[\]: Address lines.
 * `postal_code` - str: Postal code.
 * `zone` - str: Zone/state.

### Category

Each product will belong to one or more categories.

 * `description` - str
 * `id` - int
 * `image` - str
 * `name` - int

### Checkin

Authenticated customers can use checkin service.

 * `customer_id` - int
 * `duration` - int
 * `start_time` - datetime

### Company

Companies are businesses who use Kounta at their points of sale. A company
may have one or more registers running Kounta on one or more sites.

 * `addresses` - [Address\[\]](#address): All addresses attached to this company.
 * `business_number` - str: ABN, ACN or whatever is applicable as the business number.
 * `contact_staff_member` - [Staff](#staff): Contact staff member.
 * `created_at` - datetime: When the company was created.
 * `currency` - str: Currency code.
 * `id` - int: Company ID.
 * `image` - str: Avatar image.
 * `name` - str: Company name.
 * `postal_address` - [Address](#address): Postal address.
 * `registers` - [Register\[\]](#register): Fetch all registers for this company.
 * `shipping_address` - [Address](#address): Shipping address.
 * `sites` - [Site\[\]](#site): Fetch all sites for this company.
 * `timezone` - [Timezone](#timezone): Timezone information.
 * `updated_at` - datetime: When the company was last modified.
 * `website` - str: Website.

### Customer

Customers are people who buy from the authenticated company.

 * `first_name` - str
 * `id` - int
 * `image` - str
 * `last_name` - str
 * `primary_email_address` - str
 * `reference_id` - str

### Inventory

Inventory indicates the quantity for a given product.

 * `id` - int
 * `stock` - int

### Line

Lines (also called order lines, sale lines or line items) describe the
products included in an order.

 * `modifiers` - int\[\]
 * `notes` - str
 * `number` - int: The line number. This will start with `1`.
 * `price_variation` - float
 * `product_id` - int
 * `quantity` - int
 * `unit_price` - float

### Location

A geographical location with a latitude and longitude.

 * `latitude` - float
 * `longitude` - float

### Order

Orders are also sometimes called sales or invoices.

 * `created_at` - datetime
 * `id` - int
 * `paid` - float
 * `status` - str
 * `total_tax` - float
 * `total` - float
 * `updated_at` - datetime

### Payment

Payments (also called transactions) are financial transactions related to an
order.

 * `amount` - float
 * `method_id` - int
 * `ref` - str

### PaymentMethod

Payment methods are assigned to order payments.

 * `id` - int
 * `ledger_code` - str
 * `name` - str

### Permission
 * `code` - str
 * `domain` - str
 * `name` - str

### PriceList

Each site will be assigned a price list that determines ex tax unit prices
of each item on sale.

Price lists work by overriding prices in their parent lists (just like
subclassing in object-oriented programming). The base price list has a
parent_id of null.

 * `id` - int
 * `name` - str
 * `parent_id` - int

### Product

Products are saleable items in your inventory, including modifier products.

 * `barcode` - str
 * `code` - str
 * `description` - str
 * `id` - int
 * `name` - int

### Register

Registers are iPads or other computers running Kounta.

 * `code` - str
 * `id` - int
 * `name` - str
 * `site_id` - int

### Shift

Shifts record staff check-ins, check-outs and breaks.

 * `breaks` - [Shift\[\]](#shift)
 * `site` - [Site](#site)
 * `staff_member` - [Staff](#staff)

### ShiftPeriod

Represents a block of time when dealing with `Shift`s.

 * `finished_at` - datetime
 * `period` - timedelta: The timedelta between the start anf finish time.
 * `started_at` - datetime

### Site

Sites are physical locations, such as outlets, offices etc, at which one or
more Kountas will be used.

 * `business_number` - str
 * `code` - str
 * `contact_person` - [Staff](#staff)
 * `created_at` - datetime
 * `email` - str
 * `fax` - str
 * `id` - int
 * `image` - str
 * `location` - [Location](#location)
 * `mobile` - str
 * `name` - str
 * `phone` - str
 * `postal_address` - [Address](#address)
 * `price_list` - [PriceList](#pricelist)
 * `register_level_reconciliation` - boolean
 * `shipping_address` - [Address](#address)
 * `updated_at` - datetime
 * `website` - str

### Staff

Staff members are people who work for the authenticated company.

 * `created_at` - str
 * `email_addresses` - str\[\]
 * `fax` - str
 * `first_name` - str
 * `id` - int
 * `image` - str
 * `is_admin` - boolean
 * `last_name` - str
 * `mobile` - str
 * `permissions` - [Permission\[\]](#permission)
 * `phone` - str
 * `postal_address` - [Address](#address)
 * `primary_email_address` - str
 * `shipping_address` - [Address](#address)
 * `updated_at` - str

### Tax

Each product can be assigned one or more tax, defined as a code, name, and
rate.

 * `code` - str
 * `id` - int
 * `name` - str
 * `rate` - float

### Timezone

A timezone represents a time offset at a geographical location.

 * `name` - str
 * `offset` - str
