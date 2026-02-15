"""Add contact fields to vendors table

Revision ID: 003
Revises: 002
Create Date: B2Bmarket vendor contact fields

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("vendors", sa.Column("first_name", sa.String(length=100), nullable=True))
    op.add_column("vendors", sa.Column("last_name", sa.String(length=100), nullable=True))
    op.add_column("vendors", sa.Column("email", sa.String(length=255), nullable=True))
    op.add_column("vendors", sa.Column("phone_number", sa.String(length=20), nullable=True))
    op.create_index(op.f("ix_vendors_email"), "vendors", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_vendors_email"), table_name="vendors")
    op.drop_column("vendors", "phone_number")
    op.drop_column("vendors", "email")
    op.drop_column("vendors", "last_name")
    op.drop_column("vendors", "first_name")
