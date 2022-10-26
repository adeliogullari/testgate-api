"""

Create Role Permission Table

Revision ID: ca63e2d086b1
Revises: dm63et6zl27b3
Create Date: 2022-12-13 22:50:40.342551

"""
from alembic import op
import sqlalchemy as sa


revision = 'ca63e2d086b1'
down_revision = 'dm63et6zl27b3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "role_permission",
        sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id')),
        sa.Column('permission_id', sa.Integer, sa.ForeignKey('permission.id')),
    )


def downgrade():
    op.drop_table('role_permission')
