from __future__ import annotations

import logging
import uuid

import asyncpg

logger = logging.getLogger(__name__)


async def user_workspaces(pool: asyncpg.Pool, user_id: str) -> set[str]:
    """Return the set of workspace UUIDs this user belongs to.

    Returns an empty set when the user is unknown, when the user_id is not a
    UUID, or when the workspace_members table is missing (pre-migration). The
    caller decides whether an empty set is "no workspace claim allowed" or
    "single-tenant fallback".
    """
    try:
        uuid.UUID(user_id)
    except (ValueError, TypeError):
        return set()

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT workspace_id::text AS ws FROM workspace_members WHERE user_id = $1",
                uuid.UUID(user_id),
            )
            return {r["ws"] for r in rows}
    except asyncpg.UndefinedTableError:
        # Migration 005 not applied yet — single-tenant deployment.
        return set()
    except Exception as exc:
        logger.warning("workspace_members lookup failed: %s", exc)
        return set()


async def user_is_member(pool: asyncpg.Pool, user_id: str, workspace_id: str) -> bool:
    """Return True if (user_id, workspace_id) ∈ workspace_members.

    Returns False on any UUID parse failure or DB error — fail closed.
    """
    try:
        uuid.UUID(user_id)
        uuid.UUID(workspace_id)
    except (ValueError, TypeError):
        return False

    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT 1 FROM workspace_members
                WHERE user_id = $1 AND workspace_id = $2
                LIMIT 1
                """,
                uuid.UUID(user_id),
                uuid.UUID(workspace_id),
            )
            return row is not None
    except asyncpg.UndefinedTableError:
        # Pre-migration: deny rather than silently allow cross-tenant.
        return False
    except Exception as exc:
        logger.warning("workspace_members membership check failed: %s", exc)
        return False
