"""converted a column type in fix_records

Revision ID: 8e5deb67bd9f
Revises: 7cfd4627dd06
Create Date: 2026-06-28 11:32:17.845243
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8e5deb67bd9f'
down_revision: Union[str, None] = '7cfd4627dd06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        op.f('fk_fix_records_downstream_service_id_services'),
        'fix_records',
        type_='foreignkey',
    )
    op.alter_column(
        'fix_records',
        'downstream_service_id',
        existing_type=sa.UUID(),
        type_=sa.ARRAY(sa.UUID()),
        nullable=True,
        postgresql_using='ARRAY[downstream_service_id]',
    )


def downgrade() -> None:
    op.alter_column(
        'fix_records',
        'downstream_service_id',
        existing_type=sa.ARRAY(sa.UUID()),
        type_=sa.UUID(),
        nullable=False,
        postgresql_using='downstream_service_id[1]',
    )
    op.create_foreign_key(
        op.f('fk_fix_records_downstream_service_id_services'),
        'fix_records',
        'services',
        ['downstream_service_id'],
        ['id'],
    )
