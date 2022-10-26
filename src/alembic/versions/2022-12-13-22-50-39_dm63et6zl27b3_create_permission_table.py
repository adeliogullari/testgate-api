"""

Create Permission Table

Revision ID: dm63et6zl27b3
Revises: dc63e2d086b1
Create Date: 2022-12-13 22:50:39.459537

"""
from alembic import op
import sqlalchemy as sa


revision = 'dm63et6zl27b3'
down_revision = 'dc63e2d086b1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'permission',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False)
    )


def downgrade():
    op.drop_table('permission')
