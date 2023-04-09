"""add users unique email constraint

Revision ID: c87ec669602c
Revises: ff6cd0dd71ba
Create Date: 2023-04-09 19:35:56.711131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c87ec669602c'
down_revision = 'ff6cd0dd71ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "unique_email",
        "users",
        ["email"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "unique_email",
        table_name="users"
    )
