"""create users table

Revision ID: a252a3a93eae
Revises: ff6cd0dd71ba
Create Date: 2023-04-09 19:08:30.806131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a252a3a93eae'
down_revision = '2e7cec074bcb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
            index=True,
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.sql.expression.text('now()')
        ),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("users")
