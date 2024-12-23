"""Product module."""
from flask import request

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


def create_dinamic_filters(request_data, object):
    """Create search filter dynamically."""
    filters = []
    for search in request_data.search:
        if search.type == "int":
            filters.append(object.unit_price > search.value)
        if search.type == "text":
            filters.append(object.product_name.like(search.value + "%"))
    return filters


@api.route("/productdetails", methods=("POST",))
def product_details():
    """Product Details API."""
    print("===> Inside customer details....")

    request_data = build_request(body=request.form["request"])
    filters = create_dinamic_filters(request_data=request_data, object=Product)

    value = Product.query.count()
    print(f"=============> Count of records: {value}")

    # search_data1 = f"{request_data.search[1].value}%"
    # print("=============> " + search_data1)
    # search_data2 = Product.unit_price > request_data.search[0].value

    query = Product.query
    # query = query.filter(Product.product_name.like(search_data1)
    #                      ).filter(search_data2)

    for filter in filters:
        query = query.filter(filter)

    query = query.limit(request_data.limit)
    query = query.offset(request_data.offset)
    products = query.all()
    # print(len(products))

    for product in products:
        print(f"{product}")

    return {"status": request_data}
