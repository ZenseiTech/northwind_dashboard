"""General utils module."""
import re

IN_DATE_FORMAT = "%m/%d/%Y"
OUT_DATE_FORMAT = "%Y-%m-%d"

num_to_bool = {"1": True, "0": False}


def date_format(date_in, format):
    """Format the input date with passed format."""
    if date_in:
        return date_in.strftime(format)
    return ""


def camel_case_to_snake(key_value):
    """Change camelcase to snakecase."""
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", key_value).lower()
