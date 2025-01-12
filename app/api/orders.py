"""Order module."""
import json

from flask import request
from sqlalchemy import or_

from app.api import response
from app.api.query import create_dinamic_filters, create_dinamic_sort
from app.api.request import build_request

from ..models import OrderDetailsView, OrderView, ShipRegions
from . import api


@api.route("/shipregions", methods=("GET", "POST"))
def ship_regions():
    """Retreive regions from api."""
    data = ShipRegions.query.all()
    regions = []
    for d in data:
        regions.append(d.region_name)
    return regions


@api.route(
    "/orders",
    methods=(
        "GET",
        "POST",
    ),
)
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

        record["recid"] = d.id
        record["customerName"] = d.customer_name
        record["customerId"] = d.customer_id
        record["employeeName"] = d.employee_name
        record["freight"] = d.freight
        record["orderDate"] = d.order_date.strftime("%m/%d/%Y")
        record["requiredDate"] = d.required_date.strftime("%m/%d/%Y")
        record["shippedDate"] = d.shipped_date.strftime("%m/%d/%Y")
        record["shipAddress"] = d.ship_address
        record["shipCity"] = d.ship_city
        record["shipCountry"] = d.ship_country
        record["shipPostalCode"] = d.ship_postal_code
        record["shipRegion"] = d.ship_region
        record["shipperName"] = d.shipper_name

    elif request_data["action"] == "save":
        print("Saving to DB")
        record = {}
        record["success"] = True

    return json.dumps(record)
