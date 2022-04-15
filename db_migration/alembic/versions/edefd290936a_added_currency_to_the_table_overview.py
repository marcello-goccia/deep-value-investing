"""added currency to the table overview

Revision ID: edefd290936a
Revises: 2cb3e075bb34
Create Date: 2019-08-07 21:19:50.811607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edefd290936a'
down_revision = '2cb3e075bb34'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'Overview',
        sa.Column('currency', sa.String(6), nullable=True)
    )


def downgrade():
    op.drop_column('Overview', 'currency')
