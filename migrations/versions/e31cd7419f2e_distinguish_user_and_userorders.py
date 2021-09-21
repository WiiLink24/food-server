"""Distinguish User and UserOrders

Revision ID: e31cd7419f2e
Revises: b0abdec8d94c
Create Date: 2021-09-21 14:27:44.943459

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e31cd7419f2e"
down_revision = "b0abdec8d94c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(None, "menu_list", "shops", ["shop_code"], ["shop_code"])
    op.alter_column(
        "shops",
        "category_code",
        existing_type=postgresql.ENUM(
            "Pizza",
            "Bento_Box",
            "Sushi",
            "Fish",
            "Seafood",
            "Western",
            "Fast_Food",
            "Curry",
            "Party_Food",
            "Drinks",
            "Others",
            name="categorytypes",
        ),
        nullable=False,
    )
    op.alter_column("user_orders", "basket", existing_type=sa.TEXT(), nullable=False)


def downgrade():
    op.alter_column("user_orders", "basket", existing_type=sa.TEXT(), nullable=True)
    op.alter_column(
        "shops",
        "category_code",
        existing_type=postgresql.ENUM(
            "Pizza",
            "Bento_Box",
            "Sushi",
            "Fish",
            "Seafood",
            "Western",
            "Fast_Food",
            "Curry",
            "Party_Food",
            "Drinks",
            "Others",
            name="categorytypes",
        ),
        nullable=True,
    )
    op.drop_constraint(None, "menu_list", type_="foreignkey")
