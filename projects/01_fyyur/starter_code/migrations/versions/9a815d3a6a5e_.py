"""empty message

Revision ID: 9a815d3a6a5e
Revises: 4351b0f1b03a
Create Date: 2020-10-13 12:10:24.607509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a815d3a6a5e'
down_revision = '4351b0f1b03a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('venues_1', sa.Integer(), nullable=True))
    op.add_column('Show', sa.Column('venues_2', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Show', 'Venue', ['venues_1'], ['id'])
    op.create_foreign_key(None, 'Show', 'Venue', ['venues_2'], ['id'])
    op.drop_constraint('Venue_past_shows_fkey', 'Venue', type_='foreignkey')
    op.drop_constraint('Venue_upcoming_shows_fkey', 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'upcoming_shows')
    op.drop_column('Venue', 'past_shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('past_shows', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Venue_upcoming_shows_fkey', 'Venue', 'Show', ['upcoming_shows'], ['id'])
    op.create_foreign_key('Venue_past_shows_fkey', 'Venue', 'Show', ['past_shows'], ['id'])
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_column('Show', 'venues_2')
    op.drop_column('Show', 'venues_1')
    # ### end Alembic commands ###
