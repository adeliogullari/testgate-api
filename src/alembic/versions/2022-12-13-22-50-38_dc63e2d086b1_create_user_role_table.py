"""

Create User Role Table

Revision ID: dc63e2d086b1
Revises: 682c9689c13d
Create Date: 2022-12-13 22:50:38.456183

"""
from alembic import op
import sqlalchemy as sa


revision = 'dc63e2d086b1'
down_revision = '682c9689c13d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_role",
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id')),
    )


def downgrade():
    op.drop_table('user_role')
