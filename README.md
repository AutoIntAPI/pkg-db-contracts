# pkg-db-contracts

Shared database contracts package for internal services.

## What this package provides

- SQLAlchemy ORM model definitions grouped by schema/domain.
- A shared declarative base with naming conventions.
- Alembic migration configuration and scripts.
- Optional utility helpers for engine/session creation.

## Project layout

- `src/db_contracts/base.py`: Declarative base + metadata naming conventions.
- `src/db_contracts/models/*.py`: Domain model modules (`auth`, `dependency`, `analysis`, `fixgen`, `ai`).
- `src/db_contracts/models/__init__.py`: Model import aggregator.
- `src/db_contracts/db.py`: SQLAlchemy engine/session helpers.
- `migrations/`: Alembic migration environment.

## Local setup

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows (PowerShell: .venv\Scripts\Activate.ps1)
pip install -e ".[dev]"
```

## Run checks

```bash
ruff check .
pytest
```

## Build package

```bash
python -m build
```

## Migrations

Set `DATABASE_URL` then run:

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

## Versioning

Use semantic versioning.

- `MAJOR`: breaking model/contract changes
- `MINOR`: backward-compatible additions
- `PATCH`: bug fixes

## Installation

```bash
# In terminal, set GITHUB_TOKEN env variable with appropriate permissions
pip install git+https://${GITHUB_TOKEN}@github.com/AutoIntAPI/pkg-db-contracts.git

# or in requirements.txt
db-contract @ git+https://${GITHUB_TOKEN}@github.com/AutoIntAPI/pkg-db-contracts.git
```