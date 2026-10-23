"""Phase 3 - Create timeline tables

Revision ID: 003
Revises: 002
Create Date: 2026-10-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create timelines table
    op.create_table(
        'timelines',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('duration', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('fps', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('width', sa.Integer(), nullable=False, server_default='1920'),
        sa.Column('height', sa.Integer(), nullable=False, server_default='1080'),
        sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_current', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_timelines_project_id', 'timelines', ['project_id'])
    op.create_index('ix_timelines_version', 'timelines', ['version'])

    # Create timeline_versions table
    op.create_table(
        'timeline_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timeline_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('is_autosave', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['timeline_id'], ['timelines.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_timeline_versions_timeline_id', 'timeline_versions', ['timeline_id'])

    # Create timeline_actions table
    op.create_table(
        'timeline_actions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timeline_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('action_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('action_order', sa.Integer(), nullable=False),
        sa.Column('is_undo', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['timeline_id'], ['timelines.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_timeline_actions_timeline_id', 'timeline_actions', ['timeline_id'])


def downgrade() -> None:
    op.drop_index('ix_timeline_actions_timeline_id', table_name='timeline_actions')
    op.drop_table('timeline_actions')

    op.drop_index('ix_timeline_versions_timeline_id', table_name='timeline_versions')
    op.drop_table('timeline_versions')

    op.drop_index('ix_timelines_version', table_name='timelines')
    op.drop_index('ix_timelines_project_id', table_name='timelines')
    op.drop_table('timelines')
