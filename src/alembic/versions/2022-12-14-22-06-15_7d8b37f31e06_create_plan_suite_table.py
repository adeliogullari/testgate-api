"""create team project bbbbaarrraaaaa

Revision ID: 7d8b37f31e06
Revises: bcdc0a529ead
Create Date: 2022-12-14 22:06:15.294789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d8b37f31e06'
down_revision = 'bcdc0a529ead'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'plan_suite',
        sa.Column('plan_id', sa.Integer, sa.ForeignKey('plan.id')),
        sa.Column('suite_id', sa.Integer, sa.ForeignKey('suite.id')),
    )


def downgrade():
    op.drop_table('plan_suite')
