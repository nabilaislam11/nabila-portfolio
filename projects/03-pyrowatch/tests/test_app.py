import io
from app import create_app, db
from app.models import User, DetectionRecord

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


def test_analysis_and_record_pages_render(tmp_path):
    app = make_app(tmp_path)
    with app.app_context():
        user = User.query.filter_by(username="tester").first()
        record = DetectionRecord(original_filename="sample.jpg", media_type="image",
            status="model_unavailable", created_by=user.id,
            error_message="Model weights are not configured.")
        db.session.add(record)
        db.session.commit()
        record_id = record.id
    client = app.test_client()
    login(client)
    assert client.get("/analyze").status_code == 200
    response = client.get(f"/records/{record_id}")
    assert response.status_code == 200
    assert b"sample.jpg" in response.data
