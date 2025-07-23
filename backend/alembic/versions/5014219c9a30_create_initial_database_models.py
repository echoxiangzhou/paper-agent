"""Create initial database models

Revision ID: 5014219c9a30
Revises: 
Create Date: 2025-07-23 21:48:07.677080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5014219c9a30'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create categories table
    op.create_table('categories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=False)

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create keywords table
    op.create_table('keywords',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('keyword', sa.String(length=200), nullable=False),
        sa.Column('aliases', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.Column('auto_collect', sa.Boolean(), nullable=False),
        sa.Column('papers_count', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_keywords_category_id'), 'keywords', ['category_id'], unique=False)
    op.create_index(op.f('ix_keywords_keyword'), 'keywords', ['keyword'], unique=False)
    op.create_index(op.f('ix_keywords_user_id'), 'keywords', ['user_id'], unique=False)

    # Create papers table
    op.create_table('papers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('authors', sa.Text(), nullable=True),
        sa.Column('abstract', sa.Text(), nullable=True),
        sa.Column('journal', sa.String(length=200), nullable=True),
        sa.Column('publication_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('volume', sa.String(length=50), nullable=True),
        sa.Column('issue', sa.String(length=50), nullable=True),
        sa.Column('pages', sa.String(length=50), nullable=True),
        sa.Column('doi', sa.String(length=200), nullable=True),
        sa.Column('arxiv_id', sa.String(length=50), nullable=True),
        sa.Column('pmid', sa.String(length=20), nullable=True),
        sa.Column('pdf_url', sa.String(length=500), nullable=True),
        sa.Column('web_url', sa.String(length=500), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('full_text', sa.Text(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('keywords', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'SKIPPED', name='paperstatus'), nullable=False),
        sa.Column('citation_count', sa.Integer(), nullable=False),
        sa.Column('impact_factor', sa.Float(), nullable=True),
        sa.Column('h_index', sa.Float(), nullable=True),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('processing_metadata', sa.JSON(), nullable=True),
        sa.Column('content_hash', sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_papers_arxiv_id'), 'papers', ['arxiv_id'], unique=True)
    op.create_index(op.f('ix_papers_content_hash'), 'papers', ['content_hash'], unique=True)
    op.create_index(op.f('ix_papers_doi'), 'papers', ['doi'], unique=True)
    op.create_index(op.f('ix_papers_pmid'), 'papers', ['pmid'], unique=True)
    op.create_index(op.f('ix_papers_status'), 'papers', ['status'], unique=False)
    op.create_index(op.f('ix_papers_title'), 'papers', ['title'], unique=False)

    # Create email_configs table
    op.create_table('email_configs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email_address', sa.String(length=255), nullable=False),
        sa.Column('provider', sa.Enum('GMAIL', 'OUTLOOK', 'QQ', 'NETEASE', 'IMAP', name='emailprovider'), nullable=False),
        sa.Column('imap_server', sa.String(length=100), nullable=False),
        sa.Column('imap_port', sa.Integer(), nullable=False),
        sa.Column('use_ssl', sa.Boolean(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('app_password', sa.String(length=255), nullable=True),
        sa.Column('inbox_folder', sa.String(length=50), nullable=False),
        sa.Column('processed_folder', sa.String(length=50), nullable=True),
        sa.Column('search_keywords', sa.Text(), nullable=True),
        sa.Column('sender_filters', sa.Text(), nullable=True),
        sa.Column('subject_filters', sa.Text(), nullable=True),
        sa.Column('auto_process', sa.Boolean(), nullable=False),
        sa.Column('process_interval', sa.Integer(), nullable=False),
        sa.Column('max_emails_per_batch', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('last_check', sa.String(length=50), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('connection_status', sa.String(length=20), nullable=False),
        sa.Column('total_processed', sa.Integer(), nullable=False),
        sa.Column('papers_found', sa.Integer(), nullable=False),
        sa.Column('last_paper_count', sa.Integer(), nullable=False),
        sa.Column('advanced_settings', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_configs_email_address'), 'email_configs', ['email_address'], unique=False)
    op.create_index(op.f('ix_email_configs_user_id'), 'email_configs', ['user_id'], unique=False)

    # Create user_papers table
    op.create_table('user_papers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('paper_id', sa.Integer(), nullable=False),
        sa.Column('keyword_id', sa.Integer(), nullable=True),
        sa.Column('read_status', sa.Enum('UNREAD', 'READING', 'READ', 'SAVED', 'ARCHIVED', name='readstatus'), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tags', sa.Text(), nullable=True),
        sa.Column('bookmarked', sa.Boolean(), nullable=False),
        sa.Column('shared', sa.Boolean(), nullable=False),
        sa.Column('downloaded', sa.Boolean(), nullable=False),
        sa.Column('last_read_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reading_progress', sa.Float(), nullable=False),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('collected_from', sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(['keyword_id'], ['keywords.id'], ),
        sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_papers_keyword_id'), 'user_papers', ['keyword_id'], unique=False)
    op.create_index(op.f('ix_user_papers_paper_id'), 'user_papers', ['paper_id'], unique=False)
    op.create_index(op.f('ix_user_papers_read_status'), 'user_papers', ['read_status'], unique=False)
    op.create_index(op.f('ix_user_papers_user_id'), 'user_papers', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user_papers')
    op.drop_table('email_configs')
    op.drop_table('papers')
    op.drop_table('keywords')
    op.drop_table('users')
    op.drop_table('categories')
