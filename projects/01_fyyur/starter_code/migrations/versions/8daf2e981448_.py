"""empty message

Revision ID: 8daf2e981448
Revises: 949edf926f7a
Create Date: 2020-10-14 22:41:56.827823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8daf2e981448'
down_revision = '949edf926f7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'num_upcoming_shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('num_upcoming_shows', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
