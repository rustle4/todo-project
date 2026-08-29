"""add priority tier to tasks

Revision ID: 6cff744d85f6
Revises: d8ca0eef1fd5
Create Date: 2026-08-29 15:17:47.123456
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

PRIORITY_ENUM_NAME = 'prioritytier'
PRIORITY_VALUES = ['S', 'A', 'B', 'C', 'D']

revision = '6cff744d85f6'
down_revision = 'd8ca0eef1fd5'
branch_labels = None
depends_on = None

def upgrade():
    priority_enum = ENUM(*PRIORITY_VALUES, name=PRIORITY_ENUM_NAME, create_type=True)
    priority_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('tasks', sa.Column('priority', priority_enum, nullable=True))

def downgrade():
    op.drop_column('tasks', 'priority')

    priority_enum = ENUM(*PRIORITY_VALUES, name=PRIORITY_ENUM_NAME, create_type=True)
    priority_enum.drop(op.get_bind(), checkfirst=True)
