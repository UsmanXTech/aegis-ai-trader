# Testing Strategy

## Test suite

Python tests live in `tests/` and are discovered by pytest because `pyproject.toml` sets `testpaths = ["tests"]` and adds `src` to `pythonpath`.

The suite covers application components including:

- agent decisions
- API health/events
- backtesting
- chain normalization
- contract selection
- data adapters/loaders
- execution and execution gates
- Greeks
- market data
- MCP client/gateway/registry/tools
- monitoring
- optimization/research
- option contracts/options intelligence/options risk
- order policy/builder
- paper controller/gateway/loop
- performance and portfolio intelligence
- position intelligence/synchronization
- risk and risk pipeline
- runner
- selection filters
- spread strategy
- SQLite store
- strategy optimizer
- trade pipeline

## Verification layers

### Layer 1 — deterministic unit tests

Use mocks/fakes for broker and MCP interfaces. These tests should not require credentials or network access.

```bash
pytest -q
```

### Layer 2 — lint

```bash
ruff check .
```

### Layer 3 — dashboard build

For frontend changes:

```bash
cd dashboard
npm install
npm run build
```

### Layer 4 — paper integration tests

**Needs verification.** The repository has broker/MCP boundaries and test doubles, but the tree does not prove a complete credentialed integration-test command. When adding one, keep it separate from the default unit suite and require explicit paper-account configuration.

## Safety test priorities

Any change touching execution should test:

1. Rejected risk decision cannot submit.
2. Invalid leg count cannot submit.
3. Invalid quantity cannot submit.
4. Live trading cannot be enabled accidentally by a default.
5. MCP/tool errors propagate clearly.
6. Order/position synchronization handles broker responses deterministically.

## Research tests

Backtesting/optimization tests should remain deterministic. A real historical-data experiment should be treated separately from the unit suite and record the dataset/version, date range, assumptions, transaction costs, and out-of-sample split.

## CI

GitHub Actions currently runs:

```bash
pip install -e ".[dev]"
ruff check .
pytest -q
```

on Python 3.11 for pushes and pull requests.
