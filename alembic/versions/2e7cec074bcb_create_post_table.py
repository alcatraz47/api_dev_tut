"""create post table

Revision ID: 2e7cec074bcb
Revises: 
Create Date: 2023-04-09 18:31:40.082425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e7cec074bcb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, index=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("published", sa.Boolean, server_default="TRUE"),
        sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.sql.expression.text('now()'))
    )


def downgrade() -> None:
    op.drop_table("posts")
