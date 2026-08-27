from alembic import op

revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE workflow_runs
            ALTER COLUMN user_id TYPE VARCHAR(128) USING user_id::text
        """
    )


def downgrade() -> None:
    # Non-UUID values (e.g. "rep-1") cannot cast back to UUID; null them first
    # so the type change cannot fail on legacy string ids.
    op.execute(
        """
        UPDATE workflow_runs
           SET user_id = NULL
         WHERE user_id !~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        """
    )
    op.execute(
        """
        ALTER TABLE workflow_runs
            ALTER COLUMN user_id TYPE UUID USING user_id::uuid
        """
    )
