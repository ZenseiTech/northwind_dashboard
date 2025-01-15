"""Product module."""
import json

from flask import request
from sqlalchemy import or_

from app.api import response
from app.api.search_query import create_dinamic_filters, create_dinamic_sort
from app.api.search_request import build_request

from ..models import Category, Product, ProductView, Supplier, db
from ..utils.utils import camel_case_to_snake
from . import api


def get_category(category_name):
    """Return the category."""
    query = Category.query
    query = query.filter(Category.category_name == category_name)
    return query.one()


def get_supplier(supplier_name):
    """Return the supplier."""
    query = Supplier.query
    query = query.filter(Supplier.company_name == supplier_name)
    return query.one()


def create_object(record):
    """From a dictionary create the Product object."""
    new_record = {}
    for (key, value) in record.items():
        if key == "supplierName":
            new_record["supplier_id"] = get_supplier(record["supplierName"]["id"]).id
        elif key == "categoryName":
            new_record["category_id"] = get_category(record["categoryName"]["id"]).id
        elif key == "supplierRegion":
            pass
        else:
            new_record[camel_case_to_snake(key)] = value

    if new_record["recid"]:
        new_record["id"] = new_record["recid"]
        del new_record["recid"]

    return new_record


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
        d = query.one()
        record = ProductView.product_record(d)

    elif request_data["action"] == "save":
        print("Saving to DB")
        in_record = {}
        if request_data["recid"]:
            in_record = create_object(request_data["record"])
            product = Product(**in_record)
            product_update = Product.query.get(product.id)
            product_update.units_on_order = product.units_on_order
            db.session.commit()
        else:
            print("Add...")

        record["success"] = True

    return json.dumps(record)
