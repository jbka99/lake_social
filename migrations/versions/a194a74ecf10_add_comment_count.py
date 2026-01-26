"""add comment_count

Revision ID: a194a74ecf10
Revises: 4ebaa2c5886e
Create Date: 2026-01-26 19:56:37.055329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a194a74ecf10'
down_revision = '4ebaa2c5886e'
branch_labels = None
depends_on = None


def upgrade():
    
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment_count', sa.Integer(), nullable=True))

def downgrade():

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('comment_count')

