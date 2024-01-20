"""Habits

Revision ID: 384f67f9ac4e
Revises: ecda84adec9c
Create Date: 2024-01-20 17:19:59.796732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '384f67f9ac4e'
down_revision = 'ecda84adec9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('habits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('broken', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('habits')
    # ### end Alembic commands ###
