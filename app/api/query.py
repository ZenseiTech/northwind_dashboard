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


def create_dinamic_filters(request_data, object):
    """Create search filter dynamically."""
    filters = []

    for search in request_data.search:
        type = operators_map[search.type]
        if type == "number":
            if search.operator == "more":
                filters.append(object.unit_price > search.value)
            elif search.operator == "more than":
                filters.append(object.unit_price >= search.value)
            elif search.operator == "less":
                filters.append(object.unit_price < search.value)
            elif search.operator == "less than":
                filters.append(object.unit_price <= search.value)
            elif search.operator == "between":
                filters.append(
                    object.unit_price.between(search.value[0], search.value[1])
                )
            else:
                filters.append(object.unit_price == search.value)
        if type == "text":
            if search.operator == "begins":
                filters.append(object.product_name.like(search.value + "%"))
            elif search.operator == "ends":
                filters.append("%" + object.product_name.like(search.value))
            elif search.operator == "contains":
                filters.append("%" + object.product_name.like(search.value) + "%")
            else:
                filters.append(object.product_name == search.value)
        # if type == "date":

    return filters
