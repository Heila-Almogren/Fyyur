"""empty message

Revision ID: 09f4dc2c16da
Revises: ecbc1de75ef9
Create Date: 2020-10-13 04:43:05.430537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09f4dc2c16da'
down_revision = 'ecbc1de75ef9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Area', sa.Column('state', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Area', 'state')
    # ### end Alembic commands ###
