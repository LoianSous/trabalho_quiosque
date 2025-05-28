"""user_master_add

Revision ID: fca89f1b9733
Revises: c173c5b98921
Create Date: 2025-05-20 15:23:27.702092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fca89f1b9733'
down_revision = 'c173c5b98921'
branch_labels = None
depends_on = None


def upgrade():
    
    op.execute("""
        INSERT INTO users(
            id,
            name,
            passphrase,
            email,
            u_type,
            u_state,
            dt_created,
            dt_updated
            )
        VALUES (
        0,
        'sa',
        'scrypt:32768:8:1$ZF6omYpojhSj81dP$f51d06b894bb60c9e5b79ed04e3f276e4230d4bd1ff73e02ddbd6025ea8c1039aa885755ec1ef4b53ffea4fe5065164d983f8a94905b9d60de939f9b0cf5584f',
        'super@admin.com',
        'ADMIN',
        'ACTIVE',
        datetime('now'),
        datetime('now'));
            """)


def downgrade():
    op.execute(
        """
        DELETE FROM users WHERE id = 0;
        """
    )
