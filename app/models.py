"""Contains the model to the database."""
import hashlib
import traceback
from datetime import datetime, timedelta

import jwt
from flask import current_app, url_for
from flask_login import AnonymousUserMixin, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import logging as logger

from . import db


class Permission:
    """Contain the constant permissions."""

    VIEW = 1
    WRITE = 2
    ADMIN = 16


class Role(db.Model):
    """Role."""

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        """Initialize the class."""
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        """Insert initial roles."""
        roles = {
            "User": [Permission.WRITE],
            "Viewer": [Permission.VIEW, Permission.WRITE],
            "Administrator": [Permission.VIEW, Permission.WRITE, Permission.ADMIN],
        }
        default_role = "User"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = role.name == default_role
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        """Add permission the pass permission."""
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """Remove the pass permission."""
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        """Reset all the permissions."""
        self.permissions = 0

    def has_permission(self, perm):
        """Check the existance of the pass permission."""
        return self.permissions & perm == perm

    def __repr__(self):
        """Represent string of the class."""
        return "<Role %r>" % self.name


class User(UserMixin, db.Model):
    """User class."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        """Initialize the class."""
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["FLASKY_ADMIN"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @property
    def password(self):
        """Raise error when trying to read the password."""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Set the password."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify the pass password."""
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expiration, type="confirm"):
        """Generate a token, with the pass expiration."""
        reset_token = jwt.encode(
            {
                type: self.id,
                "exp": datetime.utcnow() + timedelta(seconds=expiration),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return reset_token

    def generate_confirmation_token(self, expiration=3600):
        """Generate a confirmation token with the pass expiration."""
        return self.generate_token(expiration)

    def generate_reset_token(self, expiration=3600):
        """Generate a reset token with the pass expiration."""
        return self.generate_token(expiration, type="reset")

    def confirm(self, token):
        """Confirm the pass token."""
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )
        except Exception:
            logger.error(traceback.format_exc())
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def reset_password(token, new_password):
        """Reset the password with the new pass password."""
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )
        except Exception:
            logger.error(traceback.format_exc())
            return False
        user = User.query.get(data.get("reset"))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate token for email change."""
        return jwt.encode(
            {
                "change_email": self.id,
                "new_email": new_email,
                "exp": datetime.utcnow() + timedelta(seconds=expiration),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    def change_email(self, token):
        """Change email checking the pass token."""
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )
        except Exception:
            logger.error(traceback.format_exc())
            return False
        if data.get("change_email") != self.id:
            return False
        new_email = data.get("new_email")
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        """Check if the user has permission."""
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        """Return whether a user is an administrator."""
        return self.can(Permission.ADMIN)

    def ping(self):
        """Update the user last activity time."""
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar_hash(self):
        """Return the hash of the user email."""
        return hashlib.md5(self.email.lower().encode("utf-8")).hexdigest()

    def gravatar(self, size=100, default="identicon", rating="g"):
        """Return the user avatar."""
        url = "https://secure.gravatar.com/avatar"
        hash = self.avatar_hash or self.gravatar_hash()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    def to_json(self):
        """Return the json representation of the user."""
        json_user = {
            "url": url_for("api.get_user", id=self.id),
            "username": self.username,
            "member_since": self.member_since,
            "last_seen": self.last_seen,
        }
        return json_user

    def generate_auth_token(self, expiration):
        """Generate auth token."""
        return self.generate_token(expiration)

    @staticmethod
    def verify_auth_token(token):
        """Verify auth token."""
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )
        except Exception:
            logger.error(traceback.format_exc())
            return None
        return User.query.get(data["id"])

    def __repr__(self):
        """Reprentation string of class."""
        return "<User %r>" % self.username


class AnonymousUser(AnonymousUserMixin):
    """Anonymous user."""

    def can(self, permissions):
        """Check if user has permissions."""
        return False

    def is_administrator(self):
        """Check if user is administrator."""
        return False


class Category(db.Model):
    """Category model."""

    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    description = db.Column(db.Text())
    picture = db.Column(db.LargeBinary)

    products = db.relationship("Product", backref="categories", lazy="dynamic")

    def __repr__(self):
        """Representation."""
        return "<Categories %r>" % self.category_name


class Supplier(db.Model):
    """Supplier model."""

    __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    contact_name = db.Column(db.String(64))
    contact_title = db.Column(db.String(64))
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    region = db.Column(db.String(64))
    postal_code = db.Column(db.String(64))
    country = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    fax = db.Column(db.String(64))
    home_page = db.Column(db.String(64))

    products = db.relationship("Product", backref="suppliers", lazy="dynamic")

    def __repr__(self):
        """Representation."""
        return "<Companies %r>" % self.company_name


class Product(db.Model):
    """Product model."""

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    quantity_per_unit = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    units_in_stock = db.Column(db.Integer)
    units_on_order = db.Column(db.Integer)
    reorder_level = db.Column(db.Integer)
    discontinued = db.Column(db.String(64))
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    orders = db.relationship(
        "Order", secondary="order_details", back_populates="products"
    )

    def __repr__(self):
        """Representation."""
        return "<Products %r>" % self.product_name


class Employee(db.Model):
    """Employee model."""

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    title_of_courtesy = db.Column(db.String(64))
    birthdate = db.Column(db.String(64), nullable=False)
    hire_date = db.Column(db.DateTime(), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    region = db.Column(db.String(64), nullable=False)
    postal_code = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    home_phone = db.Column(db.String(64), nullable=False)
    extension = db.Column(db.String(64))
    photo = db.Column(db.LargeBinary)
    notes = db.Column(db.String(64))
    reports_to = db.Column(db.Integer, db.ForeignKey("employees.id"))
    photo_path = db.Column(db.String(64))

    orders = db.relationship("Order", backref="employees", lazy="dynamic")

    def __repr__(self):
        """Representation."""
        return f"<Employees {self.first_name} {self.last_name}>"


class Customer(db.Model):
    """Customer model."""

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(64), nullable=False, unique=True, index=True)
    company_name = db.Column(db.String(64), nullable=False)
    contact_name = db.Column(db.String(64), nullable=False)
    contact_title = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    region = db.Column(db.String(64), nullable=True)
    postal_code = db.Column(db.String(64), nullable=True)
    country = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    fax = db.Column(db.String(64), nullable=True)
    orders = db.relationship("Order", backref="customers", lazy="dynamic")

    def __repr__(self):
        """Representation."""
        return f"<Customers {self.company_name} {self.customer_id}>"


class Shipper(db.Model):
    """Shipper model."""

    __tablename__ = "shippers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    orders = db.relationship("Order", backref="shippers", lazy="dynamic")

    def __repr__(self):
        """Representation."""
        return f"<Shippers {self.company_name} {self.phone}>"


class Order(db.Model):
    """Order model."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime(), nullable=False)
    required_date = db.Column(db.DateTime(), nullable=False)
    shipped_date = db.Column(db.DateTime(), nullable=True)
    freight = db.Column(db.Integer, default=0)
    ship_name = db.Column(db.String(64), nullable=False)
    ship_address = db.Column(db.String(64), nullable=False)
    ship_city = db.Column(db.String(64), nullable=False)
    ship_region = db.Column(db.String(64), nullable=False)
    ship_postal_code = db.Column(db.String(64), nullable=True)
    ship_country = db.Column(db.String(64), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    ship_via = db.Column(db.Integer, db.ForeignKey("shippers.id"))

    products = db.relationship(
        "Product", secondary="order_details", back_populates="orders"
    )

    def __repr__(self):
        """Representation."""
        return f"<Orders order.id = {self.id} customer_id: {self.customer_id}>"


order_details = db.Table(
    "order_details",
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id")),
    db.Column("unit_price", db.Float),
    db.Column("quantity", db.Integer),
    db.Column("discount", db.Float),
)
