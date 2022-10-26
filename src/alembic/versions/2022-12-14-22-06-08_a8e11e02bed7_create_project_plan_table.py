"""create team project bbbbaarrr

Revision ID: a8e11e02bed7
Revises: 031edeee3023
Create Date: 2022-12-14 22:06:08.264515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8e11e02bed7'
down_revision = '031edeee3023'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'project_plan',
        sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id')),
        sa.Column('plan_id', sa.Integer, sa.ForeignKey('plan.id')),
    )


def downgrade():
    op.drop_table('project_plan')
