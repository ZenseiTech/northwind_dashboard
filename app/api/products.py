"""Product module."""
from ..models import Product
from . import api


@api.route("/products", methods=("GET", "POST"))
def products():
    """Product API."""
    products = Product.query.all()
    # categories = Category.query.filter_by(categoryName='Produce').all()
    # categories = Category.query.limit(2).all()
    # Category.query.limit
    for product in products:
        print(f"Name: {product}")
    return {"status": "Ok"}
