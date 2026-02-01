"""baseline placeholder for production

Revision ID: a194a74ecf10
Revises: 
Create Date: 2026-02-01
"""

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401

revision = "a194a74ecf10"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # This is a placeholder revision to match the production DB state.
    pass


def downgrade():
    pass