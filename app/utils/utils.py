"""General utils module."""
IN_DATE_FORMAT = "%m/%d/%Y"
OUT_DATE_FORMAT = "%Y-%m-%d"

num_to_bool = {"1": True, "0": False}


def date_format(date_in, format):
    """Format the input date with passed format."""
    if date_in:
        return date_in.strftime(format)
    return ""
