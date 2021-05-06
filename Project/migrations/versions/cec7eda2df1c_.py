"""empty message

Revision ID: cec7eda2df1c
Revises: 
Create Date: 2021-05-06 13:39:55.718427

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geometry
import psycopg2

conn = psycopg2.connect("host=localhost dbname=bloodbank user=shri password=1234")
cur = conn.cursor()
cur.execute("CREATE EXTENSION postgis")
conn.commit()
cur.close()
conn.close()


# revision identifiers, used by Alembic.
revision = 'cec7eda2df1c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bloodbank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('address', sa.String(length=1000), nullable=False),
    sa.Column('contact_no', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('latitude', sa.Float(precision=20), nullable=False),
    sa.Column('longitude', sa.Float(precision=20), nullable=False),
    sa.Column('geom',Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact_no')
    )
    op.create_table('donor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('contact_no', sa.String(length=15), nullable=False),
    sa.Column('blood_group', sa.String(length=5), nullable=False),
    sa.Column('last_donation', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact_no'),
    sa.UniqueConstraint('email')
    )
    op.create_table('app_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('contact_no', sa.String(length=15), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('bloodbank_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bloodbank_id'], ['bloodbank.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact_no'),
    sa.UniqueConstraint('email')
    )
    op.create_table('bloodbank_stats',
    sa.Column('bloodbank_id', sa.Integer(), nullable=False),
    sa.Column('a_positive', sa.Integer(), nullable=False),
    sa.Column('a_negative', sa.Integer(), nullable=False),
    sa.Column('b_positive', sa.Integer(), nullable=False),
    sa.Column('b_negative', sa.Integer(), nullable=False),
    sa.Column('ab_positive', sa.Integer(), nullable=False),
    sa.Column('ab_negative', sa.Integer(), nullable=False),
    sa.Column('o_positive', sa.Integer(), nullable=False),
    sa.Column('o_negative', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bloodbank_id'], ['bloodbank.id'], ),
    sa.PrimaryKeyConstraint('bloodbank_id')
    )
    op.create_table('donation',
    sa.Column('donor_id', sa.Integer(), nullable=False),
    sa.Column('bloodbank_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('units', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bloodbank_id'], ['bloodbank.id'], ),
    sa.ForeignKeyConstraint(['donor_id'], ['donor.id'], ),
    sa.PrimaryKeyConstraint('donor_id', 'bloodbank_id', 'date')
    )
    op.create_table('utilisation',
    sa.Column('bloodbank_id', sa.Integer(), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('blood_group', sa.String(length=5), nullable=False),
    sa.Column('units', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bloodbank_id'], ['bloodbank.id'], ),
    sa.PrimaryKeyConstraint('bloodbank_id', 'date_time')
    )
    op.create_table('request',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('blood_group', sa.String(length=5), nullable=False),
    sa.Column('units', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['app_user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'date')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    op.drop_table('utilisation')
    op.drop_table('donation')
    op.drop_table('bloodbank_stats')
    op.drop_table('app_user')
    op.drop_table('donor')
    op.drop_table('bloodbank')
    # ### end Alembic commands ###
