"""Customer module."""
import json

from flask import abort, request
from flask_login import current_user, login_required
from sqlalchemy import or_

from app.api import response
from app.api.search_query import create_dinamic_filters, create_dinamic_sort
from app.api.search_request import build_request

from ..models import Customer, Permission
from . import api


@api.route(
    "/customers",
    methods=(
        "GET",
        "POST",
    ),
)
@login_required
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


@api.route(
    "/customer",
    methods=(
        "GET",
        "POST",
    ),
)
@login_required
# @permission_required(Permission.EDIT)
def customer():
    """Add or Edit Customer API."""
    print("===> Inside customer....")

    request_data = json.loads(request.values["request"])

    # checking permission for adding customer ...
    if (
        "isAdd" in request_data
        and request_data["isAdd"]
        and not current_user.can(Permission.ADD)
    ):
        abort(403)

    # checking permission for editing customer ...
    if (
        "isEdit" in request_data
        and request_data["isEdit"]
        and not current_user.can(Permission.EDIT)
    ):
        abort(403)

    record = {}

    if request_data["action"] == "get":
        query = Customer.query
        query = query.filter(Customer.id == request_data["recid"])
        d = query.one()
        record = Customer.customer_record(d)

    elif request_data["action"] == "save":
        isAdd = request_data["record"]["recid"] is None
        if isAdd:
            if current_user.can(Permission.ADD):
                print("Add...")
                # __save(request_data)
            else:
                abort(403)
        else:
            if current_user.can(Permission.EDIT):
                print("Customer update...")
                # __update(request_data)
            else:
                abort(403)

        record["success"] = True

    return json.dumps(record)
