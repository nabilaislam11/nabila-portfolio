from datetime import date
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Student, FeeInvoice, Payment
from app.utils import roles_required

bp = Blueprint("finance", __name__)

@bp.route("/invoices", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def invoices():
    students = Student.query.filter_by(status="Active").order_by(Student.full_name).all()
    if request.method == "POST":
        try:
            student_id = int(request.form.get("student_id", ""))
            amount = Decimal(request.form.get("amount", "0"))
            due_date = date.fromisoformat(request.form.get("due_date", ""))
            description = request.form.get("description", "").strip()
            if amount <= 0 or not description or not db.session.get(Student, student_id):
                raise ValueError
            db.session.add(FeeInvoice(student_id=student_id, amount=amount, due_date=due_date, description=description))
            db.session.commit()
            flash("Invoice created.", "success")
            return redirect(url_for("finance.invoices"))
        except (ValueError, InvalidOperation):
            flash("Enter valid invoice details.", "error")
    invoices = FeeInvoice.query.order_by(FeeInvoice.due_date.desc()).all()
    return render_template("invoices.html", students=students, invoices=invoices)

@bp.post("/invoices/<int:invoice_id>/payments")
@login_required
@roles_required("admin")
def add_payment(invoice_id):
    invoice = db.get_or_404(FeeInvoice, invoice_id)
    try:
        amount = Decimal(request.form.get("amount_paid", "0"))
        reference = request.form.get("reference", "").strip()
        if amount <= 0 or amount > invoice.balance or not reference:
            raise ValueError
        if Payment.query.filter_by(reference=reference).first():
            raise ValueError
        db.session.add(Payment(invoice_id=invoice.id, amount_paid=amount, reference=reference))
        db.session.flush()
        invoice.status = "Paid" if invoice.balance == 0 else "Partially Paid"
        db.session.commit()
        flash("Payment recorded.", "success")
    except (ValueError, InvalidOperation):
        db.session.rollback()
        flash("Invalid payment. Check the amount, balance, and unique reference.", "error")
    return redirect(url_for("finance.invoices"))
