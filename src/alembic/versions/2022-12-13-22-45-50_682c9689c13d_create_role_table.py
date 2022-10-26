"""

Create Role Table

Revision ID: 682c9689c13d
Revises: 4eaaf7f0365e
Create Date: 2022-12-13 22:45:50.479180

"""
from alembic import op
import sqlalchemy as sa


revision = '682c9689c13d'
down_revision = '4eaaf7f0365e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'role',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False)
    )


def downgrade():
    op.drop_table('role')
