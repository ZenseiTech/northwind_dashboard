"""empty message.

Revision ID: 0dbc11606671
Revises:
Create Date: 2024-06-05 15:20:25.193224
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0dbc11606671"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("category_name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("picture", sa.LargeBinary(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("categories", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_categories_category_name"), ["category_name"], unique=True
        )

    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_name", sa.String(length=64), nullable=False),
        sa.Column("contact_name", sa.String(length=64), nullable=True),
        sa.Column("contact_title", sa.String(length=64), nullable=True),
        sa.Column("address", sa.String(length=64), nullable=True),
        sa.Column("city", sa.String(length=64), nullable=True),
        sa.Column("region", sa.String(length=64), nullable=True),
        sa.Column("postal_code", sa.String(length=64), nullable=True),
        sa.Column("country", sa.String(length=64), nullable=True),
        sa.Column("phone", sa.String(length=64), nullable=True),
        sa.Column("fax", sa.String(length=64), nullable=True),
        sa.Column("home_page", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("suppliers", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_suppliers_company_name"), ["company_name"], unique=True
        )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_name", sa.String(length=64), nullable=False),
        sa.Column("quantity_per_unit", sa.Integer(), nullable=True),
        sa.Column("unit_price", sa.Float(), nullable=True),
        sa.Column("units_in_stock", sa.Integer(), nullable=True),
        sa.Column("units_on_order", sa.Integer(), nullable=True),
        sa.Column("reorder_level", sa.Integer(), nullable=True),
        sa.Column("discontinued", sa.String(length=64), nullable=True),
        sa.Column("supplier_id", sa.Integer(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["supplier_id"],
            ["suppliers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_products_product_name"), ["product_name"], unique=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_products_product_name"))

    op.drop_table("products")
    with op.batch_alter_table("suppliers", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_suppliers_company_name"))

    op.drop_table("suppliers")
    with op.batch_alter_table("categories", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_categories_category_name"))

    op.drop_table("categories")
    # ### end Alembic commands ###
