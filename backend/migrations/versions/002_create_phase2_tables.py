"""Phase 2 - Create media, transcripts, analysis tables

Revision ID: 002
Revises: 001
Create Date: 2026-10-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_projects_user_id', 'projects', ['user_id'])

    # Create media_assets table
    op.create_table(
        'media_assets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('original_filename', sa.String(255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('fps', sa.Float(), nullable=True),
        sa.Column('codec', sa.String(50), nullable=True),
        sa.Column('original_file_path', sa.String(500), nullable=False),
        sa.Column('proxy_file_path', sa.String(500), nullable=True),
        sa.Column('thumbnail_path', sa.String(500), nullable=True),
        sa.Column('status', sa.Enum('uploading', 'ready', 'processing', 'error', name='mediastatusenum'), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('upload_session_id', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_media_assets_project_id', 'media_assets', ['project_id'])
    op.create_index('ix_media_assets_user_id', 'media_assets', ['user_id'])
    op.create_index('ix_media_assets_status', 'media_assets', ['status'])

    # Create transcripts table
    op.create_table(
        'transcripts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('media_asset_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('segments', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('language', sa.String(10), nullable=False, server_default='vi'),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'error', name='transcriptstatusenum'), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('provider', sa.String(50), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['media_asset_id'], ['media_assets.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_transcripts_media_asset_id', 'transcripts', ['media_asset_id'])
    op.create_index('ix_transcripts_status', 'transcripts', ['status'])

    # Create video_analyses table
    op.create_table(
        'video_analyses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('media_asset_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('silence_segments', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('speech_segments', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('scene_changes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('key_phrases', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('highlights', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('suggested_cuts', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('suggested_structure', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'error', name='analysisstatusenum'), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['media_asset_id'], ['media_assets.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_video_analyses_media_asset_id', 'video_analyses', ['media_asset_id'])
    op.create_index('ix_video_analyses_status', 'video_analyses', ['status'])

    # Create brand_templates table
    op.create_table(
        'brand_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('logo_url', sa.String(500), nullable=True),
        sa.Column('intro_video_path', sa.String(500), nullable=True),
        sa.Column('outro_video_path', sa.String(500), nullable=True),
        sa.Column('colors', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('fonts', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('call_to_action', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('subtitle_template', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_brand_templates_user_id', 'brand_templates', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_brand_templates_user_id', table_name='brand_templates')
    op.drop_table('brand_templates')

    op.drop_index('ix_video_analyses_status', table_name='video_analyses')
    op.drop_index('ix_video_analyses_media_asset_id', table_name='video_analyses')
    op.drop_table('video_analyses')

    op.drop_index('ix_transcripts_status', table_name='transcripts')
    op.drop_index('ix_transcripts_media_asset_id', table_name='transcripts')
    op.drop_table('transcripts')

    op.drop_index('ix_media_assets_status', table_name='media_assets')
    op.drop_index('ix_media_assets_user_id', table_name='media_assets')
    op.drop_index('ix_media_assets_project_id', table_name='media_assets')
    op.drop_table('media_assets')

    op.drop_index('ix_projects_user_id', table_name='projects')
    op.drop_table('projects')
