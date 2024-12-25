"""Filter queries."""

operators_map = {
    "text": "text",
    "int": "number",
    "float": "number",
    "money": "number",
    "currency": "number",
    "percent": "number",
    "hex": "hex",
    "alphanumeric": "text",
    "color": "color",
    "date": "date",
    "time": "date",
    "datetime": "date",
    "list": "list",
    "combo": "text",
    "enum": "enum",
    "file": "enum",
    "select": "list",
    "radio": "list",
    "checkbox": "list",
    "toggle": "list",
}

field_map = {
    "unitPrice": "unit_price",
    "productName": "product_name",
    "quantityPerUnit": "quantity_per_unit",
    "unitPrice": "unit_price",
    "unitsInStock": "units_in_stock",
    "unitsOnOrder": "units_on_order",
    "reorderLevel": "reorder_level",
    "discontinued": "discontinued",
    "categoryName": "category_name",
    "supplierName": "supplier_name",
    "supplierRegion": "supplier_region",
    "shipCountry": "ship_country",
    "orderDate": "order_date",
}

bool_map = {"N": 0, "Y": 1}


def create_dinamic_sort(request_data, object):
    """Create sort dinamically."""
    # print(dir(object))
    asc = True
    for sort in request_data.sort:
        print(f"---------> {sort}")
        attr = getattr(object, field_map[sort.field])
        if "desc" in sort.direction:
            asc = False
        return attr, asc

    return None, asc


def create_dinamic_filters(request_data, object):
    """Create search filter dynamically."""
    filters = []

    for search in request_data.search:
        attr = getattr(object, field_map[search.field])
        type = operators_map[search.type]
        if type == "number":
            if search.operator == "more":
                filters.append(attr > search.value)
            elif search.operator == "more than":
                filters.append(attr >= search.value)
            elif search.operator == "less":
                filters.append(attr < search.value)
            elif search.operator == "less than":
                filters.append(attr <= search.value)
            elif search.operator == "between":
                filters.append(attr.between(search.value[0], search.value[1]))
            else:
                filters.append(attr == search.value)
        elif type == "list":
            if "Y" in search.value or "N" in search.value:
                filters.append(attr == bool_map[search.value])
            else:
                filters.append(attr == search.value)
        elif type == "date":
            if search.operator == "between":
                filters.append(attr.between(search.value[0], search.value[1]))
            else:
                filters.append(attr.between(search.value))
        elif type == "text":
            if search.operator == "begins":
                filters.append(attr.like(search.value + "%"))
            elif search.operator == "ends":
                filters.append("%" + attr.like(search.value))
            elif search.operator == "contains":
                filters.append("%" + attr.like(search.value) + "%")
            else:
                filters.append(attr == search.value)
        # if type == "date":

    return filters
