"""added no financial data to the table financial

Revision ID: b091a9eb4eb8
Revises: edefd290936a
Create Date: 2019-10-02 17:07:27.152526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b091a9eb4eb8'
down_revision = 'edefd290936a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'Fundamentals',
        sa.Column('no_financial_available', sa.Boolean(), server_default='0', default=False),
    )

    # op.execute("""
    #     UPDATE Fundamentals
    #     SET no_financial_available = '0'
    # """)
    # op.alter_column('Fundamentals', 'no_financial_available', nullable=False)


def downgrade():
    pass
