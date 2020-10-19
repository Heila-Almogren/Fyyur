"""empty message

Revision ID: ff81e71455ea
Revises: d3461e6dc169
Create Date: 2020-10-13 06:55:13.271211

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ff81e71455ea'
down_revision = 'd3461e6dc169'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('past_shows', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Venue', 'Show', ['past_shows'], ['id'])
    op.create_foreign_key(None, 'Venue', 'Show', ['upcoming_shows'], ['id'])
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'upcoming_shows')
    op.drop_column('Venue', 'past_shows')
    # ### end Alembic commands ###
