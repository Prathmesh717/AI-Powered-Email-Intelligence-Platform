from alembic import op

revision = "009"
down_revision = "008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_users (
            id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            username       VARCHAR(128) UNIQUE NOT NULL,
            password_hash  TEXT,
            role           VARCHAR(32)  NOT NULL DEFAULT 'viewer',
            workspace_id   UUID,
            auth_provider  VARCHAR(32)  NOT NULL DEFAULT 'local',
            external_subject TEXT,
            mfa_secret     TEXT,
            mfa_enabled    BOOLEAN NOT NULL DEFAULT FALSE,
            disabled       BOOLEAN NOT NULL DEFAULT FALSE,
            created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_auth_users_external_subject "
        "ON auth_users (external_subject) WHERE external_subject IS NOT NULL"
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_refresh_tokens (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id     UUID NOT NULL REFERENCES auth_users(id) ON DELETE CASCADE,
            family_id   UUID NOT NULL,
            token_hash  CHAR(64) UNIQUE NOT NULL,
            issued_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
            expires_at  TIMESTAMPTZ NOT NULL,
            used_at     TIMESTAMPTZ,
            revoked     BOOLEAN NOT NULL DEFAULT FALSE
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_auth_refresh_family ON auth_refresh_tokens (family_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_auth_refresh_user ON auth_refresh_tokens (user_id)")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS auth_refresh_tokens")
    op.execute("DROP TABLE IF EXISTS auth_users")
