"""empty message.

Revision ID: b812a50211e1
Revises: 0dbc11606671
Create Date: 2024-06-05 15:26:54.040652
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "b812a50211e1"
down_revision = "0dbc11606671"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("products", "unit_price", new_column_name="unit_price2")

    # ### end Alembic commands ###


def downgrade():
    op.alter_column("products", "unit_price2", new_column_name="unit_price")

    # ### end Alembic commands ###
