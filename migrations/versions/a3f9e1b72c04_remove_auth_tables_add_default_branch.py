"""remove auth tables and add default_branch to repositories

Revision ID: a3f9e1b72c04
Revises: d5cbe78df4b1
Create Date: 2026-05-15 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

revision: str = 'a3f9e1b72c04'
down_revision: Union[str, None] = 'd5cbe78df4b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop notifications first — references users, api_changes, impact_analysis
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.drop_table('notifications')

    # Drop user_projects — references users, projects
    op.drop_table('user_projects')

    # Drop users — references organizations
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

    # Remove project_id FK and column from repositories before dropping projects
    op.drop_constraint(op.f('fk_repositories_project_id_projects'), 'repositories', type_='foreignkey')
    op.drop_column('repositories', 'project_id')

    # Drop projects — references organizations
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')

    # Drop organizations
    op.drop_index(op.f('ix_organizations_id'), table_name='organizations')
    op.drop_table('organizations')

    # Add default_branch to repositories
    op.add_column('repositories', sa.Column('default_branch', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    op.drop_column('repositories', 'default_branch')

    op.create_table('organizations',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_organizations'))
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'], unique=False)

    op.create_table('projects',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name=op.f('fk_projects_organization_id_organizations')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_projects'))
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)

    op.add_column('repositories', sa.Column('project_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(
        op.f('fk_repositories_project_id_projects'),
        'repositories', 'projects',
        ['project_id'], ['id']
    )

    op.create_table('users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name=op.f('fk_users_organization_id_organizations')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    op.create_table('user_projects',
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('project_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name=op.f('fk_user_projects_project_id_projects')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_projects_user_id_users')),
        sa.PrimaryKeyConstraint('user_id', 'project_id', name=op.f('pk_user_projects'))
    )

    op.create_table('notifications',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('message', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('impact_analysis_id', sa.Uuid(), nullable=False),
        sa.Column('api_change_id', sa.Uuid(), nullable=False),
        sa.Column('recipient_id', sa.Uuid(), nullable=False),
        sa.Column('channel', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(['api_change_id'], ['api_changes.id'], name=op.f('fk_notifications_api_change_id_api_changes')),
        sa.ForeignKeyConstraint(['impact_analysis_id'], ['impact_analysis.id'], name=op.f('fk_notifications_impact_analysis_id_impact_analysis')),
        sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], name=op.f('fk_notifications_recipient_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_notifications'))
    )
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=False)
