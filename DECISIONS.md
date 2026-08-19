# Architecture Decision Records

## ADR-001: Keep deterministic risk separate from strategy reasoning

### Status
Accepted — inferred from implementation.

### Context
`AegisAgent` creates a trade proposal from a selected strategy and then passes that proposal to `RiskEngine`. `TradePipeline` performs another risk evaluation after selecting the actual spread.

### Decision
Keep risk authorization in deterministic risk components rather than allowing strategy/LLM reasoning to authorize execution directly.

### Reason
The code structure clearly treats risk approval as a separate gate and allows actual selected-spread loss/profit to be checked before an order is prepared.

### Alternatives
- Let strategy code submit directly.
- Use the LLM as the final execution authority.

### Consequences
**Positive:** Clear safety boundary, easier unit testing, deterministic rejection behavior.

**Negative:** A proposal may need to be evaluated more than once as concrete order characteristics become known.

---

## ADR-002: Default to Alpaca paper trading

### Status
Accepted — explicit in configuration.

### Context
The project targets a paper-trading hackathon environment and `Settings` defaults `aegis_live_trading` to `false`; `.env.example` uses the Alpaca paper API URL.

### Decision
Default configuration is paper trading. Live trading is not enabled by default.

### Reason
It is appropriate for development/testing and is explicitly encoded in configuration and safety-oriented execution components.

### Alternatives
- Default to live trading.
- Require a separate broker implementation for every environment.

### Consequences
**Positive:** Safer local development and easier integration testing.

**Negative:** Paper behavior is not proof of live broker behavior.

---

## ADR-003: Use a local SQLite event store

### Status
Accepted — explicit in implementation.

### Context
`AegisStore` initializes a single `events` table and stores heterogeneous payloads as JSON.

### Decision
Use SQLite as a local operational journal/read model rather than a normalized trading database.

### Reason
The implementation is intentionally small and supports recent event queries used by the API/dashboard.

### Alternatives
- PostgreSQL with normalized account/order/position tables.
- Flat files.
- External event store.

### Consequences
**Positive:** No external database service is required; simple persistence and querying.

**Negative:** No database-enforced domain relationships; payload compatibility must be managed by the application.

---

## ADR-004: Separate order construction from broker submission

### Status
Accepted — inferred from implementation.

### Context
`execution.py` builds Alpaca-compatible MLeg payloads, while `paper_controller.py` submits through a `PaperGateway` protocol.

### Decision
Keep payload construction and broker submission behind separate abstractions.

### Reason
This allows deterministic order validation to be unit-tested without a broker connection and keeps paper execution behind an explicit gateway.

### Alternatives
- Call the broker directly from strategy/pipeline code.
- Put serialization and HTTP/MCP transport into one service.

### Consequences
**Positive:** Better testability and clearer safety boundary.

**Negative:** More interfaces and adapter code.

---

## ADR-005: Discover MCP tools instead of assuming vendor tool names

### Status
Accepted — inferred from current MCP client/registry design.

### Context
The repository contains an MCP client that performs initialization/tool discovery and a registry that indexes returned tools and schemas.

### Decision
Treat MCP tool discovery and schemas as runtime capabilities rather than hard-coding every external tool name into core business logic.

### Reason
External MCP tool names/input schemas are provider/runtime concerns and may change independently of Aegis.

### Alternatives
- Hard-code all tool names and schemas.
- Call the broker API directly everywhere.

### Consequences
**Positive:** More adaptable integration and clearer separation of protocol/vendor concerns.

**Negative:** Integration tests must verify the actual external tool registry.

---

## ADR-006: Use a vendor-neutral historical options schema

### Status
Accepted — explicit in implementation.

### Context
`HistoricalOptionRecord`, `OptionsDataAdapter`, and `HistoricalOptionsLoader` separate source rows from backtesting logic.

### Decision
Normalize historical option data into an Aegis-owned schema before research/backtesting.

### Reason
The backtester should not depend on one provider's raw field names or file format.

### Alternatives
- Couple the backtester to one provider.
- Pass raw dictionaries throughout the research stack.

### Consequences
**Positive:** Easier provider substitution and deterministic validation.

**Negative:** Each provider requires an adapter/normalization step.
