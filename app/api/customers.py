"""Customer module."""
from flask import request
from sqlalchemy import or_

from app.api import response
from app.api.search_query import create_dinamic_filters, create_dinamic_sort
from app.api.search_request import build_request

from ..models import Customer
from . import api


@api.route(
    "/customers",
    methods=(
        "GET",
        "POST",
    ),
)
def customers():
    """Call API for customer."""
    print("===> Inside customer....")

    query = Customer.query

    request_data = build_request(body=request.values["request"])
    filters = create_dinamic_filters(request_data=request_data, object=Customer)

    if request_data.searchLogic == "OR":
        query = query.filter(or_(*filters))
    else:
        query = query.filter(*filters)

    count = query.count()
    print(f"---------------> Count is: {count}")

    sorting, asc = create_dinamic_sort(request_data=request_data, object=Customer)

    if sorting:
        if asc:
            query = query.order_by(sorting.asc())
        else:
            query = query.order_by(sorting.desc())

    query = query.limit(request_data.limit)
    query = query.offset(request_data.offset)

    # calling the query ...
    customers = query.all()

    return response.grid_response("Customer", customers, count)
