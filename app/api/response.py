"""Grid response."""
from app.models import Customer, OrderDetailsView, OrderView, ProductView


def grid_response(object_type, data, count):
    """Generate response depending on object_type."""
    if object_type == "Product":
        return ProductView.product_response(data, count)
    elif object_type == "Order":
        return OrderView.order_response(data, count)
    elif object_type == "OrderDetails":
        return OrderDetailsView.order_details_response(data)
    elif object_type == "Customer":
        return Customer.response(data, count)
    else:
        response = {}
        response["status"] = "error"
        response["message"] = "Something went wrong. Check with your admin"
        return response
