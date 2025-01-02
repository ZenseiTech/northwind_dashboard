"""Order module."""
from flask import request

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
