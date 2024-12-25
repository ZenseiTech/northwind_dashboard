"""Filter queries."""

import re

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

bool_map = {"N": 0, "Y": 1}


def camel_case_to_snake(key_value):
    """Change camelcase to snakecase."""
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", key_value).lower()


def create_dinamic_sort(request_data, object):
    """Create sort dinamically."""
    # print(dir(object))
    asc = True
    for sort in request_data.sort:
        print(f"---------> {sort}")
        attr = getattr(object, camel_case_to_snake(sort.field))
        if "desc" in sort.direction:
            asc = False
        return attr, asc

    return None, asc


def create_dinamic_filters(request_data, object):
    """Create search filter dynamically."""
    filters = []

    for search in request_data.search:
        attr = getattr(object, camel_case_to_snake(search.field))
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
