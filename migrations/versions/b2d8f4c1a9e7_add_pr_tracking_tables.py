"""add PR tracking tables and restructure api_changes

Adds pull_requests, service_changes, api_call_changes tables.
Restructures api_changes to capture the full API state change per PR
instead of a single commit reference.

Revision ID: b2d8f4c1a9e7
Revises: a3f9e1b72c04
Create Date: 2026-05-15 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

revision: str = 'b2d8f4c1a9e7'
down_revision: Union[str, None] = 'a3f9e1b72c04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- pull_requests ---
    op.create_table(
        'pull_requests',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('pr_number', sa.Integer(), nullable=False),
        sa.Column('pr_title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('head_branch', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('base_branch', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('repository_id', sa.Uuid(), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(['repository_id'], ['repositories.id'], name=op.f('fk_pull_requests_repository_id_repositories')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_pull_requests')),
    )
    op.create_index(op.f('ix_pull_requests_id'), 'pull_requests', ['id'], unique=False)

    # --- service_changes ---
    op.create_table(
        'service_changes',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('pr_id', sa.Uuid(), nullable=False),
        sa.Column('source_service_id', sa.Uuid(), nullable=True),
        sa.Column('change_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('change_degree', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('language', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('path', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(['pr_id'], ['pull_requests.id'], name=op.f('fk_service_changes_pr_id_pull_requests')),
        sa.ForeignKeyConstraint(['source_service_id'], ['services.id'], name=op.f('fk_service_changes_source_service_id_services')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_service_changes')),
    )
    op.create_index(op.f('ix_service_changes_id'), 'service_changes', ['id'], unique=False)

    # --- restructure api_changes ---
    # Drop the old commit_id column and its FK, then add the new columns.
    op.drop_column('api_changes', 'commit_id')

    # Added as nullable to handle any pre-existing rows; the model enforces NOT NULL at app level.
    op.add_column('api_changes', sa.Column('pr_id', sa.Uuid(), nullable=True))
    op.add_column('api_changes', sa.Column('service_change_id', sa.Uuid(), nullable=True))
    op.add_column('api_changes', sa.Column('method', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('api_changes', sa.Column('endpoint_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('api_changes', sa.Column('file_path', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('api_changes', sa.Column('line_number', sa.Integer(), nullable=True))
    op.add_column('api_changes', sa.Column('old_request_schema', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('api_changes', sa.Column('new_request_schema', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('api_changes', sa.Column('old_response_schema', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('api_changes', sa.Column('new_response_schema', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('api_changes', sa.Column('version', sqlmodel.sql.sqltypes.AutoString(), nullable=True))

    op.create_foreign_key(
        op.f('fk_api_changes_pr_id_pull_requests'),
        'api_changes', 'pull_requests', ['pr_id'], ['id'],
    )
    op.create_foreign_key(
        op.f('fk_api_changes_service_change_id_service_changes'),
        'api_changes', 'service_changes', ['service_change_id'], ['id'],
    )

    # --- api_call_changes ---
    op.create_table(
        'api_call_changes',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('pr_id', sa.Uuid(), nullable=False),
        sa.Column('source_api_call_id', sa.Uuid(), nullable=True),
        sa.Column('service_from_change_id', sa.Uuid(), nullable=True),
        sa.Column('service_to_change_id', sa.Uuid(), nullable=True),
        sa.Column('api_change_id', sa.Uuid(), nullable=True),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('change_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('change_degree', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('file_path', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('line_number', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['api_change_id'], ['api_changes.id'], name=op.f('fk_api_call_changes_api_change_id_api_changes')),
        sa.ForeignKeyConstraint(['pr_id'], ['pull_requests.id'], name=op.f('fk_api_call_changes_pr_id_pull_requests')),
        sa.ForeignKeyConstraint(['service_from_change_id'], ['service_changes.id'], name=op.f('fk_api_call_changes_service_from_change_id_service_changes')),
        sa.ForeignKeyConstraint(['service_to_change_id'], ['service_changes.id'], name=op.f('fk_api_call_changes_service_to_change_id_service_changes')),
        sa.ForeignKeyConstraint(['source_api_call_id'], ['api_calls.id'], name=op.f('fk_api_call_changes_source_api_call_id_api_calls')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_api_call_changes')),
    )
    op.create_index(op.f('ix_api_call_changes_id'), 'api_call_changes', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_api_call_changes_id'), table_name='api_call_changes')
    op.drop_table('api_call_changes')

    op.drop_constraint(op.f('fk_api_changes_service_change_id_service_changes'), 'api_changes', type_='foreignkey')
    op.drop_constraint(op.f('fk_api_changes_pr_id_pull_requests'), 'api_changes', type_='foreignkey')
    op.drop_column('api_changes', 'version')
    op.drop_column('api_changes', 'new_response_schema')
    op.drop_column('api_changes', 'old_response_schema')
    op.drop_column('api_changes', 'new_request_schema')
    op.drop_column('api_changes', 'old_request_schema')
    op.drop_column('api_changes', 'line_number')
    op.drop_column('api_changes', 'file_path')
    op.drop_column('api_changes', 'endpoint_url')
    op.drop_column('api_changes', 'method')
    op.drop_column('api_changes', 'service_change_id')
    op.drop_column('api_changes', 'pr_id')
    op.add_column('api_changes', sa.Column('commit_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False))

    op.drop_index(op.f('ix_service_changes_id'), table_name='service_changes')
    op.drop_table('service_changes')

    op.drop_index(op.f('ix_pull_requests_id'), table_name='pull_requests')
    op.drop_table('pull_requests')
