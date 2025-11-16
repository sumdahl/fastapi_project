"""change_user_id_to_uuid

Revision ID: 2a2a4feb2fdb
Revises: ce79af6555e8
Create Date: 2025-11-16 17:04:49.807786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '2a2a4feb2fdb'
down_revision: Union[str, Sequence[str], None] = 'ce79af6555e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Enable UUID extension for PostgreSQL
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Drop the existing index on id
    op.drop_index(op.f('ix_users_id'), table_name='users')
    
    # Drop the old primary key constraint (must be done before dropping the column)
    op.drop_constraint('users_pkey', 'users', type_='primary')
    
    # Add a new UUID column
    op.add_column('users', sa.Column('id_new', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Generate UUIDs for existing rows
    op.execute('UPDATE users SET id_new = uuid_generate_v4()')
    
    # Make the new column NOT NULL
    op.alter_column('users', 'id_new', nullable=False)
    
    # Drop the old integer id column
    op.drop_column('users', 'id')
    
    # Rename the new column to id using raw SQL
    op.execute('ALTER TABLE users RENAME COLUMN id_new TO id')
    
    # Recreate the primary key constraint
    op.create_primary_key('users_pkey', 'users', ['id'])
    
    # Recreate the index
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the UUID index
    op.drop_index(op.f('ix_users_id'), table_name='users')
    
    # Drop the primary key constraint
    op.drop_constraint('users_pkey', 'users', type_='primary')
    
    # Add back the integer id column
    op.add_column('users', sa.Column('id_old', sa.Integer(), nullable=True))
    
    # Generate sequential IDs for existing rows
    op.execute('''
        WITH numbered AS (
            SELECT id, ROW_NUMBER() OVER (ORDER BY email) as rn
            FROM users
        )
        UPDATE users SET id_old = numbered.rn
        FROM numbered
        WHERE users.id = numbered.id
    ''')
    
    # Make the integer column NOT NULL
    op.alter_column('users', 'id_old', nullable=False)
    
    # Drop the UUID column
    op.drop_column('users', 'id')
    
    # Rename the integer column to id using raw SQL
    op.execute('ALTER TABLE users RENAME COLUMN id_old TO id')
    
    # Recreate the primary key constraint
    op.create_primary_key('users_pkey', 'users', ['id'])
    
    # Recreate the index
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
