"""

Create Team Project Table

Revision ID: 117030c7abc9
Revises: 00fcd5a0b3b9
Create Date: 2022-12-14 20:41:17.164577

"""
from alembic import op
import sqlalchemy as sa


revision = '117030c7abc9'
down_revision = '00fcd5a0b3b9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "team_project",
        sa.Column('team_id', sa.Integer, sa.ForeignKey('team.id')),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id')),
    )


def downgrade():
    op.drop_table('team_project')
