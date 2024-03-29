"""empty message

Revision ID: 1857d6e43f72
Revises: 7efbbbb842b4
Create Date: 2019-11-11 23:34:41.521329

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1857d6e43f72'
down_revision = '7efbbbb842b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lecture', sa.Column('date_held', sa.DateTime(), nullable=True))
    op.drop_column('lecture', 'date_to_happen')
    op.add_column('task', sa.Column('date_to', sa.DateTime(), nullable=True))
    op.drop_column('task', 'date_to_do')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('date_to_do', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('task', 'date_to')
    op.add_column('lecture', sa.Column('date_to_happen', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('lecture', 'date_held')
    # ### end Alembic commands ###
