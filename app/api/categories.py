"""Category module."""
from ..models import Category
from . import api


def info():
    """Print info."""
    print("Categories added to api blueprint")


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
