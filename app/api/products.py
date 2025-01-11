"""Product module."""
import json

from flask import request
from sqlalchemy import or_

from app.api import response
from app.api.query import create_dinamic_filters, create_dinamic_sort
from app.api.request import build_request

from ..models import ProductView
from ..utils.utils import num_to_bool
from . import api


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


@api.route(
    "/productdetails",
    methods=(
        "GET",
        "POST",
    ),
)
def product_details():
    """Product Details API."""
    print("===> Inside product details....")

    query = ProductView.query

    request_data = build_request(body=request.values["request"])
    filters = create_dinamic_filters(request_data=request_data, object=ProductView)

    if request_data.searchLogic == "OR":
        query = query.filter(or_(*filters))
    else:
        query = query.filter(*filters)

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


@api.route(
    "/product",
    methods=(
        "GET",
        "POST",
    ),
)
def product():
    """Product API."""
    print("===> Inside product....")

    request_data = json.loads(request.values["request"])

    record = {}

    if request_data["action"] == "get":
        query = ProductView.query
        query = query.filter(ProductView.id == request_data["recid"])

        # calling the query ...
        d = query.one()

        record["recid"] = d.id
        record["productName"] = d.product_name
        record["quantityPerUnit"] = d.quantity_per_unit
        record["unitPrice"] = d.unit_price
        record["unitsInStock"] = d.units_in_stock
        record["unitsOnOrder"] = d.units_on_order
        record["reorderLevel"] = d.reorder_level
        record["discontinued"] = num_to_bool[d.discontinued]
        record["categoryName"] = d.category_name
        record["supplierName"] = d.supplier_name
        record["supplierRegion"] = d.supplier_region

    elif request_data["action"] == "save":
        print("Saving to DB")
        record = {}
        record["success"] = True

    return json.dumps(record)
