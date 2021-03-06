"""empty message

Revision ID: 2ef48a9dca01
Revises: 927fca3076a9
Create Date: 2019-08-01 23:35:11.975437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ef48a9dca01'
down_revision = '927fca3076a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('contents', sa.String(length=144), nullable=True),
    sa.Column('date_published', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contents_contents'), 'contents', ['contents'], unique=True)
    op.create_index(op.f('ix_contents_user_id'), 'contents', ['user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_contents_user_id'), table_name='contents')
    op.drop_index(op.f('ix_contents_contents'), table_name='contents')
    op.drop_table('contents')
    # ### end Alembic commands ###
