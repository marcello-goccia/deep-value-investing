"""add columns for assets monitoring

Revision ID: 2cb3e075bb34
Revises: 
Create Date: 2019-07-18 18:13:49.586131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cb3e075bb34'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'Overview',
        sa.Column('valuable_company', sa.Boolean(), server_default='0', default=False),
    )

    # op.execute("""
    #     UPDATE Overview
    #     SET valuable_company = '0'
    # """)
    # op.alter_column('Overview', 'valuable_company', nullable=False)


    op.add_column(
        'Overview',
        sa.Column('intrinsic_value', sa.Float(), nullable=True),
    )


def downgrade():
    op.drop_column('Overview', 'valuable_company')
    op.drop_column('Overview', 'intrinsic_value')
