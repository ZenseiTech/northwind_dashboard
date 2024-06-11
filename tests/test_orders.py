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
        self.app.logger.info("\n\n")

    def tearDown(self):
        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    # def test_app_exists(self):
    #     self.assertFalse(current_app is None)

    # def test_app_is_testing(self):
    #     self.assertTrue(current_app.config["TESTING"])

    def test_order(self):

        self.assertTrue(current_app.config["TESTING"])

        self.assertFalse(current_app is None)

        orders = Order.query.filter_by(customer_id="87").all()
        self.assertTrue(len(orders) == 5)

        query = select(Order, Product).join(Product.orders).filter_by(id=10248)
        results = db.session.execute(query).all()

        for order, product in results:
            self.app.logger.info(f"Result of query: {order.id} {product.id}")

        self.app.logger.info("\n")
        query = (
            select(order_details, Product.product_name)
            .join(Product)
            .where(order_details.c.order_id == 10248)
        )
        self.app.logger.info(f"Query: {query}")
        self.app.logger.info("\n")
        values = db.session.execute(query)

        count = 0
        for value in values:
            self.app.logger.info(value)
            count = count + 1
        # self.app.logger.info(db.session.query(order_details)
        # .join(Order).join(Product).filter(order_details.c.order_id == 10248))
        # self.app.logger.info(values)
        self.assertTrue(count == 3)
