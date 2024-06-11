"""empty message.

Revision ID: 56a3f2296499
Revises: c27a2e221a35
Create Date: 2024-06-06 11:14:00.468529
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "56a3f2296499"
down_revision = "c27a2e221a35"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("customers", schema=None) as batch_op:
        batch_op.alter_column(
            "address", existing_type=sa.VARCHAR(length=64), nullable=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("customers", schema=None) as batch_op:
        batch_op.alter_column(
            "address", existing_type=sa.VARCHAR(length=64), nullable=False
        )

    # ### end Alembic commands ###
