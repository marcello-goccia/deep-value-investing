"""add time frame to the table prices

Revision ID: 81e20d095203
Revises: b091a9eb4eb8
Create Date: 2019-12-25 21:21:25.999612

"""
from alembic import op
import sqlalchemy as sa

from data_storing.assets.common import TimeFrame


# revision identifiers, used by Alembic.
revision = '81e20d095203'
down_revision = 'b091a9eb4eb8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'Prices',
        sa.Column('time_frame', sa.Enum(TimeFrame), nullable=True),
    )


def downgrade():
    op.drop_column('Prices', 'time_frame')
