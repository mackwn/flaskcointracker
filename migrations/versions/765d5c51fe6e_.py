"""empty message

Revision ID: 765d5c51fe6e
Revises: 58a332d7dc81
Create Date: 2020-11-11 21:20:40.957332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '765d5c51fe6e'
down_revision = '58a332d7dc81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('exchange', sa.String(length=30), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('_password', sa.Binary(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coin', sa.String(length=30), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('initial_price', sa.Float(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('fulfilled_date', sa.DateTime(), nullable=True),
    sa.Column('fulfilled_price', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    op.drop_table('user')
    op.drop_table('coin')
    # ### end Alembic commands ###
