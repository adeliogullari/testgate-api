"""

Create Request Table

Revision ID: 7ff8ba550230
Revises: cee109a6c4ec
Create Date: 2022-12-14 22:06:23.474309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ff8ba550230'
down_revision = 'cee109a6c4ec'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'request',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('host', sa.String),
        sa.Column('port', sa.String),
        sa.Column('method', sa.String),
        sa.Column('body', sa.JSON),
    )


def downgrade():
    op.drop_table('request')
