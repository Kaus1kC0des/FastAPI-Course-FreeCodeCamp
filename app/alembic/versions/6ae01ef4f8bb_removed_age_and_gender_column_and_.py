"""Removed age and gender column and renamed user_name column to username

Revision ID: 6ae01ef4f8bb
Revises: a819281e034c
Create Date: 2026-02-26 22:28:42.099104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6ae01ef4f8bb'
down_revision: Union[str, Sequence[str], None] = 'a819281e034c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'user_name', new_column_name='username')
    op.drop_column('users', 'birth_date')
    op.drop_column('users', 'gender')
    op.drop_column('users', 'age')


def downgrade() -> None:
    op.add_column('users', sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('gender', postgresql.ENUM('male', 'female', 'prefer_not_to_say', 'other', name='gender_enum'), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('birth_date', sa.DATE(), autoincrement=False, nullable=True))
    op.alter_column('users', 'username', new_column_name='user_name')
