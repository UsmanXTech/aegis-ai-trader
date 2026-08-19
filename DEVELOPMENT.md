# Development Guide

## Requirements

### Backend

`pyproject.toml` requires Python `>=3.11` and defines the backend dependencies and development tools.

### Frontend

`dashboard/package.json` defines a React + TypeScript + Vite application. The repository does not pin a Node.js version; exact Node/npm compatibility is therefore **Needs verification**.

## Python installation

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\\Scripts\\activate
pip install -e ".[dev]"
```

## Configuration

```bash
cp .env.example .env
```

Configuration is loaded by `src/aegis/config.py` using `.env`. See [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) and [`README.md`](README.md) for the verified variable list.

Keep credentials local. The repository's `.env.example` contains empty placeholders only.

## Run the API

The FastAPI application object is `aegis.api:app`.

```bash
uvicorn aegis.api:app --reload
```

## Run the dashboard

```bash
cd dashboard
npm install
npm run dev
```

The dashboard uses `VITE_API_URL` when set; otherwise it calls `http://localhost:8000`.

## Build the dashboard

```bash
cd dashboard
npm run build
npm run preview
```

## Tests

Full suite:

```bash
pytest
```

Verbose:

```bash
pytest -v
```

Focused example:

```bash
pytest -v tests/test_risk.py tests/test_trade_pipeline.py
```

## Lint

```bash
ruff check .
```

There is no separate formatter command configured in `pyproject.toml`; Ruff is currently configured for linting only.

## CI

`.github/workflows/test.yml` runs on pushes and pull requests using Ubuntu and Python 3.11:

```text
checkout
→ setup Python 3.11
→ upgrade pip
→ pip install -e ".[dev]"
→ ruff check .
→ pytest -q
```

## Debugging workflow

1. Reproduce with the smallest relevant unit test.
2. Trace the call path from the public entry point into the existing abstraction.
3. For trading behavior, inspect both the initial risk decision and the post-selection risk recheck.
4. For order issues, inspect `contract_selector.py`, `execution.py`, `paper_controller.py`, and the relevant gateway.
5. For MCP issues, inspect `mcp_client.py`, `mcp_registry.py`, and `mcp_tools.py`; do not guess external tool schemas.
6. For API/dashboard issues, inspect the event type and JSON payload stored by `AegisStore`.

## Database setup

There is no migration framework. `AegisStore` creates `data/aegis.db` and its `events` table automatically when instantiated.

There is no verified seed-data command.

## Historical research data

The repository contains a vendor-neutral schema and CSV/Parquet loader, but no verified production historical-options dataset. Dataset source, download procedure, licensing, and expected coverage are **Needs verification**.

## Broker/MCP development

Use Alpaca paper credentials only. Do not commit credentials.

Recommended progression:

```text
Unit tests
→ mocked broker/MCP tests
→ MCP initialize/tools discovery
→ paper account read
→ options data read
→ paper order submission
→ order status/position synchronization
```

Do not treat a successful unit test as proof of broker compatibility.

## Database migration workflow

**Not applicable / Unknown.** There is currently no migration tool. If the SQLite schema is changed, document the exact schema change in [`DATABASE.md`](DATABASE.md), add/adjust tests, and record the architectural decision when appropriate.

## Deployment

**Unknown.** No verified production deployment manifest or hosting configuration is present in the repository tree. Do not invent deployment commands.

## Common failure areas

| Area | Likely cause | First place to inspect |
|---|---|---|
| Import errors | Environment not installed with editable package | `pyproject.toml` |
| Test failures | Contract changed without corresponding unit tests | `tests/` and target module |
| Risk rejection | Account/portfolio constraints or spread max-loss | `risk.py`, `risk_pipeline.py`, `options_risk.py` |
| Order rejection | Invalid legs/payload | `contract_selector.py`, `execution.py` |
| MCP failure | Tool/schema/process mismatch | `mcp_client.py`, `mcp_registry.py`, `mcp_tools.py` |
| Dashboard empty | API unavailable or no events | `api.py`, `store.py`, dashboard `main.tsx` |
| Account display error | Unexpected `account` event payload | `dashboard/src/main.tsx` |

## Before a pull request

```bash
ruff check .
pytest -q
```

For frontend changes, also run:

```bash
cd dashboard
npm run build
```

Review the diff for secrets and verify documentation for changed APIs/configuration/database behavior.
