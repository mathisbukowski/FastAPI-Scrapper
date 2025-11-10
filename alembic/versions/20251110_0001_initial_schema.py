"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2025-11-10

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('username', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, index=True),
    )
    op.create_index('ix_items_user_id', 'items', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_items_user_id', table_name='items')
    op.drop_table('items')
    op.drop_table('users')
