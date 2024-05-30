"""init10

Revision ID: b98b40f56018
Revises: e3afc77ef559
Create Date: 2024-05-30 16:36:50.329685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b98b40f56018'
down_revision: Union[str, None] = 'e3afc77ef559'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('laboratory', sa.Column('url', sa.String(), nullable=True))
    op.drop_column('laboratory', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('laboratory', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('laboratory', 'url')
    # ### end Alembic commands ###