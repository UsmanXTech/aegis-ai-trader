# Project Context

## Project goal

Aegis AI Trader is intended to be an autonomous options-trading agent operating against Alpaca's paper-trading environment. The repository was created for the 2026 lablab.ai × Alpaca AI Trading Agents Hackathon.

## Current verified state

Implemented source areas include:

- Python package and typed domain models.
- Market scanning and strategy-selection scaffolding.
- Deterministic trade/portfolio risk controls.
- Greeks and options-risk helpers.
- Option contract/spread selection.
- Historical backtesting primitives and a vendor-neutral historical-data schema/loader.
- Parameter grid optimization and a research runner.
- Alpaca market-data/account/position adapter boundaries.
- MCP stdio/JSON-RPC client, initialization, tool discovery, registry, gateway, and tool adapter components.
- MLeg order construction and paper-execution controller/gateway abstractions.
- Local SQLite event journal.
- FastAPI read APIs.
- React/Vite dashboard.
- Broad unit-test coverage across the Python modules.
- GitHub Actions CI running Ruff and pytest.

## Important design choices

### Deterministic risk authorization — inferred from code

`AegisAgent` creates a proposal and delegates authorization to `RiskEngine`. `TradePipeline` rechecks risk after actual contract selection. This strongly indicates that AI/strategy reasoning is intended to be subordinate to deterministic risk controls.

### Paper-first execution — explicit

Configuration defaults to the Alpaca paper endpoint and `AEGIS_LIVE_TRADING=false`. Dedicated paper gateway/controller components reinforce the boundary.

### Event-sourced local journal — explicit

`AegisStore` deliberately stores heterogeneous events as JSON payloads in one SQLite `events` table instead of modeling every trading object as a separate relational table.

### Vendor-neutral research data — explicit

`HistoricalOptionRecord`, `OptionsDataAdapter`, and `HistoricalOptionsLoader` separate provider-specific input from the backtesting domain.

## Current features

### Trading path

- Market snapshot scanning.
- Regime/signal-based strategy selection.
- Option candidate and spread selection.
- Greeks/risk evaluation.
- MLeg order payload generation.
- Paper execution boundary.
- Account/position synchronization components.
- Position monitoring and exit-related logic.
- Decision/event journaling.

### Research path

- Generic bar backtesting.
- Multi-leg options pricing primitives.
- Historical option schema.
- CSV/Parquet loading.
- Parameter grid optimization.
- Out-of-sample evaluation primitives.

### Observability

- SQLite event store.
- FastAPI health/events/account/decision/order/position/P&L endpoints.
- React dashboard showing health, account summary, and recent events.

## Incomplete / needs verification

These are not claimed as implemented end-to-end merely because supporting modules exist:

- A complete historical-options dataset and validated historical performance results: **Needs verification**.
- A complete options strategy backtest connected to real historical data: **Needs verification**.
- Real optimizer results: **Not present in repository**.
- Exact Alpaca MCP tool names/input schemas in the user's configured server: **Needs verification**.
- Successful end-to-end paper order submission using the current MCP path: **Needs verification**.
- Production deployment: **Unknown**.
- API authentication/authorization: **No implementation visible in `api.py`; external protection is Unknown**.
- A concrete LLM provider integration: **Not verified from the current source tree**.

## Constraints

- Python requires 3.11+.
- Python dependencies are version-bounded in `pyproject.toml`.
- Ruff line length is 100.
- The current SQLite store is a local event log.
- Dashboard and backend are separate packages/processes.
- The project must remain paper-only during normal development/testing unless a deliberate, documented safety decision changes that policy.

## High-risk areas

1. **Broker execution:** any change can affect financial behavior even in paper mode and must be tested with mocks before network tests.
2. **Risk gates:** changes can invalidate the safety model.
3. **Options leg semantics:** symbols, sides, ratios, position intent, and max-loss calculations must remain consistent.
4. **MCP schemas:** external tool names and payloads can change; discovery should be preferred over hard-coded assumptions.
5. **SQLite event compatibility:** dashboard/API consumers expect JSON payloads and known event types.
6. **Configuration:** accidentally enabling live trading or leaking secrets is unacceptable.
7. **Dashboard assumptions:** `dashboard/src/main.tsx` parses account event payloads into a specific shape; event schema changes may break the UI.
