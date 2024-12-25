"""Category module."""
from ..models import Category
from . import api


@api.route("/categories", methods=("GET", "POST"))
def categories():
    """Categories API."""
    categories = Category.query.all()
    # categories = Category.query.filter_by(categoryName='Produce').all()
    # categories = Category.query.limit(2).all()
    # Category.query.limit
    for category in categories:
        print(f"Name: {category}")
    return {"status": "Ok"}
