"""empty message

Revision ID: 5a1d301f9a07
Revises: 
Create Date: 2018-09-25 21:39:23.905227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a1d301f9a07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('productos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('productos')
    # ### end Alembic commands ###
