# Runtime Data Flow

## Analysis/preparation path

```text
UnderlyingSnapshot + OptionCandidate[]
              ↓
     PaperRunCoordinator
              ↓
        MarketScanner
              ↓
         AegisAgent
        ↙          ↘
 StrategySelector   RiskEngine
        ↘          ↙
         TradeDecision
              ↓
       TradePipeline
        ↓           ↓
ContractSelector  RiskEngine (recheck)
        ↓
    SpreadSelection
        ↓
  PaperExecutionService
        ↓
 PreparedTrade / payload
```

`PaperRunCoordinator` journals the decision and prepared/rejected result. It does not directly submit the payload.

## Paper submission boundary

```text
Prepared MultiLegOrder + payload
              ↓
     PaperExecutionController
              ↓
       PaperGateway protocol
              ↓
      Alpaca/paper adapter
```

The controller requires an approved trade and validates basic MLeg structure before calling the gateway.

## MCP path

```text
Aegis MCP operation
       ↓
 mcp_gateway / mcp_tools
       ↓
    mcp_client
       ↓
 stdio JSON-RPC process
       ↓
 external MCP server
```

The MCP client supports initialization and tool discovery. `McpToolRegistry` indexes discovered names/descriptions/input schemas.

Exact runtime tool mappings are **Needs verification**.

## Persistence/read path

```text
Decision / account / order / position / P&L event
                      ↓
                TradeJournal
                      ↓
                  AegisStore
                      ↓
                SQLite events
                  ↙         ↘
          FastAPI routes    direct store readers
                ↓
          React dashboard
```

## Dashboard polling

`dashboard/src/main.tsx` calls `/health`, `/api/v1/events?limit=20`, and `/api/v1/account?limit=1` on initial render and every 10 seconds. It expects the account event payload to contain `equity`, `daily_pnl`, `buying_power`, and `open_positions`.
