"""Load data from sql files."""
import logging as logger

from sqlalchemy import text

logger.basicConfig(
    format="%(levelname)s : Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s",
    level=logger.DEBUG,
)


def __load_data__(db, filename):
    with open(filename, "r") as f:
        insert_data_sql = f.read()

    if "categories" in insert_data_sql:
        # this is necessary to propery set image data ...
        logger.debug("===========> Adding categories images ...")
        insert_data_sql = (
            insert_data_sql.replace("0x", "x'")
            .replace("),", "'),")
            .replace(");", "');")
        )
    elif "employees" in insert_data_sql:
        logger.debug("===========> Adding employees images ...")

        insert_data_sql = insert_data_sql.replace("0x", "x'").replace("D900,", "D900',")

    with db.engine.begin() as conn:
        try:
            conn.execute(text(insert_data_sql))
            if "Orders" in insert_data_sql:
                conn.execute(text("ALTER TABLE orders add cust_id varchar"))
                conn.execute(text("UPDATE orders SET cust_id = customer_id"))
                conn.execute(
                    text(
                        """
                        UPDATE orders
                            SET customer_id = customers.id
                            FROM customers
                            WHERE cust_id = customers.customer_id
                        """
                    )
                )
                conn.execute(text("ALTER TABLE orders drop cust_id"))
        except Exception as e:
            logger.error(e)


def load(db, dropall=False):
    """Load datas."""
    if dropall:
        db.drop_all()
        db.create_all()
    __load_data__(db, "./db_backup/categories.sql")
    __load_data__(db, "./db_backup/products.sql")
    __load_data__(db, "./db_backup/suppliers.sql")
    __load_data__(db, "./db_backup/employees.sql")
    __load_data__(db, "./db_backup/customers.sql")
    __load_data__(db, "./db_backup/shippers.sql")
    __load_data__(db, "./db_backup/orders.sql")
    __load_data__(db, "./db_backup/order_details.sql")
