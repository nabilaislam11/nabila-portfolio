# Advanced Book Shop — PHP Source Guide

The PHP/MySQL bookshop management application with customer shopping pages and administrative workflows. The following links open the original group-project implementation directly.

| Component | PHP source | Role |
| --- | --- | --- |
| Web entry point | [index.php](https://github.com/Khandaker-Atik/Book_shop_management/blob/main/index.php) | Main storefront routing and views |
| Catalogue | [products.php](https://github.com/Khandaker-Atik/Book_shop_management/blob/main/products.php) | Book browsing |
| Product detail | [view_product.php](https://github.com/Khandaker-Atik/Book_shop_management/blob/main/view_product.php) | Product details |
| Shopping cart | [cart.php](https://github.com/Khandaker-Atik/Book_shop_management/blob/main/cart.php) | Customer cart |
| Checkout | [checkout.php](https://github.com/Khandaker-Atik/Book_shop_management/blob/main/checkout.php) | Order submission |
| Database connection | [DBConnection.php](https://github.com/Khandaker-Atik/Book_shop_management/blob/main/classes/DBConnection.php) | MySQL connection |
| Application services | [Master.php](https://github.com/Khandaker-Atik/Book_shop_management/blob/main/classes/Master.php) | Business operations |
| Book administration | [admin/product](https://github.com/Khandaker-Atik/Book_shop_management/tree/main/admin/product) | Product management |
| Stock management | [admin/inventory](https://github.com/Khandaker-Atik/Book_shop_management/tree/main/admin/inventory) | Inventory operations |
| Orders | [admin/orders](https://github.com/Khandaker-Atik/Book_shop_management/tree/main/admin/orders) | Order records and status |
| Sales | [admin/sales](https://github.com/Khandaker-Atik/Book_shop_management/tree/main/admin/sales) | Transaction reporting |
| Database export | [book_shop_db.sql](https://github.com/Khandaker-Atik/Book_shop_management/blob/main/database/book_shop_db.sql) | Database tables and sample application records |

## Local academic materials

- [SQL schema](../sql/schema.sql) — 11 table definitions, indexes and auto-increment settings
- [Database architecture and business workflows](database-design.md)
- [Academic project overview](../README.md)

The schema included in this portfolio contains database definitions without seeded personal records.
