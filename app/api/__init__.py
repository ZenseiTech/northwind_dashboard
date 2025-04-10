"""Setup the API Blueprint."""

from flask import Blueprint

from app.models import Permission

api = Blueprint("api", __name__)

from . import categories, customers, orders, products, suppliers


@api.app_context_processor
def inject_permissions():
    """Add permissions so can be used in templates."""
    return dict(Permission=Permission)
