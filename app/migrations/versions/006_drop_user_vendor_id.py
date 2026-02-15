"""Drop vendor_id from users - vendor is matched by email instead

Revision ID: 006
Revises: 005
Create Date: B2Bmarket vendor by email

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(op.f("ix_users_vendor_id"))
        batch_op.drop_constraint("fk_users_vendor_id_vendors", type_="foreignkey")
        batch_op.drop_column("vendor_id")


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("vendor_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_users_vendor_id_vendors",
            "vendors",
            ["vendor_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_index(op.f("ix_users_vendor_id"), ["vendor_id"], unique=False)
