"""add interview columns

Revision ID: 0001_add_interview_columns
Revises: 
Create Date: 2026-08-08 14:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_add_interview_columns'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add interview columns if missing. For SQLite this is acceptable for simple adds.
    op.add_column('interviews', sa.Column('candidate_name', sa.String(length=255), nullable=True))
    op.add_column('interviews', sa.Column('position', sa.String(length=255), nullable=True))
    op.add_column('interviews', sa.Column('interviewer', sa.String(length=255), nullable=True))
    op.add_column('interviews', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('interviews', sa.Column('scheduled_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('interviews', 'scheduled_at')
    op.drop_column('interviews', 'notes')
    op.drop_column('interviews', 'interviewer')
    op.drop_column('interviews', 'position')
    op.drop_column('interviews', 'candidate_name')
