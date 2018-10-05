"""alter collections add farmer_no

Revision ID: 23e79d371587
Revises: dea951c3341d
Create Date: 2018-10-03 12:37:35.137990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23e79d371587'
down_revision = 'dea951c3341d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('collections_farmer_id_fkey', 'collections', type_='foreignkey')
    op.drop_column('collections', 'farmer_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collections', sa.Column('farmer_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('collections_farmer_id_fkey', 'collections', 'farmers', ['farmer_id'], ['id'])
    # ### end Alembic commands ###