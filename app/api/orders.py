"""Order module."""
import json

from flask import request
from flask_login import login_required
from sqlalchemy import or_

from app.api import response
from app.api.search_query import create_dinamic_filters, create_dinamic_sort
from app.api.search_request import build_request
from app.decorators import permission_required
from app.utils.utils import camel_case_to_snake

from ..models import (
    Customer,
    Employee,
    Order,
    OrderDetailsView,
    OrderView,
    Permission,
    ShipCities,
    ShipCountries,
    Shipper,
    ShipRegions,
    db,
)
from . import api


def __get_shipper(shipper_name):
    """Return the shipper."""
    query = Shipper.query
    query = query.filter(Shipper.company_name == shipper_name)
    return query.one()


def __get_employee(employee_name):
    """Return the employee."""
    query = Employee.query
    fname, lname = employee_name.split(" ")
    query = query.filter(
        Employee.first_name == fname.strip(), Employee.last_name == lname.strip()
    )
    return query.one()


def __get_customer(customer_name):
    """Return the customer."""
    query = Customer.query
    query = query.filter(Customer.company_name == customer_name)
    return query.one()


def __create_object(record):
    """From the record create the Order object."""
    new_record = {}

    for (key, value) in record.items():
        if key == "customerName":
            new_record["customer_id"] = __get_customer(record["customerName"]).id
        elif key == "employeeName":
            new_record["employee_id"] = __get_employee(record["employeeName"]).id
        elif key == "shipperName":
            new_record["ship_name"] = record["shipperName"]
        else:
            new_record[camel_case_to_snake(key)] = value

    if new_record["recid"]:
        new_record["id"] = new_record["recid"]

    del new_record["recid"]

    return new_record


def __save(request_data):
    in_record = __create_object(request_data["record"])
    order = Order(**in_record)
    db.session.add(order)
    db.session.commit()


def __update(request_data):
    in_record = __create_object(request_data["record"])
    order = Order(**in_record)
    order_update = Order.query.get(order.id)

    # TODO Set the values ....
    order_update.freight = order.freight
    # order_update.quantity_per_unit = order.quantity_per_unit
    # order_update.unit_price = order.unit_price
    db.session.commit()


@api.route("/shipregions", methods=("GET", "POST"))
@login_required
@permission_required(Permission.VIEW)
def ship_regions():
    """Retreive regions from api."""
    data = ShipRegions.query.all()
    regions = []
    for d in data:
        regions.append(d.region_name)
    return regions


@api.route("/shipcountries", methods=("GET", "POST"))
@login_required
@permission_required(Permission.VIEW)
def ship_countries():
    """Retreive countries from api."""
    data = ShipCountries.query.all()
    countries = []
    for d in data:
        countries.append(d.country_name)
    return countries


@api.route("/shipcities", methods=("GET", "POST"))
@login_required
@permission_required(Permission.VIEW)
def ship_cities():
    """Retreive cities from api."""
    data = ShipCities.query.all()
    cities = []
    for d in data:
        cities.append(d.city_name)
    return cities


@api.route(
    "/orders",
    methods=(
        "GET",
        "POST",
    ),
)
@login_required
@permission_required(Permission.VIEW)
def orders():
    """Order API."""
    print("===> Inside orders ...")

    query = OrderView.query

    request_data = build_request(body=request.values["request"])
    filters = create_dinamic_filters(request_data=request_data, object=OrderView)

    if request_data.searchLogic == "OR":
        query = query.filter(or_(*filters))
    else:
        query = query.filter(*filters)

    count = query.count()
    print(f"---------------> Count is: {count}")

    sorting, asc = create_dinamic_sort(request_data=request_data, object=OrderView)

    if sorting:
        if asc:
            query = query.order_by(sorting.asc())
        else:
            query = query.order_by(sorting.desc())

    query = query.limit(request_data.limit)
    query = query.offset(request_data.offset)

    # calling the query ...
    orders = query.all()

    return response.grid_response("Order", orders, count)


@api.route(
    "/orderdetails/<int:order_id>",
    methods=(
        "GET",
        "POST",
    ),
)
@login_required
@permission_required(Permission.VIEW)
def order_details(order_id):
    """Order Details API."""
    print("===> Inside order details....")

    query = OrderDetailsView.query
    query = query.filter(OrderDetailsView.order_id == order_id)

    # calling the query ...
    order_details = query.all()

    return response.grid_response("OrderDetails", order_details, 500)


@api.route(
    "/order",
    methods=(
        "GET",
        "POST",
    ),
)
@login_required
@permission_required(Permission.EDIT)
def order():
    """Order API."""
    print("===> Inside order....")

    request_data = json.loads(request.values["request"])

    record = {}

    if request_data["action"] == "get":
        query = OrderView.query
        query = query.filter(OrderView.id == request_data["recid"])

        # calling the query ...
        d = query.one()
        record = OrderView.order_record(d)

    elif request_data["action"] == "save":
        print("Saving to DB")
        __update(request_data)
        # record["status"] = "success"
        # record["message"] = "Form data saved successfully"

        record["success"] = True

    return json.dumps(record)
