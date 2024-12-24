"""Grid response."""
import json

num_to_bool = {"1": True, "0": False}


def product_response(data):
    """Create the product response."""
    response = {}
    response["status"] = "success"
    response["total"] = len(data)

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


def grid_response(object_type, data):
    """Generate response depending on object_type."""
    if object_type == "Product":
        return product_response(data)
    else:
        response = {}
        response["status"] = "error"
        response["message"] = "Something went wrong. Check with your admin"
        return response
