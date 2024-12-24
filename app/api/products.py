"""Product module."""
from flask import request

from app.api.query import create_dinamic_filters
from app.api.request import build_request

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


@api.route("/productdetails", methods=("POST",))
def product_details():
    """Product Details API."""
    print("===> Inside customer details....")

    request_data = build_request(body=request.form["request"])
    filters = create_dinamic_filters(request_data=request_data, object=Product)

    count = Product.query.count()
    print(f"=============> Count of records: {count}")

    query = Product.query

    for filter in filters:
        query = query.filter(filter)

    query = query.limit(request_data.limit)
    query = query.offset(request_data.offset)
    products = query.all()
    # print(len(products))

    for product in products:
        print(f"{product}")

    return {"status": request_data}
