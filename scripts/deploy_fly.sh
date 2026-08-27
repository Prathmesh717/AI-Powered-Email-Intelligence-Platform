#!/usr/bin/env bash
# Deploy Smartai's 3 services to Fly.io in the right order.
#
# Prereqs:
#   - fly CLI installed + authenticated (`fly auth login`)
#   - The 3 apps already created (see fly/*.toml headers for one-time setup)
#   - Secrets already set per fly/*.toml comments
#   - Postgres provisioned + attached to Smartai-api
#
# Run:
#   bash scripts/deploy_fly.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Deploying MCP tool server (Smartai-mcp)"
fly deploy -a Smartai-mcp -c fly/mcp.toml --remote-only

echo "==> Deploying API (Smartai-api) — runs alembic migrations as release_command"
fly deploy -a Smartai-api -c fly/api.toml --remote-only

echo "==> Deploying frontend console (Smartai-console)"
fly deploy -a Smartai-console -c fly/frontend.toml --remote-only

echo
echo "Done. Health-check the deployment:"
echo "  fly status -a Smartai-api"
echo "  curl https://Smartai-console.fly.dev/api/health"
echo
echo "Console URL:"
echo "  fly info -a Smartai-console --json | jq -r '.Hostname' | awk '{print \"https://\" \$0}'"
