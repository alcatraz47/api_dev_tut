"""create phone number column and change email type in users

Revision ID: a1d17cddf19f
Revises: 21e9ad9f4f82
Create Date: 2023-04-09 20:14:48.928038

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = 'a1d17cddf19f'
down_revision = '21e9ad9f4f82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sqlalchemy_utils.types.phone_number.PhoneNumberType(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
