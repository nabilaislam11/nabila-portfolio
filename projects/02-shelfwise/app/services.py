from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4
from sqlalchemy import select
from .extensions import db
from .models import Book, Sale, SaleItem, StockMovement

CENT = Decimal("0.01")

def money(value):
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)

def calculate_totals(lines, discount=Decimal("0.00"), tax_rate=Decimal("0.00")):
    subtotal = money(sum((Decimal(int(q)) * money(price) for q, price in lines), Decimal("0.00")))
    discount = money(discount)
    tax_rate = Decimal(str(tax_rate))
    if discount < 0 or discount > subtotal:
        raise ValueError("Discount must be between zero and the subtotal.")
    if tax_rate < 0 or tax_rate > Decimal("1"):
        raise ValueError("Tax rate must be between 0 and 1.")
    taxable = subtotal - discount
    tax = money(taxable * tax_rate)
    return {"subtotal": subtotal, "discount": discount, "tax": tax, "total": money(taxable + tax)}

def create_sale(*, user_id, customer_id, cart, discount=Decimal("0.00"), tax_rate=Decimal("0.00")):
    if not cart:
        raise ValueError("Add at least one book to the sale.")
    normalised = {}
    for book_id, quantity in cart.items():
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Every sale quantity must be a positive integer.")
        normalised[int(book_id)] = normalised.get(int(book_id), 0) + quantity
    books = {}
    for book_id, quantity in normalised.items():
        book = db.session.execute(select(Book).where(Book.id == book_id).with_for_update()).scalar_one_or_none()
        if book is None or not book.active:
            raise ValueError(f"Book {book_id} is unavailable.")
        if book.stock_quantity < quantity:
            raise ValueError(f"Insufficient stock for '{book.title}'. Available: {book.stock_quantity}.")
        books[book_id] = book
    lines = [(qty, books[book_id].unit_price) for book_id, qty in normalised.items()]
    totals = calculate_totals(lines, discount, tax_rate)
    sale = Sale(invoice_number=f"BS-{uuid4().hex[:10].upper()}",
                customer_id=customer_id or None, user_id=user_id, **totals)
    db.session.add(sale)
    db.session.flush()
    for book_id, quantity in normalised.items():
        book = books[book_id]
        book.stock_quantity -= quantity
        db.session.add(SaleItem(sale_id=sale.id, book_id=book.id, book_title=book.title,
            quantity=quantity, unit_price=money(book.unit_price),
            line_total=money(Decimal(quantity) * money(book.unit_price))))
        db.session.add(StockMovement(book_id=book.id, user_id=user_id,
            movement_type="sale", quantity_change=-quantity, note=f"Invoice {sale.invoice_number}"))
    return sale

def adjust_stock(*, book, user_id, quantity_change, note, movement_type="correction"):
    quantity_change = int(quantity_change)
    if quantity_change == 0:
        raise ValueError("Stock adjustment cannot be zero.")
    if book.stock_quantity + quantity_change < 0:
        raise ValueError("Stock cannot become negative.")
    book.stock_quantity += quantity_change
    db.session.add(StockMovement(book_id=book.id, user_id=user_id,
        movement_type=movement_type, quantity_change=quantity_change, note=(note or "")[:250]))
