"""Grid response."""
import json

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


def date_format(date_in, format):
    """Format the input date with passed format."""
    if date_in:
        return date_in.strftime(format)
    return ""


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
        record["orderDate"] = date_format(d.order_date, "%Y-%m-%d")
        record["requiredDate"] = date_format(d.required_date, "%Y-%m-%d")
        record["shippedDate"] = date_format(d.shipped_date, "%Y-%m-%d")
        record["shippedAddress"] = d.ship_address
        record["shipCity"] = d.ship_city
        record["shipCountry"] = d.ship_country
        record["shipName"] = d.ship_name
        record["shipPostalCode"] = d.ship_postal_code
        record["shipRegion"] = d.ship_region
        record["shipperCompanyName"] = d.ship_name

        records.append(record)

    response["records"] = records

    return json.dumps(response)


def grid_response(object_type, data, count):
    """Generate response depending on object_type."""
    if object_type == "Product":
        return product_response(data, count)
    elif object_type == "Order":
        return order_response(data, count)
    else:
        response = {}
        response["status"] = "error"
        response["message"] = "Something went wrong. Check with your admin"
        return response
