"""Supplier module."""
from flask_login import login_required

from app.models import Supplier

from . import api


@api.route("/suppliers", methods=("GET", "POST"))
@login_required
def suppliers():
    """Retreive suppliers from api."""
    data = Supplier.query.all()
    suppliers = []
    for d in data:
        suppliers.append(d.company_name)
    return suppliers
