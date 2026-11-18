from datetime import date
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Student, SchoolClass, Subject, Attendance, Exam, Result, Teacher
from app.utils import roles_required, calculate_grade

bp = Blueprint("academics", __name__)

@bp.route("/classes", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def classes():
    teachers = Teacher.query.order_by(Teacher.full_name).all()
    if request.method == "POST":
        name = request.form.get("class_name", "").strip()
        section = request.form.get("section", "").strip()
        teacher_id = request.form.get("class_teacher_id", type=int) or None
        if not name or not section:
            flash("Class name and section are required.", "error")
        elif SchoolClass.query.filter_by(class_name=name, section=section).first():
            flash("That class and section already exists.", "error")
        else:
            db.session.add(SchoolClass(class_name=name, section=section, class_teacher_id=teacher_id))
            db.session.commit()
            flash("Class created.", "success")
            return redirect(url_for("academics.classes"))
    return render_template("classes.html", classes=SchoolClass.query.order_by(SchoolClass.class_name).all(), teachers=teachers)

@bp.route("/subjects", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def subjects():
    if request.method == "POST":
        code = request.form.get("subject_code", "").strip()
        name = request.form.get("subject_name", "").strip()
        if not code or not name:
            flash("Subject code and name are required.", "error")
        elif Subject.query.filter_by(subject_code=code).first():
            flash("Subject code already exists.", "error")
        else:
            db.session.add(Subject(subject_code=code, subject_name=name))
            db.session.commit()
            flash("Subject added.", "success")
            return redirect(url_for("academics.subjects"))
    return render_template("subjects.html", subjects=Subject.query.order_by(Subject.subject_name).all())

@bp.route("/attendance", methods=["GET", "POST"])
@login_required
@roles_required("admin", "teacher")
def attendance():
    classes = SchoolClass.query.order_by(SchoolClass.class_name).all()
    selected_class = request.values.get("class_id", type=int)
    selected_date = request.values.get("attendance_date", date.today().isoformat())
    students = Student.query.filter_by(class_id=selected_class, status="Active").order_by(Student.full_name).all() if selected_class else []
    if request.method == "POST":
        for student in students:
            status = request.form.get(f"student_{student.id}")
            if status not in ("Present", "Absent", "Late", "Excused"):
                continue
            day = date.fromisoformat(selected_date)
            record = Attendance.query.filter_by(student_id=student.id, attendance_date=day).first()
            if record:
                record.status = status
            else:
                db.session.add(Attendance(student_id=student.id, attendance_date=day, status=status))
        db.session.commit()
        flash("Attendance saved.", "success")
        return redirect(url_for("academics.attendance", class_id=selected_class, attendance_date=selected_date))
    existing = {}
    if selected_class:
        rows = Attendance.query.join(Student).filter(Student.class_id == selected_class,
            Attendance.attendance_date == date.fromisoformat(selected_date)).all()
        existing = {r.student_id: r.status for r in rows}
    return render_template("attendance.html", classes=classes, students=students,
        selected_class=selected_class, selected_date=selected_date, existing=existing)

@bp.route("/exams", methods=["GET", "POST"])
@login_required
@roles_required("admin", "teacher")
def exams():
    classes = SchoolClass.query.order_by(SchoolClass.class_name).all()
    subjects = Subject.query.order_by(Subject.subject_name).all()
    if request.method == "POST":
        if current_user.role != "admin":
            abort(403)
        try:
            maximum = Decimal(request.form.get("maximum_marks", "0"))
            exam_date = date.fromisoformat(request.form.get("exam_date", ""))
            class_id = int(request.form.get("class_id", ""))
            subject_id = int(request.form.get("subject_id", ""))
            name = request.form.get("exam_name", "").strip()
            if maximum <= 0 or not name or not db.session.get(SchoolClass, class_id) or not db.session.get(Subject, subject_id):
                raise ValueError
            db.session.add(Exam(exam_name=name, class_id=class_id, subject_id=subject_id, exam_date=exam_date, maximum_marks=maximum))
            db.session.commit()
            flash("Exam created.", "success")
            return redirect(url_for("academics.exams"))
        except (ValueError, InvalidOperation):
            flash("Enter valid examination details.", "error")
    return render_template("exams.html", exams=Exam.query.order_by(Exam.exam_date.desc()).all(), classes=classes, subjects=subjects)

@bp.route("/exams/<int:exam_id>/results", methods=["GET", "POST"])
@login_required
@roles_required("admin", "teacher")
def results(exam_id):
    exam = db.get_or_404(Exam, exam_id)
    students = Student.query.filter_by(class_id=exam.class_id, status="Active").order_by(Student.full_name).all()
    existing = {r.student_id: r for r in Result.query.filter_by(exam_id=exam.id).all()}
    if request.method == "POST":
        try:
            for student in students:
                raw = request.form.get(f"marks_{student.id}", "").strip()
                if raw == "":
                    continue
                marks = Decimal(raw)
                if marks < 0 or marks > exam.maximum_marks:
                    raise ValueError("Marks must be within the exam maximum.")
                result = existing.get(student.id)
                grade = calculate_grade(marks, exam.maximum_marks)
                if result:
                    result.marks_obtained, result.grade = marks, grade
                else:
                    db.session.add(Result(exam_id=exam.id, student_id=student.id, marks_obtained=marks, grade=grade))
            db.session.commit()
            flash("Results saved.", "success")
            return redirect(url_for("academics.results", exam_id=exam.id))
        except (ValueError, InvalidOperation) as exc:
            db.session.rollback()
            flash(str(exc) or "Enter valid marks.", "error")
    return render_template("results.html", exam=exam, students=students, existing=existing)
