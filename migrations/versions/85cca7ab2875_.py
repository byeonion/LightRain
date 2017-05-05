"""empty message

Revision ID: 85cca7ab2875
Revises: 
Create Date: 2017-05-03 22:57:35.808439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85cca7ab2875'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('listname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lists_listname'), 'lists', ['listname'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('author', sa.String(length=64), nullable=True),
    sa.Column('avatar_hash', sa.String(length=32), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('style', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['lists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_articles_author'), 'articles', ['author'], unique=False)
    op.create_index(op.f('ix_articles_email'), 'articles', ['email'], unique=False)
    op.create_index(op.f('ix_articles_timestamp'), 'articles', ['timestamp'], unique=False)
    op.create_index(op.f('ix_articles_title'), 'articles', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_articles_title'), table_name='articles')
    op.drop_index(op.f('ix_articles_timestamp'), table_name='articles')
    op.drop_index(op.f('ix_articles_email'), table_name='articles')
    op.drop_index(op.f('ix_articles_author'), table_name='articles')
    op.drop_table('articles')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_lists_listname'), table_name='lists')
    op.drop_table('lists')
    # ### end Alembic commands ###
