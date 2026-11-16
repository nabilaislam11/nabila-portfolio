from functools import wraps
from decimal import Decimal
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator

def calculate_grade(marks, maximum):
    if maximum <= 0:
        raise ValueError("Maximum marks must be positive.")
    percentage = (Decimal(marks) / Decimal(maximum)) * Decimal("100")
    # Illustrative thresholds; configure these for a real institution.
    if percentage >= 80: return "A+"
    if percentage >= 70: return "A"
    if percentage >= 60: return "A-"
    if percentage >= 50: return "B"
    if percentage >= 40: return "C"
    if percentage >= 33: return "D"
    return "F"
