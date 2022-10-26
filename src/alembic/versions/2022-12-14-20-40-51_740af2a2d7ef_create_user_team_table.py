"""

Create User Team Table

Revision ID: 740af2a2d7ef
Revises: fcd6d66b67e4
Create Date: 2022-12-14 20:40:51.220903

"""
from alembic import op
import sqlalchemy as sa


revision = '740af2a2d7ef'
down_revision = 'fcd6d66b67e4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_team",
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('team_id', sa.Integer, sa.ForeignKey('team.id')),
    )


def downgrade():
    op.drop_table('user_team')
