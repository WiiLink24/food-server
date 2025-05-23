"""Initial revision

Revision ID: b0abdec8d94c
Revises:
Create Date: 2021-09-13 10:25:19.079232

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b0abdec8d94c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "menu_list", ["menu_code"])
    op.create_unique_constraint(None, "shops", ["shop_code"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "shops", type_="unique")
    op.drop_constraint(None, "menu_list", type_="unique")
    # ### end Alembic commands ###
