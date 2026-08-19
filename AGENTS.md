# AGENTS.md — Aegis AI Trader Agent Guide

## Purpose

Aegis AI Trader is a Python-based autonomous options-trading system designed for Alpaca **paper trading**. It combines market scanning, strategy selection, options contract selection, deterministic risk controls, multi-leg order construction, paper-execution boundaries, synchronization, journaling, and a React dashboard.

The repository is currently an engineering/research system, not a verified live-trading production system. Treat paper-only safety as a hard constraint.

## Quick project map

```text
src/aegis/                 Python application package
  api.py                   FastAPI app
  runner.py                One analysis/preparation cycle
  agent.py                 Strategy + risk coordination
  scanner.py               Market scanning
  strategies.py            Strategy selection
  regime.py                Market-regime logic
  contract_selector.py     Option spread selection
  options*.py              Option domain, intelligence, risk, backtesting
  risk*.py                 Risk engine and risk pipeline
  execution.py             Alpaca-compatible MLeg payload builder
  execution_gate.py        Risk/paper execution boundary
  paper_*.py               Paper broker/controller/loop components
  mcp_*.py                 MCP client, registry, gateway, tool adapter
  *sync.py                 Account/position synchronization
  monitor.py               Position monitoring/exit logic
  store.py                 SQLite event store
  journal.py               Decision/trade journal
  performance.py           Performance calculations
  portfolio_intelligence.py Portfolio analytics/intelligence
  backtest*.py             Backtesting primitives
  optimization.py          Parameter optimization
  research.py              Research runner

tests/                     Python unit tests

dashboard/                React + TypeScript + Vite UI
config/                   MCP configuration example
.github/workflows/test.yml CI checks
pyproject.toml            Python dependencies, pytest and Ruff configuration
.env.example              Environment-variable template
```

## Entry points

### HTTP API

`src/aegis/api.py` defines the FastAPI application as `app`.

Run with the verified command:

```bash
uvicorn aegis.api:app --reload
```

### One-cycle coordinator

`src/aegis/runner.py` contains `PaperRunCoordinator.run_once()`. It scans an underlying, evaluates an agent decision, journals the decision, rejects failed risk checks, prepares a spread through `TradePipeline`, and journals the prepared result. It does not itself submit an order.

### Dashboard

`dashboard/src/main.tsx` is the React entry point. Vite commands are defined in `dashboard/package.json`.

## Architecture rules

1. Keep **strategy reasoning separate from deterministic authorization**. `AegisAgent` proposes/evaluates; risk components decide whether a proposal is allowed.
2. Keep **order construction separate from broker submission**. `execution.py` creates an Alpaca-compatible MLeg payload; `paper_controller.py`/gateway components own submission boundaries.
3. Keep **MCP transport/tool discovery separate from business logic**. `mcp_client.py` handles protocol transport; `mcp_registry.py` indexes discovered tools; adapters translate Aegis operations.
4. Preserve paper-only defaults. `Settings.aegis_live_trading` defaults to `false`, and the configured base URL defaults to the Alpaca paper endpoint.
5. Prefer existing domain models, selectors, risk engines, stores, gateways, and intelligence classes over creating parallel abstractions.
6. Keep persistence behind `AegisStore`/journal abstractions rather than scattering SQLite access through application code.
7. API routes are read-oriented today. Do not add mutating endpoints without documenting authentication, authorization, safety, and tests.

## Before editing

1. Read this file and the relevant sections of [`ARCHITECTURE.md`](ARCHITECTURE.md).
2. Locate existing implementations of the requested behavior with repository search.
3. Check adjacent tests before designing a new abstraction.
4. Trace the change through strategy → risk → order → broker → persistence/API if applicable.
5. Check configuration and environment implications.
6. Identify database/API compatibility impact.
7. Prefer the smallest focused change.

## Implementation workflow

```text
Understand
   → Locate
   → Plan
   → Implement
   → Test
   → Review
   → Document
```

Do not modify application behavior merely to make documentation accurate.

## Development conventions

- Python target: 3.11+.
- Ruff target: Python 3.11; line length 100.
- Ruff rules configured: `E`, `F`, `I`, `UP`, `B`.
- Use type annotations for new public interfaces.
- Prefer dataclasses for immutable/value-style structures where the existing code uses them.
- Preserve existing Pydantic models for domain/config validation.
- Use parameterized SQL; never interpolate values into SQL statements.
- Raise explicit exceptions for invalid domain input; do not silently accept invalid orders or market data.
- Keep tests close to behavior changes in `tests/` using `test_*.py`.

## Configuration and secrets

Configuration is loaded through `src/aegis/config.py` using `pydantic-settings` and `.env`. Never hardcode API keys, secrets, tokens, MFA secrets, recovery codes, or credentials. Never commit a real `.env`.

`AEGIS_LIVE_TRADING=false` is the documented safety default. Do not change it as part of unrelated work.

## Testing expectations

Before submitting a Python change:

```bash
ruff check .
pytest -q
```

For focused work, run the relevant test module first, then the complete suite. CI uses Python 3.11 and runs both Ruff and pytest.

For broker/MCP changes, separate deterministic unit tests from credentialed/network integration tests. Never make a unit test depend on a real account.

## API/database rules

- Do not silently rename or remove existing API routes.
- Document new routes in [`API.md`](API.md).
- Do not alter the SQLite schema without documenting the change in [`DATABASE.md`](DATABASE.md) and [`DECISIONS.md`](DECISIONS.md) when it is an architectural decision.
- The current database is a local event store, not a relational trading domain model. Do not assume normalized order/position tables exist.

## Don't break

Do not casually change:

- The paper-trading default.
- Risk approval gates.
- MLeg validation limits.
- Existing contract-selection behavior.
- Existing event persistence semantics.
- MCP paper/live safety boundaries.
- Public API routes.
- Existing test contracts.

Do not remove existing functionality to make tests pass. Do not duplicate services/components when an existing abstraction can be extended.

## Unknowns and verification requirements

The repository does not by itself verify every runtime detail. Treat these as **Needs verification** rather than facts:

- Exact live Alpaca MCP tool names and input schemas in the user's environment.
- Real paper-account execution success.
- Availability/quality of a historical options dataset.
- Production deployment target and infrastructure.
- Authentication/authorization for the FastAPI API; current routes do not show an auth layer.

## Documentation maintenance

When architecture, APIs, configuration, database schema, commands, or important safety rules change, update the relevant documentation in the same change. Keep cross-references valid and remove claims that are no longer true.
