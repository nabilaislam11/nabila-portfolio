from decimal import Decimal
import pytest
from app import create_app
from app.extensions import db
from app.models import Book, User
from app.services import calculate_totals, create_sale

@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret-key",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", "WTF_CSRF_ENABLED": False})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def seed(app, stock=5):
    with app.app_context():
        user = User(username="tester", role="admin")
        user.set_password("test-password-long")
        book = Book(isbn="9780000000001", title="Test Book", author="A. Writer",
            category="Fiction", unit_price=Decimal("12.50"), stock_quantity=stock)
        db.session.add_all([user, book])
        db.session.commit()
        return user.id, book.id

def test_calculate_totals_uses_decimal_and_discount_before_tax():
    result = calculate_totals([(2, "10.00"), (1, "5.00")], discount="2.00", tax_rate="0.10")
    assert result == {"subtotal": Decimal("25.00"), "discount": Decimal("2.00"),
        "tax": Decimal("2.30"), "total": Decimal("25.30")}

def test_discount_cannot_exceed_subtotal():
    with pytest.raises(ValueError):
        calculate_totals([(1, "10.00")], discount="11.00")

def test_sale_reduces_stock_and_records_line_item(app):
    user_id, book_id = seed(app)
    with app.app_context():
        sale = create_sale(user_id=user_id, customer_id=None, cart={book_id: 2})
        db.session.commit()
        assert sale.total == Decimal("25.00")
        assert db.session.get(Book, book_id).stock_quantity == 3
        assert len(sale.items) == 1

def test_sale_rejects_insufficient_stock_without_changing_stock(app):
    user_id, book_id = seed(app, stock=1)
    with app.app_context():
        with pytest.raises(ValueError, match="Insufficient stock"):
            create_sale(user_id=user_id, customer_id=None, cart={book_id: 2})
        db.session.rollback()
        assert db.session.get(Book, book_id).stock_quantity == 1

def test_sale_rejects_nonpositive_quantity(app):
    user_id, book_id = seed(app)
    with app.app_context():
        with pytest.raises(ValueError, match="positive integer"):
            create_sale(user_id=user_id, customer_id=None, cart={book_id: 0})


def test_authenticated_pages_render(app):
    user_id, book_id = seed(app)
    with app.app_context():
        sale = create_sale(user_id=user_id, customer_id=None, cart={book_id: 1})
        db.session.commit()
        sale_id = sale.id
    client = app.test_client()
    response = client.post("/login", data={"username": "tester", "password": "test-password-long"},
        follow_redirects=True)
    assert response.status_code == 200
    for path in ["/", "/books", "/books/new", f"/books/{book_id}/stock",
                 "/customers", "/customers/new", "/sales/new", "/sales",
                 f"/sales/{sale_id}"]:
        response = client.get(path)
        assert response.status_code == 200, (path, response.get_data(as_text=True))
