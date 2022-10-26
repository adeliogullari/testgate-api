"""

Create User Table

Revision ID: 4eaaf7f0365e
Revises:
Create Date: 2022-12-13 21:47:42.341474

"""
from alembic import op
import sqlalchemy as sa


revision = '4eaaf7f0365e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('firstname', sa.String(50), nullable=False),
        sa.Column('lastname', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('verified', sa.Boolean, default=False),
    )


def downgrade():
    op.drop_table('user')
