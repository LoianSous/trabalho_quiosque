from alembic import op
import sqlalchemy as sa

revision = 'c173c5b98921'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('passphrase', sa.String(length=128), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('u_type', sa.Enum('ADMIN', 'USER', name='user_type'), nullable=False),
        sa.Column('u_state', sa.Enum('ACTIVE', 'INACTIVE', 'BLOCKED', name='user_state'), nullable=False),
        sa.Column('dt_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('dt_updated', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table('devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ip', sa.String(length=128), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('locale', sa.String(length=128), nullable=False),
        sa.Column('group', sa.String(length=128), nullable=True),
        sa.Column('a_state', sa.Enum('ACTIVE', 'INACTIVE', 'BLOCKED', name='device_state'), nullable=False),
        sa.Column('dt_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('dt_updated', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('files_trk',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=128), nullable=True),
        sa.Column('filepath', sa.String(length=128), nullable=False),
        sa.Column('file_state', sa.Enum('UPLOADED', 'PROCESSED', 'DELETED', name='file_state'), nullable=False),
        sa.Column('dt_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('dt_updated', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('files_trk')
    op.drop_table('devices')
    op.drop_table('users')
