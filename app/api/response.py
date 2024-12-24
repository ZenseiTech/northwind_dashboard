"""Grid response."""
import json


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
        record["discontinued"] = d.discontinued
        record["categoryName"] = d.category.category_name
        record["supplierName"] = d.supplier.company_name
        record["supplierRegion"] = d.supplier.region

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
