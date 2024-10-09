"""Add column in referrals 

Revision ID: c335c962486a
Revises: 72f8b3558c9a
Create Date: 2024-10-09 13:29:33.647278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c335c962486a'
down_revision: Union[str, None] = '72f8b3558c9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('referrals', 'telegram_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('referrals', 'telegram_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
