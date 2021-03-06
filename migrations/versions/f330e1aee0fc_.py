"""empty message

Revision ID: f330e1aee0fc
Revises: 
Create Date: 2020-07-03 13:01:21.697587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f330e1aee0fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organization',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('firstname', sa.String(length=80), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.Column('activision_id', sa.String(length=80), nullable=True),
    sa.Column('stream_url', sa.String(length=255), nullable=True),
    sa.Column('stream_type', sa.String(length=25), nullable=True),
    sa.Column('avatar_url', sa.String(length=255), nullable=True),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('gender', sa.CHAR(length=1), nullable=True),
    sa.Column('registration_date', sa.DateTime(), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('account_verified', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('org_role',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('organization_id', sa.CHAR(length=36), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tournament',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('organization_id', sa.CHAR(length=36), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_otp',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('sg_message_id', sa.String(length=30), nullable=True),
    sa.Column('exp_time', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.CHAR(length=36), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('org_roles_users',
    sa.Column('user_id', sa.CHAR(length=36), nullable=True),
    sa.Column('role_id', sa.CHAR(length=36), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['org_role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )
    op.create_table('role',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('tournament_id', sa.CHAR(length=36), nullable=True),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournament.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.CHAR(length=36), nullable=True),
    sa.Column('role_id', sa.CHAR(length=36), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('role')
    op.drop_table('org_roles_users')
    op.drop_table('user_otp')
    op.drop_table('tournament')
    op.drop_table('org_role')
    op.drop_table('user')
    op.drop_table('organization')
    # ### end Alembic commands ###
