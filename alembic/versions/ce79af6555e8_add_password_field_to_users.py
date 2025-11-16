"""add_password_field_to_users

Revision ID: ce79af6555e8
Revises: 8bf99c83cda3
Create Date: 2025-11-16 16:38:25.996019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce79af6555e8'
down_revision: Union[str, Sequence[str], None] = '8bf99c83cda3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('hashed_password', sa.String(length=255), nullable=False, server_default=''))
    # Note: If you have existing users, you'll need to set their passwords manually
    # or make this nullable=True initially, then update existing users, then make it nullable=False


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'hashed_password')
