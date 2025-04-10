"""Order module."""
import json

from flask import request
from flask_login import login_required
from sqlalchemy import or_

from app.api import response
from app.api.search_query import create_dinamic_filters, create_dinamic_sort
from app.api.search_request import build_request

from ..models import OrderDetailsView, OrderView, ShipCities, ShipCountries, ShipRegions
from . import api


@api.route("/shipregions", methods=("GET", "POST"))
@login_required
def ship_regions():
    """Retreive regions from api."""
    data = ShipRegions.query.all()
    regions = []
    for d in data:
        regions.append(d.region_name)
    return regions


@api.route("/shipcountries", methods=("GET", "POST"))
@login_required
def ship_countries():
    """Retreive countries from api."""
    data = ShipCountries.query.all()
    countries = []
    for d in data:
        countries.append(d.country_name)
    return countries


@api.route("/shipcities", methods=("GET", "POST"))
@login_required
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
        record["status"] = "success"
        record["message"] = "Form data saved successfully"

    return json.dumps(record)
