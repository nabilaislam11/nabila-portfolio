# CampusDesk — School Management System

A reconstructed web application inspired by the academic project title **Advanced School Management System**.

## Reference implementation

- Python, Flask, Flask-SQLAlchemy and SQLite
- Flask-Login role-aware access (admin and teacher)
- Flask-WTF CSRF protection
- Student and teacher records
- Class, section and subject management
- Attendance, examination scheduling and results
- Fee invoices and payment records

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

Open `http://127.0.0.1:5000`. Use a unique administrator password. Do not deploy with the fallback development secret.

## Validation status

Python syntax compilation and static checks for CSRF-protected POST forms passed in the local reconstruction environment. Runtime, database integration, authorization-boundary, and browser tests have not yet been completed. The automated test suite is included under `tests/`.

## Scope and provenance

This is a newly written reference implementation, not a verified reproduction of the original university source code. The feature list describes this reconstructed application and should not be interpreted as a claim that every feature existed in the historical submission.

## Known limitations

- Teacher access is role-aware but not yet restricted to assigned classes or subjects.
- Grading thresholds are illustrative.
- Audit logging, database migrations, and production deployment hardening are not implemented.
- The dashboard's outstanding invoice figure is gross unpaid/partially paid invoice value and does not subtract partial payments.
- Review SQLite foreign-key enforcement and deletion behaviour before relying on it for real records.
