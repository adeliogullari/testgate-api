"""

Create Request Parameter Table

Revision ID: 4f0f6040d99b
Revises: afa0363e2741
Create Date: 2022-12-14 22:06:30.469889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f0f6040d99b'
down_revision = 'afa0363e2741'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "request_parameter",
        sa.Column('request_id', sa.Integer, sa.ForeignKey('request.id')),
        sa.Column('parameter_id', sa.Integer, sa.ForeignKey('parameter.id')),
    )


def downgrade():
    op.drop_table('request_parameter')

