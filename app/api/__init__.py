"""Setup the API Blueprint."""

from flask import Blueprint

from . import categories, orders, products

api = Blueprint("api", __name__)

categories.info()
orders.info()
products.info()
