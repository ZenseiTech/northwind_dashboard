import unittest

from flask import current_app
from sqlalchemy import select

from app import create_app, db
from app.models import Order, Product, order_details
from db_backup import load_data


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        load_data.load(db)

    def tearDown(self):
        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])

    def test_order(self):
        orders = Order.query.filter_by(customer_id="87").all()
        self.assertTrue(len(orders) == 5)

        query = select(Order, Product).join(Product.orders).filter_by(id=10248)
        results = db.session.execute(query).all()

        for order, product in results:
            print(f"---==> {order.id} {product.id}")

        print()
        query = (
            select(order_details, Product.product_name)
            .join(Product)
            .where(order_details.c.order_id == 10248)
        )
        print(query)
        print()
        values = db.session.execute(query)

        count = 0
        for value in values:
            print(value)
            count = count + 1
        # print(db.session.query(order_details).join(Order).join(Product).filter(order_details.c.order_id == 10248))
        # print(values)
        self.assertTrue(count == 3)
