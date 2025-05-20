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
        'Victor Guilherme',
        '$argon2id$v=19$m=65536,t=3,p=4$HMOY837v3VvLGeO8t1YKgQ$2wzGWnyNOEUo/ljgiCiuN/IdFsWOJUWn1WzLxa+xrIc',
        'v.guilherme.barreto@gmail.com',
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
