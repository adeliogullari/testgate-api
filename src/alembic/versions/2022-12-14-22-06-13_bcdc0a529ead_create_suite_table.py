"""create team project bbbbaarrraaa

Revision ID: bcdc0a529ead
Revises: a8e11e02bed7
Create Date: 2022-12-14 22:06:13.185841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcdc0a529ead'
down_revision = 'a8e11e02bed7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'suite',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )


def downgrade():
    op.drop_table('suite')
