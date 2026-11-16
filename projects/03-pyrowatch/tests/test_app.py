import io
from app import create_app, db
from app.models import User

def make_app(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "UPLOAD_FOLDER": str(tmp_path / "uploads"), "SECRET_KEY": "test-key"})
    with app.app_context():
        user = User(username="tester", role="admin")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    return app

def login(client):
    return client.post("/login", data={"username": "tester", "password": "password123"},
        follow_redirects=True)

def test_login_and_dashboard(tmp_path):
    app = make_app(tmp_path)
    response = login(app.test_client())
    assert response.status_code == 200
    assert b"Detection dashboard" in response.data

def test_unsupported_file_is_rejected(tmp_path):
    app = make_app(tmp_path)
    client = app.test_client()
    login(client)
    response = client.post("/analyze",
        data={"media": (io.BytesIO(b"x"), "payload.exe")},
        content_type="multipart/form-data", follow_redirects=True)
    assert b"Unsupported file type" in response.data
