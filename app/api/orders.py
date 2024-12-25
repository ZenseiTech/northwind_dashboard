"""Order module."""
from flask import request

from app.api import response
from app.api.query import create_dinamic_filters, create_dinamic_sort
from app.api.request import build_request

from ..models import OrderView
from . import api


@api.route("/orderdetails", methods=("POST",))
def order_details():
    """Order Details API."""
    print("===> Inside order details....")

    query = OrderView.query

    request_data = build_request(body=request.form["request"])
    filters = create_dinamic_filters(request_data=request_data, object=OrderView)

    for filter in filters:
        query = query.filter(filter)

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
