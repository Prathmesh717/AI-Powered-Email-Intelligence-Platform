from alembic import op

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE approval_requests
            ALTER COLUMN resolved_by TYPE VARCHAR(128) USING resolved_by::text
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE approval_requests
            ALTER COLUMN resolved_by TYPE UUID USING resolved_by::uuid
        """
    )
