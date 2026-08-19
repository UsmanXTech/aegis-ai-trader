# Architecture

## Scope

This document describes the architecture discoverable from the current repository. It does not assume runtime behavior that is not represented in source/tests.

## High-level architecture

```text
                 ┌────────────────────┐
                 │ Alpaca market data │
                 └─────────┬──────────┘
                           ↓
                 Market scanner / regime
                           ↓
                    Strategy selector
                           ↓
                  Option candidates
                           ↓
                  Contract selection
                           ↓
                 Deterministic risk
                           ↓
                    Prepared trade
                           ↓
                 MLeg order builder
                           ↓
                 Paper execution gate
                           ↓
               Paper gateway/controller
                           ↓
                  Alpaca integration
                           ↓
              Account / position sync
                           ↓
                  Monitor / exits
                           ↓
                  Journal + SQLite
                           ↓
                    FastAPI / dashboard
```

The LLM-facing concept is represented by the `AegisAgent` boundary, but the repository does not prove a concrete external LLM client implementation. Configuration supports optional LLM provider/model fields.

## Major components

| Component | Responsibility | Main files |
|---|---|---|
| Configuration | Environment-backed settings and safety limits | `src/aegis/config.py`, `.env.example` |
| Domain | Typed market/trade models | `src/aegis/domain.py`, `options.py`, `option_contracts.py` |
| Scanning | Market snapshot/regime/signal preparation | `scanner.py`, `live_scan.py`, `regime.py`, `quote_intelligence.py` |
| Agent | Strategy selection and risk evaluation coordination | `agent.py`, `strategies.py` |
| Contract selection | Select option legs/spreads from candidates | `contract_selector.py`, `selection_filters.py` |
| Options intelligence | Greeks, option analysis, risk | `greeks.py`, `options_intelligence.py`, `options_risk.py` |
| Risk | Portfolio/trade risk gates | `risk.py`, `risk_pipeline.py` |
| Execution | MLeg construction and safety gates | `execution.py`, `execution_gate.py`, `order_builder.py`, `order_policy.py` |
| Paper execution | Broker boundary and controller | `paper_gateway.py`, `paper_controller.py`, `paper_loop.py` |
| Alpaca | Market/account/position integration | `alpaca_adapter.py`, `market_data.py`, `account_sync.py`, `position_sync.py` |
| MCP | Protocol transport, discovery, adapters | `mcp_client.py`, `mcp_registry.py`, `mcp_gateway.py`, `mcp_tools.py` |
| Monitoring | Position/exit monitoring | `monitor.py`, `position_manager.py`, `position_intelligence.py` |
| Persistence | Event journal and local database | `journal.py`, `store.py` |
| Research | Backtests, optimization, research runner | `backtest.py`, `options_backtest.py`, `optimization.py`, `research.py` |
| API | HTTP read APIs | `api.py` |
| UI | React monitoring dashboard | `dashboard/src/main.tsx`, `dashboard/src/styles.css` |

## Core execution flow

`PaperRunCoordinator.run_once()` is the clearest one-cycle orchestration point:

1. Scan an `UnderlyingSnapshot`.
2. Pass the resulting market snapshot to `AegisAgent`.
3. `AegisAgent` selects a strategy and calls `RiskEngine`.
4. The decision is journaled.
5. Rejected decisions are returned and journaled.
6. Approved decisions enter `TradePipeline.prepare_spread()`.
7. The pipeline selects a spread, refreshes risk using actual selected-spread loss/profit, converts the selection to a multi-leg order, and builds an Alpaca-compatible payload.
8. The prepared result is journaled.

The coordinator intentionally stops at preparation. `PaperExecutionController` is the explicit paper-only submission boundary.

## Strategy and risk separation

The design separates proposal generation from authorization:

```text
MarketSnapshot
     ↓
StrategySelector
     ↓
TradeProposal
     ↓
RiskEngine
     ↓
TradeDecision
```

The risk result is part of the decision. `TradePipeline` performs a second risk evaluation after contract selection because actual spread max-loss/max-profit can differ from the initial hints.

## Options selection

`ContractSelector` operates on option candidates and produces a `SpreadSelection`. `TradePipeline` then converts the selection to the execution order. `selection_filters.py` provides additional candidate filtering primitives.

The repository contains both `spread_strategy.py` and `options_backtest.py`; these are research/strategy layers and should not be assumed to be the production paper-execution path without tracing the caller.

## Execution architecture

`execution.py` creates an Alpaca-compatible MLeg payload. It validates quantity and requires between two and four legs. `PaperExecutionController` requires explicit risk approval before submission and uses a `PaperGateway` protocol.

The MCP stack is separate:

```text
Aegis operation
     ↓
mcp_gateway / mcp_tools
     ↓
mcp_client
     ↓
MCP server process
```

`mcp_client.py` provides stdio/JSON-RPC transport and initialization/tool discovery. `mcp_registry.py` indexes discovered tools rather than assuming every provider-specific tool name. Exact runtime Alpaca MCP tool names/schemas are **Needs verification**.

## Persistence architecture

`AegisStore` is a local SQLite event store. It creates one `events` table and an index on `(event_type, created_at)`. Events are serialized as JSON payloads. API endpoints read recent events by event type.

There are no verified normalized `orders`, `positions`, `trades`, or `accounts` tables in the current repository.

## API and dashboard flow

```text
React dashboard
      ↓ fetch
FastAPI
      ↓
AegisStore
      ↓
SQLite events
```

The dashboard polls every 10 seconds and displays health, account data, and the latest event journal. Its API base defaults to `http://localhost:8000` and can be overridden with `VITE_API_URL`.

## Deployment architecture

**Unknown / Needs verification.** The repository has GitHub Actions CI but no verified Dockerfile, deployment manifest, cloud configuration, or production hosting configuration in the current tree.

## Security boundaries

- `.env.example` defaults to the Alpaca paper API endpoint.
- `AEGIS_LIVE_TRADING` defaults to `false`.
- Paper execution is represented by dedicated gateway/controller abstractions.
- Secrets are expected to come from environment configuration.
- The FastAPI routes shown in `api.py` do not implement authentication/authorization; whether an external network boundary protects them is **Unknown**.
