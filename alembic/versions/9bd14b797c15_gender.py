"""gender

Revision ID: 9bd14b797c15
Revises: a30cf7def646
Create Date: 2025-05-11 23:57:54.208068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9bd14b797c15'
down_revision: Union[str, None] = 'a30cf7def646'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'gender',
               existing_type=postgresql.ENUM('male', 'female', name='gender'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'gender',
               existing_type=postgresql.ENUM('male', 'female', name='gender'),
               nullable=False)
    # ### end Alembic commands ###
