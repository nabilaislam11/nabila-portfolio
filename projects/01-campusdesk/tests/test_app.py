import unittest
from app import create_app, db
from app.models import User, SchoolClass, Student, Subject, Exam
from datetime import date
from decimal import Decimal
from app.utils import calculate_grade

class CampusDeskTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-secret", "WTF_CSRF_ENABLED": False})
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            admin = User(username="admin", email="admin@example.test", role="admin")
            admin.set_password("test-password-123")
            db.session.add(admin)
            db.session.add(SchoolClass(class_name="Grade 8", section="A"))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page(self):
        self.assertEqual(self.client.get("/login").status_code, 200)

    def test_dashboard_requires_login(self):
        self.assertEqual(self.client.get("/").status_code, 302)

    def test_admin_login_and_dashboard(self):
        response = self.client.post("/login", data={
            "username": "admin", "password": "test-password-123"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

    def test_admin_pages_render(self):
        self.client.post("/login", data={"username": "admin", "password": "test-password-123"})
        with self.app.app_context():
            school_class = SchoolClass.query.first()
            subject = Subject(subject_code="ENG", subject_name="English")
            db.session.add(subject)
            db.session.flush()
            exam = Exam(exam_name="Term Test", class_id=school_class.id,
                subject_id=subject.id, exam_date=date.today(), maximum_marks=Decimal("100"))
            student = Student(student_code="ST-001", full_name="Sample Student",
                class_id=school_class.id, guardian_name="Sample Guardian", guardian_phone="0000000000")
            db.session.add_all([exam, student])
            db.session.commit()
            exam_id = exam.id
        paths = ["/", "/students/", "/students/new", "/students/teachers",
            "/academics/classes", "/academics/subjects", "/academics/attendance",
            "/academics/exams", "/academics/exams/" + str(exam_id) + "/results",
            "/finance/invoices"]
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200, response.get_data(as_text=True))

    def test_grade_calculation(self):
        self.assertEqual(calculate_grade(85, 100), "A+")
        self.assertEqual(calculate_grade(35, 100), "D")
        self.assertEqual(calculate_grade(20, 100), "F")

if __name__ == "__main__":
    unittest.main()
