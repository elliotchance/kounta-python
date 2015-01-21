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

 * `city` (string): City/suburb.
 * `zone` (string): Zone/state.
 * `country` (string): Country.
 * `lines` (string\[\]): Address lines.
 * `id` (integer): Address ID.
 * `postal_code` (string): Postal code.

### Category

Each product will belong to one or more categories.

 * `description` (str)
 * `image` (str)
 * `id` (int)
 * `name` (int)

### Checkin

Authenticated customers can use checkin service.

 * `duration` (int)
 * `customer_id` (int)
 * `start_time` (datetime)

### Company

Companies are businesses who use Kounta at their points of sale. A company
may have one or more registers running Kounta on one or more sites.

 * `website` (string): Website.
 * `created_at` (datetime): When the company was created.
 * `name` (string): Company name.
 * `postal_address` (Address): Postal address.
 * `updated_at` (datetime): When the company was last modified.
 * `image` (string): Avatar image.
 * `sites` (list): Fetch all sites for this company.
 * `id` (integer): Company ID.
 * `currency` (string): Currency code.
 * `registers` (list): Fetch all registers for this company.
 * `business_number` (string): ABN, ACN or whatever is applicable as the business number.
 * `shipping_address` (Address): Shipping address.
 * `timezone` (Timezone): Timezone information.
 * `contact_staff_member` (Staff): Contact staff member.
 * `addresses` (list): All addresses attached to this company.

### Customer

Customers are people who buy from the authenticated company.

 * `last_name` (str)
 * `image` (str)
 * `first_name` (str)
 * `id` (int)
 * `primary_email_address` (str)
 * `reference_id` (str)

### Inventory

Inventory indicates the quantity for a given product.

 * `stock` (int)
 * `id` (int)

### Line

Lines (also called order lines, sale lines or line items) describe the
products included in an order.

 * `modifiers` (list)
 * `product_id` (int)
 * `notes` (str)
 * `number` (int): The line number. This will start with `1`.
 * `unit_price` (float)
 * `price_variation` (float)
 * `quantity` (int)

### Location

A geographical location with a latitude and longitude.

 * `latitude` (float)
 * `longitude` (float)

### Order

Orders are also sometimes called sales or invoices.

 * `status` (str)
 * `total_tax` (float)
 * `created_at` (datetime)
 * `updated_at` (datetime)
 * `paid` (float)
 * `id` (int)
 * `total` (float)

### Payment

Payments (also called transactions) are financial transactions related to an
order.

 * `amount` (float)
 * `ref` (str)
 * `method_id` (int)

### PaymentMethod

Payment methods are assigned to order payments.

 * `ledger_code` (str)
 * `name` (str)
 * `id` (int)

### Permission
 * `code` (string)
 * `name` (string)
 * `domain` (string)

### PriceList

Each site will be assigned a price list that determines ex tax unit prices
of each item on sale.

Price lists work by overriding prices in their parent lists (just like
subclassing in object-oriented programming). The base price list has a
parent_id of null.

 * `parent_id` (int)
 * `name` (str)
 * `id` (int)

### Product

Products are saleable items in your inventory, including modifier products.

 * `code` (str)
 * `description` (str)
 * `barcode` (str)
 * `id` (int)
 * `name` (int)

### Register

Registers are iPads or other computers running Kounta.

 * `code` (str)
 * `name` (str)
 * `site_id` (int)
 * `id` (int)

### Shift

Shifts record staff check-ins, check-outs and breaks.

 * `site` (Site)
 * `breaks` (list)
 * `staff_member` (kounta.objects.Staff)

### ShiftPeriod

Represents a block of time when dealing with `Shift`s.

 * `finished_at` (datetime)
 * `started_at` (datetime)
 * `period` (timedelta): The timedelta between the start anf finish time.

### Site

Sites are physical locations, such as outlets, offices etc, at which one or
more Kountas will be used.

 * `website` (str)
 * `created_at` (datetime)
 * `code` (str)
 * `name` (str)
 * `postal_address` (Address)
 * `phone` (str)
 * `mobile` (str)
 * `image` (str)
 * `price_list` (PriceList)
 * `fax` (str)
 * `id` (int)
 * `updated_at` (datetime)
 * `email` (str)
 * `register_level_reconciliation` (boolean)
 * `business_number` (str)
 * `shipping_address` (Address)
 * `contact_person` (Staff)
 * `location` (Location)

### Staff

Staff members are people who work for the authenticated company.

 * `created_at` (str)
 * `last_name` (str)
 * `fax` (str)
 * `postal_address` (Address)
 * `mobile` (str)
 * `image` (str)
 * `first_name` (str)
 * `id` (int)
 * `updated_at` (str)
 * `phone` (str)
 * `primary_email_address` (str)
 * `is_admin` (boolean)
 * `shipping_address` (Address)
 * `email_addresses` (str\[\])
 * `permissions` (Permission\[\])

### Tax

Each product can be assigned one or more tax, defined as a code, name, and
rate.

 * `code` (str)
 * `name` (str)
 * `id` (int)
 * `rate` (float)

### Timezone

A timezone represents a time offset at a geographical location.

 * `name` (string)
 * `offset` (string)
