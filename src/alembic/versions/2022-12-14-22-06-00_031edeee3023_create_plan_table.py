"""

Create Plan Table

Revision ID: 031edeee3023
Revises: 117030c7abc9, 259be1d3cbb1
Create Date: 2022-12-14 22:06:00.388143

"""
from alembic import op
import sqlalchemy as sa


revision = '031edeee3023'
down_revision = '117030c7abc9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'plan',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )


def downgrade():
    op.drop_table('plan')
