"""General utils module."""
IN_DATE_FORMAT = "%m/%d/%Y"


def date_format(date_in, format):
    """Format the input date with passed format."""
    if date_in:
        return date_in.strftime(format)
    return ""
