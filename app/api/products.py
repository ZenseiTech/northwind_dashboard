"""Product module."""
from flask import request

from app.api import response
from app.api.query import create_dinamic_filters, create_dinamic_sort
from app.api.request import build_request

from ..models import ProductView
from . import api


def info():
    """Print info."""
    print("Products added to api blueprint")


@api.route("/products", methods=("GET", "POST"))
def products():
    """Product API."""
    products = ProductView.query.all()
    # categories = Category.query.filter_by(categoryName='Produce').all()
    # categories = Category.query.limit(2).all()
    # Category.query.limit
    for product in products:
        print(f"Name: {product}")
    return {"status": "Ok"}


@api.route("/productdetails", methods=("POST",))
def product_details():
    """Product Details API."""
    print("===> Inside product details....")

    query = ProductView.query

    request_data = build_request(body=request.form["request"])
    filters = create_dinamic_filters(request_data=request_data, object=ProductView)

    for filter in filters:
        query = query.filter(filter)

    count = query.count()
    print(f"---------------> Count is: {count}")

    sorting, asc = create_dinamic_sort(request_data=request_data, object=ProductView)

    if sorting:
        if asc:
            query = query.order_by(sorting.asc())
        else:
            query = query.order_by(sorting.desc())

    query = query.limit(request_data.limit)
    query = query.offset(request_data.offset)

    # calling the query ...
    products = query.all()

    return response.grid_response("Product", products, count)
