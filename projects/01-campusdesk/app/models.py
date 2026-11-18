from datetime import date, datetime
from decimal import Decimal
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint, UniqueConstraint
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="teacher")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (CheckConstraint("role IN ('admin', 'teacher')", name="ck_user_role"),)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(30), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class SchoolClass(db.Model):
    __tablename__ = "school_classes"
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(40), nullable=False)
    section = db.Column(db.String(20), nullable=False)
    class_teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    class_teacher = db.relationship("Teacher")
    __table_args__ = (UniqueConstraint("class_name", "section", name="uq_class_section"),)
    @property
    def display_name(self):
        return f"{self.class_name} - {self.section}"

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(30), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("school_classes.id"), nullable=False)
    guardian_name = db.Column(db.String(120), nullable=False)
    guardian_phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120))
    admission_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False, default="Active")
    school_class = db.relationship("SchoolClass")
    attendance_records = db.relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    results = db.relationship("Result", back_populates="student", cascade="all, delete-orphan")
    invoices = db.relationship("FeeInvoice", back_populates="student", cascade="all, delete-orphan")
    __table_args__ = (CheckConstraint("status IN ('Active', 'Inactive')", name="ck_student_status"),)

class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(20), unique=True, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)

class ClassSubject(db.Model):
    __tablename__ = "class_subjects"
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("school_classes.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    school_class = db.relationship("SchoolClass")
    subject = db.relationship("Subject")
    teacher = db.relationship("Teacher")
    __table_args__ = (UniqueConstraint("class_id", "subject_id", name="uq_class_subject"),)

class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False)
    student = db.relationship("Student", back_populates="attendance_records")
    __table_args__ = (
        UniqueConstraint("student_id", "attendance_date", name="uq_student_attendance_day"),
        CheckConstraint("status IN ('Present', 'Absent', 'Late', 'Excused')", name="ck_attendance_status"),
    )

class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("school_classes.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    maximum_marks = db.Column(db.Numeric(7, 2), nullable=False)
    school_class = db.relationship("SchoolClass")
    subject = db.relationship("Subject")
    __table_args__ = (CheckConstraint("maximum_marks > 0", name="ck_exam_max_marks"),)

class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    marks_obtained = db.Column(db.Numeric(7, 2), nullable=False)
    grade = db.Column(db.String(5))
    exam = db.relationship("Exam")
    student = db.relationship("Student", back_populates="results")
    __table_args__ = (
        UniqueConstraint("exam_id", "student_id", name="uq_exam_student_result"),
        CheckConstraint("marks_obtained >= 0", name="ck_result_nonnegative"),
    )

class FeeInvoice(db.Model):
    __tablename__ = "fee_invoices"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Unpaid")
    student = db.relationship("Student", back_populates="invoices")
    payments = db.relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_invoice_positive"),
        CheckConstraint("status IN ('Unpaid', 'Partially Paid', 'Paid')", name="ck_invoice_status"),
    )
    @property
    def paid_total(self):
        return sum((p.amount_paid for p in self.payments), Decimal("0.00"))
    @property
    def balance(self):
        return self.amount - self.paid_total

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("fee_invoices.id"), nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=date.today)
    reference = db.Column(db.String(80), unique=True, nullable=False)
    invoice = db.relationship("FeeInvoice", back_populates="payments")
    __table_args__ = (CheckConstraint("amount_paid > 0", name="ck_payment_positive"),)
