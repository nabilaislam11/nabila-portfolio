# ShelfWise — Book Shop Management System

A Python/Flask implementation of a bookshop management system featuring cataloguing, inventory, customers, and sales.

## Features

- Admin and staff authentication
- ISBN-aware book catalogue and stock records
- Customer management
- Multi-item sales and invoice views
- Discount and tax calculations using Decimal
- Stock movement tracking and inventory checks

## Technology

Python · Flask · SQLAlchemy · SQLite

## Local setup

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
flask --app run.py create-admin
python run.py
```

Open `http://127.0.0.1:5000`. The application creates its local database tables through the application factory.

## Automated tests

Six GitHub Actions tests cover financial calculations, stock adjustments, invalid sale quantities, and authenticated page rendering. Source and tests are organized under `app/` and `tests/`.

## Related academic coursework

The [Advanced Book Shop Management System](../02-advanced-book-shop/README.md) is the original PHP/MySQL CSE370 group project. ShelfWise is a separate Python/Flask implementation covering bookshop administration and sales concepts.
