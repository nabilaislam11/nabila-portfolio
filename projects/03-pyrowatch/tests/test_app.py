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


def test_other_users_cannot_view_records_or_media(tmp_path):
    app = make_app(tmp_path)
    with app.app_context():
        owner = User.query.filter_by(username="tester").first()
        other = User(username="other", role="operator")
        other.set_password("other-password-123")
        db.session.add(other)
        db.session.flush()
        record = DetectionRecord(
            original_filename="private.jpg", media_type="image",
            status="completed", created_by=owner.id,
            result_filename="private-result.jpg")
        db.session.add(record)
        db.session.commit()
        record_id = record.id
    upload = tmp_path / "uploads"
    upload.mkdir(exist_ok=True)
    (upload / "private-result.jpg").write_bytes(b"private-output")
    client = app.test_client()
    response = client.post("/login", data={"username": "other", "password": "other-password-123"})
    assert response.status_code == 302
    assert client.get(f"/records/{record_id}").status_code == 404
    assert client.get("/media/private-result.jpg").status_code == 404
    dashboard = client.get("/")
    assert dashboard.status_code == 200
    assert b"private.jpg" not in dashboard.data
    assert b"private-result.jpg" not in dashboard.data


def test_owner_can_access_own_output(tmp_path):
    app = make_app(tmp_path)
    with app.app_context():
        owner = User.query.filter_by(username="tester").first()
        record = DetectionRecord(
            original_filename="sample.jpg", media_type="image",
            status="completed", created_by=owner.id,
            result_filename="own-result.jpg")
        db.session.add(record)
        db.session.commit()
        record_id = record.id
    upload = tmp_path / "uploads"
    upload.mkdir(exist_ok=True)
    (upload / "own-result.jpg").write_bytes(b"owner-output")
    client = app.test_client()
    login(client)
    assert client.get(f"/records/{record_id}").status_code == 200
    response = client.get("/media/own-result.jpg")
    assert response.status_code == 200
    assert response.data == b"owner-output"
