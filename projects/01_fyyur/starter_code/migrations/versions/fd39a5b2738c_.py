"""empty message

Revision ID: fd39a5b2738c
Revises: cb66e3edf7af
Create Date: 2020-10-19 03:30:32.986840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd39a5b2738c'
down_revision = 'cb66e3edf7af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Area')
    op.drop_constraint('Artist_area_fkey', 'Artist', type_='foreignkey')
    op.drop_column('Artist', 'area')
    op.drop_constraint('Venue_area_fkey', 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'area')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('area', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Venue_area_fkey', 'Venue', 'Area', ['area'], ['id'])
    op.add_column('Artist', sa.Column('area', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Artist_area_fkey', 'Artist', 'Area', ['area'], ['id'])
    op.create_table('Area',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Area_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Area_pkey')
    )
    # ### end Alembic commands ###