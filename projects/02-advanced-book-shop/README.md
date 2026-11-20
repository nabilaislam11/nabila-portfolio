# Advanced Book Shop Management System

**Technologies:** PHP, MySQL/MariaDB, HTML, CSS, JavaScript, XAMPP

A browser-based bookshop ordering and delivery management system developed as a collaborative academic project. The application covers customer-facing shopping workflows and an administrative interface for catalogue, inventory, orders, and sales management.

## System components

- Customer accounts and book catalogue
- Categories and inventory management
- Shopping cart and order processing
- Administrative views for products and orders
- Relational database design for customers, inventory, products, orders, and order items

## Database design

The academic database contains 11 relational tables: `products`, `categories`, `sub_categories`, `inventory`, `clients`, `users`, `cart`, `orders`, `order_list`, `sales`, and `system_info`. Its table definitions and key constraints are available in the local SQL schema.

## Project materials

- [Original PHP application repository](https://github.com/Khandaker-Atik/Book_shop_management)
- [Database schema extracted from the academic SQL project](sql/schema.sql)
- [Relational database design and transaction workflows](docs/database-design.md)
- [Browse the original PHP application components](docs/php-source-guide.md)
- [Project overview on the portfolio website](index.html)

## Local development

Install a local PHP and MariaDB/MySQL environment such as XAMPP. The original application is configured for the `book_shop` application directory and `book_shop_db` database. For its complete PHP source and setup, use the linked application repository. The schema in this directory provides a convenient SQL reference without bundled sample accounts or customer rows.

## Related software work

[ShelfWise](../02-shelfwise/README.md) is a separate Flask/SQLAlchemy implementation of bookshop administration concepts, with its own source and automated tests.
