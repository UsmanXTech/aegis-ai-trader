# Aegis AI Trader

Autonomous options-trading agent for Alpaca paper trading, built for the 2026 lablab.ai × Alpaca AI Trading Agents Hackathon.

> **Safety:** The repository is designed around Alpaca paper trading. `AEGIS_LIVE_TRADING` defaults to `false`. Never commit credentials or enable live trading casually.

## What it does

Aegis combines deterministic market analysis, options strategy selection, risk controls, order construction, paper execution boundaries, event journaling, and a small monitoring dashboard.

The main analysis path is:

```text
Market data
   ↓
Market scan / regime / signals
   ↓
Strategy selection
   ↓
Options contract selection
   ↓
Risk evaluation
   ↓
Prepared multi-leg order
   ↓
Paper execution boundary
   ↓
Position/order synchronization
   ↓
Event journal / P&L
   ↓
FastAPI + React dashboard
```

The current `PaperRunCoordinator` prepares and journals a paper order but does not itself submit it; broker submission is separated behind paper gateways/controllers. See [`src/aegis/runner.py`](src/aegis/runner.py) and [`src/aegis/paper_controller.py`](src/aegis/paper_controller.py).

## Technology stack

| Area | Technology |
|---|---|
| Backend | Python 3.11+ |
| Trading integration | `alpaca-py`, Alpaca paper API, MCP client/gateway components |
| API | FastAPI + Uvicorn |
| Data / numerical | pandas, NumPy |
| Validation/config | Pydantic, pydantic-settings |
| Persistence | SQLite |
| Dashboard | React + TypeScript + Vite |
| Tests | pytest, pytest-cov |
| Lint | Ruff |
| CI | GitHub Actions |

Dependencies and versions are declared in [`pyproject.toml`](pyproject.toml). The dashboard has an independent `package.json`.

## Repository structure

```text
.
├── .env.example                  Environment/configuration template
├── .github/workflows/test.yml    CI: Ruff + pytest
├── config/                       Alpaca MCP example configuration
├── dashboard/                    React/Vite monitoring UI
├── src/aegis/                    Python application package
├── tests/                        Unit tests
├── pyproject.toml                Python package/dependency configuration
└── README.md
```

Important backend areas:

```text
src/aegis/
├── api.py                        FastAPI application and read APIs
├── agent.py                      Strategy/risk coordination
├── runner.py                     One-cycle paper analysis coordinator
├── trade_pipeline.py             Decision → selection → validated order
├── scanner.py / live_scan.py     Market scanning
├── strategies.py / regime.py    Strategy and market-regime logic
├── options.py                    Option candidate domain helpers
├── contract_selector.py          Spread contract selection
├── selection_filters.py          Candidate filters
├── options_risk.py / risk.py     Options and portfolio risk controls
├── risk_pipeline.py              Risk pipeline
├── greeks.py                     Greeks calculations
├── execution.py                  Alpaca-compatible MLeg payload builder
├── execution_gate.py             Paper/risk execution boundary
├── paper_gateway.py              Paper broker boundary
├── paper_controller.py           Final paper-only execution controller
├── mcp_client.py                 MCP stdio/JSON-RPC client
├── mcp_registry.py               Dynamic MCP tool registry
├── mcp_gateway.py / mcp_tools.py MCP safety/tool adapters
├── market_data.py                Alpaca market-data integration
├── account_sync.py / position_sync.py Account/position synchronization
├── monitor.py                    Position monitoring/exit orchestration
├── store.py / journal.py         Local event persistence/journaling
├── performance.py                Performance calculations
├── portfolio_intelligence.py     Portfolio-level analytics/intelligence
├── backtest.py / options_backtest.py Historical backtesting primitives
├── optimization.py / research.py Research and walk-forward optimization
└── config.py                     Environment-backed settings
```

## Installation

Requirements:

- Python 3.11 or newer
- Node.js/npm for the dashboard
- Alpaca paper credentials only when testing broker integration

Python setup:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\\Scripts\\activate

pip install -e ".[dev]"
```

## Configuration

Copy the template:

```bash
cp .env.example .env
```

The verified environment variables are:

| Variable | Purpose | Default |
|---|---|---|
| `ALPACA_API_KEY` | Alpaca API key | empty |
| `ALPACA_SECRET_KEY` | Alpaca secret | empty |
| `ALPACA_BASE_URL` | Alpaca API base URL | `https://paper-api.alpaca.markets` |
| `LLM_PROVIDER` | Optional LLM provider name | empty |
| `LLM_API_KEY` | Optional LLM credential | empty |
| `LLM_MODEL` | Optional model name | empty |
| `AEGIS_LIVE_TRADING` | Live-trading switch | `false` |
| `AEGIS_MAX_POSITION_RISK_PCT` | Maximum position risk | `2.0` |
| `AEGIS_MAX_PORTFOLIO_RISK_PCT` | Maximum portfolio risk | `10.0` |
| `AEGIS_MAX_DAILY_LOSS_PCT` | Maximum daily loss | `3.0` |
| `AEGIS_MAX_OPEN_POSITIONS` | Maximum open positions | `5` |

Never commit `.env`, API keys, MFA secrets, recovery codes, or tokens.

## Running locally

Start the FastAPI application with Uvicorn:

```bash
uvicorn aegis.api:app --reload
```

The dashboard is independent:

```bash
cd dashboard
npm install
npm run dev
```

The dashboard reads `VITE_API_URL`, defaulting to `http://localhost:8000`.

## API

The backend exposes a health endpoint and read-only event views. See [`API.md`](API.md).

## Testing

Run the complete Python test suite:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

CI additionally runs:

```bash
ruff check .
pytest -q
```

See [`DEVELOPMENT.md`](DEVELOPMENT.md).

## Dashboard build

```bash
cd dashboard
npm install
npm run build
npm run preview
```

There is no verified production deployment configuration in the repository; deployment details are therefore marked as unknown in [`DEVELOPMENT.md`](DEVELOPMENT.md).

## Architecture and agent documentation

- [`AGENTS.md`](AGENTS.md) — rules and workflow for future AI coding agents
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — actual component/data-flow architecture
- [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) — current state, constraints, and risks
- [`DEVELOPMENT.md`](DEVELOPMENT.md) — verified setup/test/debug workflow
- [`API.md`](API.md) — discovered HTTP endpoints
- [`DATABASE.md`](DATABASE.md) — SQLite event-store schema
- [`DECISIONS.md`](DECISIONS.md) — documented/inferred architectural decisions
- [`docs/`](docs/) — focused implementation and architecture notes

## Current limitations

The repository contains substantial research, options, risk, MCP, and paper-execution scaffolding, but a complete verified production/hackathon execution path cannot be inferred solely from source. In particular, real Alpaca MCP tool names/schema, real historical options datasets, end-to-end paper execution, and production deployment configuration require environment/runtime verification.
