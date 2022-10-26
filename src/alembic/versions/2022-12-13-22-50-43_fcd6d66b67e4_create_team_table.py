"""

Create Team Table

Revision ID: fcd6d66b67e4
Revises: ca63e2d086b1
Create Date: 2022-12-13 22:50:43.692919

"""
from alembic import op
import sqlalchemy as sa


revision = 'fcd6d66b67e4'
down_revision = 'ca63e2d086b1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'team',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )


def downgrade():
    op.drop_table('team')
