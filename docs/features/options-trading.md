# Options Trading Feature

## Purpose

The options stack represents trades as option candidates and multi-leg spreads, then applies deterministic risk controls before preparing a paper order.

## Feature map

```text
Options candidate
├── Domain: src/aegis/options.py
├── Contract model: src/aegis/option_contracts.py
├── Selection: src/aegis/contract_selector.py
├── Filters: src/aegis/selection_filters.py
├── Greeks: src/aegis/greeks.py
├── Options intelligence: src/aegis/options_intelligence.py
├── Risk: src/aegis/options_risk.py
├── Strategy: src/aegis/spread_strategy.py / strategies.py
├── Order construction: src/aegis/execution.py
└── Tests: tests/test_options*.py, test_contract_selector.py, test_execution.py
```

## Selection

`ContractSelector` chooses a spread from available candidates. `TradePipeline.prepare_spread()` performs selection only after the initial risk-approved decision exists.

The repository also contains `selection_filters.py` for liquidity/DTE/spread-style filtering and `options_backtest.py` for historical multi-leg pricing primitives.

## Risk

There are two relevant layers:

1. General `RiskEngine` evaluates the proposal against account equity, portfolio risk, daily loss, and open-position limits.
2. Options-specific risk helpers evaluate option/spread characteristics.

After the spread is selected, `TradePipeline` replaces the proposal's max-loss/max-profit hints with the actual selection values and evaluates risk again.

## Order representation

`execution.MultiLegOrder` contains:

- option strategy
- tuple of option legs
- quantity
- optional limit price

`PaperExecutionService.build_order()` validates 2–4 legs and creates an Alpaca-compatible `mleg` payload.

## Safety

The feature is intended to remain paper-only. Do not bypass `RiskEngine`, `TradePipeline`, `execution_gate.py`, or `PaperExecutionController` to submit an order directly.

## Verification gaps

The repository does not contain verified real historical-options results or a verified live connection to every external Alpaca/MCP operation. Those require environment-backed integration tests.
