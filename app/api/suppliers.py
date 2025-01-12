"""Supplier module."""
from app.models import Supplier

from . import api


@api.route("/suppliers", methods=("GET", "POST"))
def suppliers():
    """Retreive suppliers from api."""
    data = Supplier.query.all()
    suppliers = []
    for d in data:
        suppliers.append(d.company_name)
    return suppliers
