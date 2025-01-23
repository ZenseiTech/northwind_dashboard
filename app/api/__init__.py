"""Setup the API Blueprint."""

from flask import Blueprint

api = Blueprint("api", __name__)

from . import categories, customers, orders, products, suppliers
