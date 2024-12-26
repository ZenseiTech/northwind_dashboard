"""Category module."""
from ..models import Category
from . import api


@api.route("/categories", methods=("GET", "POST"))
def categories():
    """Retreive categories from api."""
    data = Category.query.all()
    categories = []
    for d in data:
        categories.append(d.category_name)
    return categories
