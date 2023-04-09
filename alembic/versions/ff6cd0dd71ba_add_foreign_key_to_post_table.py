"""add foreign key to post table

Revision ID: ff6cd0dd71ba
Revises: 2e7cec074bcb
Create Date: 2023-04-09 19:02:05.124098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff6cd0dd71ba'
down_revision = 'a252a3a93eae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer, nullable=False)
    )
    op.create_foreign_key(
        "posts_users_fkey",
        source_table = "posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
        onupdate="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fkey", table_name="posts")
    op.drop_column("posts", "owner_id")