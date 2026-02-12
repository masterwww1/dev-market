"""Create vendors table

Revision ID: 001
Revises:
Create Date: B2Bmarket step1

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "vendors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vendors_name"), "vendors", ["name"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_vendors_name"), table_name="vendors")
    op.drop_table("vendors")
