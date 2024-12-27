"""Grid response."""
import json

from .utils import IN_DATE_FORMAT, date_format

num_to_bool = {"1": True, "0": False}


def product_response(data, count):
    """Create the product response."""
    response = {}
    response["status"] = "success"
    response["total"] = count

    records = []

    for d in data:
        record = {}
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

        records.append(record)

    response["records"] = records

    return json.dumps(response)


def order_response(data, count):
    """Create the order response."""
    response = {}
    response["status"] = "success"
    response["total"] = count

    records = []

    for d in data:
        record = {}
        record["recid"] = d.id
        record["customerName"] = d.customer_name
        record["customerId"] = d.customer_id
        record["employeeName"] = d.employee_name
        record["freight"] = d.freight
        record["orderDate"] = date_format(d.order_date, IN_DATE_FORMAT)
        record["requiredDate"] = date_format(d.required_date, IN_DATE_FORMAT)
        record["shippedDate"] = date_format(d.shipped_date, IN_DATE_FORMAT)
        record["shippedAddress"] = d.ship_address
        record["shipCity"] = d.ship_city
        record["shipCountry"] = d.ship_country
        record["shipPostalCode"] = d.ship_postal_code
        record["shipRegion"] = d.ship_region
        record["shipperName"] = d.shipper_name

        records.append(record)

    response["records"] = records

    return json.dumps(response)


def order_details_response(data):
    """Create the order details response."""
    response = {}
    response["status"] = "success"
    response["total"] = len(data)

    records = []

    for d in data:
        record = {}
        record["recid"] = d.id
        record["productName"] = d.product_name
        record["unitPrice"] = d.unit_price
        record["quantity"] = d.quantity
        record["discount"] = d.discount

        records.append(record)

    response["records"] = records

    return json.dumps(response)


def grid_response(object_type, data, count):
    """Generate response depending on object_type."""
    if object_type == "Product":
        return product_response(data, count)
    elif object_type == "Order":
        return order_response(data, count)
    elif object_type == "OrderDetails":
        return order_details_response(data)
    else:
        response = {}
        response["status"] = "error"
        response["message"] = "Something went wrong. Check with your admin"
        return response
