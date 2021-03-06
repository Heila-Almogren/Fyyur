"""empty message

Revision ID: 99808a360144
Revises: 8daf2e981448
Create Date: 2020-10-14 22:44:52.850686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99808a360144'
down_revision = '8daf2e981448'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('city', sa.String(), nullable=True))
    op.add_column('Venue', sa.Column('state', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'state')
    op.drop_column('Venue', 'city')
    # ### end Alembic commands ###
