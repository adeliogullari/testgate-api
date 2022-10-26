"""

Create Parameter Table

Revision ID: afa0363e2741
Revises: 7ff8ba550230
Create Date: 2022-12-14 22:06:27.762261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afa0363e2741'
down_revision = '7ff8ba550230'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'parameter',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('type', sa.String),
        sa.Column('key', sa.String),
        sa.Column('value', sa.String),
        sa.Column('description', sa.String),
    )


def downgrade():
    op.drop_table('parameter')
