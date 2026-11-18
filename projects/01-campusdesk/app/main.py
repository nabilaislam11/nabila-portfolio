from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Student, Teacher, SchoolClass, FeeInvoice, Attendance
from app import db
from sqlalchemy import func
from datetime import date

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def dashboard():
    totals = {"students": Student.query.count(), "teachers": Teacher.query.count(),
              "classes": SchoolClass.query.count(),
              "active": Student.query.filter_by(status="Active").count()}
    recent_students = Student.query.order_by(Student.id.desc()).limit(6).all()
    today_count = Attendance.query.filter_by(attendance_date=date.today()).count()
    outstanding = db.session.query(func.coalesce(func.sum(FeeInvoice.amount), 0)).filter(
        FeeInvoice.status != "Paid").scalar()
    return render_template("dashboard.html", totals=totals,
        recent_students=recent_students, today_count=today_count, outstanding=outstanding)
