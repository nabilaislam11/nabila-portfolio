from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import or_
from app import db
from app.models import Student, SchoolClass, Teacher
from app.utils import roles_required

bp = Blueprint("students", __name__)

@bp.route("/")
@login_required
def list_students():
    q = request.args.get("q", "").strip()
    class_id = request.args.get("class_id", type=int)
    query = Student.query.join(SchoolClass)
    if q:
        query = query.filter(or_(Student.full_name.ilike(f"%{q}%"),
            Student.student_code.ilike(f"%{q}%"), Student.guardian_name.ilike(f"%{q}%")))
    if class_id:
        query = query.filter(Student.class_id == class_id)
    return render_template("students.html",
        students=query.order_by(Student.full_name).all(),
        classes=SchoolClass.query.order_by(SchoolClass.class_name).all(), q=q, class_id=class_id)

@bp.route("/new", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def create_student():
    classes = SchoolClass.query.order_by(SchoolClass.class_name).all()
    if request.method == "POST":
        data = {k: request.form.get(k, "").strip() for k in
            ["student_code", "full_name", "guardian_name", "guardian_phone", "email"]}
        class_id = request.form.get("class_id", type=int)
        if not all(data[k] for k in ["student_code", "full_name", "guardian_name", "guardian_phone"]) or not class_id:
            flash("Complete all required fields.", "error")
        elif not db.session.get(SchoolClass, class_id):
            flash("Select a valid class.", "error")
        elif Student.query.filter_by(student_code=data["student_code"]).first():
            flash("Student ID already exists.", "error")
        else:
            db.session.add(Student(student_code=data["student_code"], full_name=data["full_name"],
                class_id=class_id, guardian_name=data["guardian_name"],
                guardian_phone=data["guardian_phone"], email=data["email"] or None))
            db.session.commit()
            flash("Student created.", "success")
            return redirect(url_for("students.list_students"))
    return render_template("student_form.html", student=None, classes=classes)

@bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def edit_student(student_id):
    student = db.get_or_404(Student, student_id)
    classes = SchoolClass.query.order_by(SchoolClass.class_name).all()
    if request.method == "POST":
        for field in ["full_name", "guardian_name", "guardian_phone", "email"]:
            setattr(student, field, request.form.get(field, "").strip() or None)
        student.class_id = request.form.get("class_id", type=int)
        student.status = request.form.get("status", "Active")
        if not student.full_name or not student.guardian_name or not student.guardian_phone or not db.session.get(SchoolClass, student.class_id):
            flash("Check the required fields and selected class.", "error")
        else:
            db.session.commit()
            flash("Student updated.", "success")
            return redirect(url_for("students.list_students"))
    return render_template("student_form.html", student=student, classes=classes)

@bp.post("/<int:student_id>/delete")
@login_required
@roles_required("admin")
def delete_student(student_id):
    student = db.get_or_404(Student, student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student and associated records deleted.", "success")
    return redirect(url_for("students.list_students"))

@bp.route("/teachers", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def teachers():
    if request.method == "POST":
        code = request.form.get("employee_code", "").strip()
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip() or None
        if not code or not name:
            flash("Employee code and name are required.", "error")
        elif Teacher.query.filter_by(employee_code=code).first():
            flash("Employee code already exists.", "error")
        else:
            db.session.add(Teacher(employee_code=code, full_name=name, email=email))
            db.session.commit()
            flash("Teacher added.", "success")
            return redirect(url_for("students.teachers"))
    return render_template("teachers.html", teachers=Teacher.query.order_by(Teacher.full_name).all())
