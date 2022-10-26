"""

Create Suite Case Table

Revision ID: cee109a6c4ec
Revises: 767665cf7a3c
Create Date: 2022-12-14 22:06:20.042105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cee109a6c4ec'
down_revision = '767665cf7a3c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'suite_case',
        sa.Column('suite_id', sa.Integer, sa.ForeignKey('suite.id')),
        sa.Column('case_id', sa.Integer, sa.ForeignKey('case.id')),
    )


def downgrade():
    op.drop_table('suite_case')
