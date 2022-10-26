"""

Create Case Table

Revision ID: 767665cf7a3c
Revises: 7d8b37f31e06
Create Date: 2022-12-14 22:06:17.505611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '767665cf7a3c'
down_revision = '7d8b37f31e06'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'case',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('steps', sa.JSON)
    )


def downgrade():
    op.drop_table('case')
