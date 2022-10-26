"""

Create Project Table

Revision ID: 00fcd5a0b3b9
Revises: 740af2a2d7ef
Create Date: 2022-12-14 20:41:09.311569

"""
from alembic import op
import sqlalchemy as sa


revision = '00fcd5a0b3b9'
down_revision = '740af2a2d7ef'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'project',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('project')
