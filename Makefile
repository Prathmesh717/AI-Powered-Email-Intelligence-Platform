.PHONY: up down migrate test lint fmt build logs demo

# ── Local development ──────────────────────────────────────────────
up:
	docker compose up

up-d:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose --profile migration run --rm migrate

build:
	docker compose build

logs:
	docker compose logs -f

# ── Database ───────────────────────────────────────────────────────
seed:
	docker compose exec api python scripts/seed_db.py

# ── Testing ────────────────────────────────────────────────────────
test:
	pytest tests/unit tests/integration -v --cov=Smartai --cov-report=term-missing

test-unit:
	pytest tests/unit -v

test-integration:
	pytest tests/integration -v

# ── Code quality ───────────────────────────────────────────────────
lint:
	ruff check Smartai/ dashboard/ tests/
	mypy Smartai/ --ignore-missing-imports

fmt:
	ruff format Smartai/ dashboard/ tests/

# ── Demo ───────────────────────────────────────────────────────────
demo:
	python scripts/run_demo.py

eval:
	python scripts/generate_eval_dataset.py

# ── Help ───────────────────────────────────────────────────────────
help:
	@echo "Smartai Makefile targets:"
	@echo "  up         Start all services"
	@echo "  down       Stop all services"
	@echo "  migrate    Run Alembic migrations"
	@echo "  test       Run all tests with coverage"
	@echo "  lint       Run ruff + mypy"
	@echo "  fmt        Auto-format with ruff"
	@echo "  demo       Run demo workflow"
	@echo "  seed       Seed demo data"
