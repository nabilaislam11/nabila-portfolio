from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .models import Book, Customer, Sale, StockMovement
from .services import adjust_stock, create_sale, money

shop_bp = Blueprint("shop", __name__)

def admin_required():
    if current_user.role != "admin":
        abort(403)

@shop_bp.get("/")
@login_required
def dashboard():
    today = datetime.now(timezone.utc).date()
    sales_today = Sale.query.filter(db.func.date(Sale.created_at) == today).all()
    return render_template("dashboard.html", book_count=Book.query.filter_by(active=True).count(),
        customer_count=Customer.query.count(), low_stock=Book.query.filter(
            Book.active.is_(True), Book.stock_quantity <= Book.low_stock_threshold
        ).order_by(Book.stock_quantity).limit(8).all(),
        sales_today=sum((s.total for s in sales_today), Decimal("0.00")),
        recent_sales=Sale.query.order_by(Sale.created_at.desc()).limit(8).all())

@shop_bp.get("/books")
@login_required
def books():
    term = request.args.get("q", "").strip()
    query = Book.query.filter_by(active=True)
    if term:
        pattern = f"%{term}%"
        query = query.filter(or_(Book.title.ilike(pattern), Book.author.ilike(pattern), Book.isbn.ilike(pattern)))
    return render_template("books.html", books=query.order_by(Book.title).all(), term=term)

@shop_bp.route("/books/new", methods=["GET", "POST"])
@login_required
def new_book():
    admin_required()
    if request.method == "POST":
        try:
            price = money(request.form.get("unit_price", "0"))
            stock = int(request.form.get("stock_quantity", "0"))
            threshold = int(request.form.get("low_stock_threshold", "5"))
            if price < 0 or stock < 0 or threshold < 0:
                raise ValueError("Price and stock values cannot be negative.")
            book = Book(isbn=request.form.get("isbn", "").strip(),
                title=request.form.get("title", "").strip(), author=request.form.get("author", "").strip(),
                category=request.form.get("category", "Uncategorised").strip(),
                publisher=request.form.get("publisher", "").strip() or None,
                unit_price=price, stock_quantity=stock, low_stock_threshold=threshold)
            if not all([book.isbn, book.title, book.author]):
                raise ValueError("ISBN, title and author are required.")
            db.session.add(book); db.session.flush()
            if stock:
                db.session.add(StockMovement(book_id=book.id, user_id=current_user.id,
                    movement_type="purchase", quantity_change=stock, note="Opening stock"))
            db.session.commit()
            flash("Book added.", "success")
            return redirect(url_for("shop.books"))
        except (ValueError, InvalidOperation) as exc:
            db.session.rollback(); flash(str(exc), "error")
        except IntegrityError:
            db.session.rollback(); flash("That ISBN already exists.", "error")
    return render_template("book_form.html")

@shop_bp.route("/books/<int:book_id>/stock", methods=["GET", "POST"])
@login_required
def stock_adjustment(book_id):
    admin_required(); book = db.get_or_404(Book, book_id)
    if request.method == "POST":
        try:
            adjust_stock(book=book, user_id=current_user.id,
                quantity_change=int(request.form.get("quantity_change", "0")),
                note=request.form.get("note", ""))
            db.session.commit(); flash("Stock updated.", "success")
            return redirect(url_for("shop.books"))
        except ValueError as exc:
            db.session.rollback(); flash(str(exc), "error")
    return render_template("stock_form.html", book=book)

@shop_bp.get("/customers")
@login_required
def customers():
    return render_template("customers.html", customers=Customer.query.order_by(Customer.name).all())

@shop_bp.route("/customers/new", methods=["GET", "POST"])
@login_required
def new_customer():
    if request.method == "POST":
        customer = Customer(name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip().lower() or None,
            phone=request.form.get("phone", "").strip() or None)
        if not customer.name:
            flash("Customer name is required.", "error")
        else:
            try:
                db.session.add(customer); db.session.commit()
                flash("Customer added.", "success"); return redirect(url_for("shop.customers"))
            except IntegrityError:
                db.session.rollback(); flash("That email address is already registered.", "error")
    return render_template("customer_form.html")

@shop_bp.route("/sales/new", methods=["GET", "POST"])
@login_required
def new_sale():
    if request.method == "POST":
        try:
            cart = {}
            for key, value in request.form.items():
                if key.startswith("qty_") and value.strip():
                    qty = int(value)
                    if qty: cart[int(key[4:])] = qty
            discount = money(request.form.get("discount", "0"))
            tax_rate = Decimal(request.form.get("tax_rate", "0")) / Decimal("100")
            sale = create_sale(user_id=current_user.id,
                customer_id=int(request.form.get("customer_id") or 0) or None,
                cart=cart, discount=discount, tax_rate=tax_rate)
            db.session.commit(); return redirect(url_for("shop.invoice", sale_id=sale.id))
        except (ValueError, InvalidOperation) as exc:
            db.session.rollback(); flash(str(exc), "error")
    return render_template("sale_form.html", books=Book.query.filter_by(active=True).order_by(Book.title).all(),
        customers=Customer.query.order_by(Customer.name).all())

@shop_bp.get("/sales")
@login_required
def sales():
    return render_template("sales.html", sales=Sale.query.order_by(Sale.created_at.desc()).limit(100).all())

@shop_bp.get("/sales/<int:sale_id>")
@login_required
def invoice(sale_id):
    sale = db.get_or_404(Sale, sale_id)
    return render_template("invoice.html", sale=sale)
