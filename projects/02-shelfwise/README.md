# Advanced Book Shop Management System

A reconstructed reference application inspired by the academic project title **Advanced Book Shop Management System**.

## Reference implementation

- Python, Flask, SQLAlchemy and SQLite
- Admin and staff authentication
- Book catalogue with ISBN uniqueness
- Inventory adjustment and low-stock monitoring
- Customer records
- Multi-item sales and invoice views
- Decimal-based discount and tax calculations
- Stock movement history and insufficient-stock validation

## Run locally

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
flask --app run.py create-admin
python run.py
```

Open `http://127.0.0.1:5000`. The database tables are created by the application factory. Create an administrator interactively; no default credentials are included.

## Validation status

The latest GitHub Actions run passed 6 tests under `tests/`, covering Decimal calculations, discount validation, stock reduction, insufficient-stock rejection, and authenticated route/template rendering. Full browser validation and production-database concurrency testing remain outstanding.

## Scope and provenance

This is a new portfolio implementation, not a verified copy of the original academic submission. The features above refer to the reconstruction only.

## Known limitations

- SQLite's row-locking behaviour differs from production database engines; concurrent sales require stronger transaction and inventory controls before production use.
- No payment gateway or accounting integration is included.
- Authentication, rate limiting, audit trails, migrations, and deployment hardening need further review.

## Original academic project: source and attribution

Original group codebase: PHP / MySQL, including database/book_shop_db.sql and administrative ordering/inventory modules. The original README contains example login credentials; these must not be reused as production secrets.

Original group materials: https://github.com/Khandaker-Atik/Book_shop_management

This was collaborative academic work. Specific individual implementation responsibilities are pending confirmation. The implementation and tests documented in this directory describe a later independently reconstructed reference build, not a copy of the historical submission. No original group files have been imported into this repository.
