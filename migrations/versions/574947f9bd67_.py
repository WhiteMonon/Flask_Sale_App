"""empty message

Revision ID: 574947f9bd67
Revises: 6aafdce1689b
Create Date: 2024-09-02 05:55:12.086592

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '574947f9bd67'
down_revision = '6aafdce1689b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=mysql.VARCHAR(collation='utf8mb4_vietnamese_ci', length=20),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=mysql.VARCHAR(collation='utf8mb4_vietnamese_ci', length=20),
               nullable=True)

    # ### end Alembic commands ###
