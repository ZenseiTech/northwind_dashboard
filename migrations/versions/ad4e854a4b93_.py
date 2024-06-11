"""empty message.

Revision ID: ad4e854a4b93
Revises: b812a50211e1
Create Date: 2024-06-05 15:56:55.347273
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "ad4e854a4b93"
down_revision = "b812a50211e1"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("PRAGMA legacy_alter_table=ON")
    op.alter_column("products", "unit_price2", new_column_name="unit_price")

    # ### end Alembic commands ###


def downgrade():
    op.execute("PRAGMA legacy_alter_table=ON")
    op.alter_column("products", "unit_price", new_column_name="unit_price2")

    # ### end Alembic commands ###
