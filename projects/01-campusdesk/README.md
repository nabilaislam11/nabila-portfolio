# CampusDesk — School Administration Application

A modular Python/Flask school administration application covering student records, teacher accounts, classes, subjects, attendance, examinations, results, and fee tracking.

## Implementation

- Python, Flask, Flask-SQLAlchemy, and SQLite
- Flask-Login role-aware access for administrator and teacher accounts
- Flask-WTF forms and CSRF handling
- Student, class, section, and subject management
- Attendance and examination records
- Fee invoices and payment records

**Related academic project:** [Advanced School Management System — original Laravel source](https://github.com/nabilaislam11/advanced-school-management-system). CampusDesk is a separate Flask implementation of the school administration domain.

## Run locally

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
flask --app run.py init-db
flask --app run.py create-admin
python run.py
```

Open `http://127.0.0.1:5000`.

## Automated tests

The GitHub Actions workflow runs Python compilation, selected form checks, and five automated tests covering login, administration pages, and grade calculations. See `tests/`.
