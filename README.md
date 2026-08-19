# Aegis AI Trader

Autonomous options trading agent for the 2026 lablab.ai × Alpaca AI Trading Agents Hackathon.

## Goal

Aegis combines market regime detection, technical signals, options-aware strategy selection, deterministic risk controls, and Alpaca paper-trading execution.

## Architecture

```text
Market Data → Regime → Signals → Options Strategy → Risk Engine → Execution → Monitoring
                                      ↑                  |
                                      └── AI reasoning ──┘
```

The LLM proposes and explains trades; deterministic risk rules authorize or reject them.

## Initial implementation

- Python backend
- Typed domain models
- Deterministic risk engine
- Strategy selection scaffold
- Alpaca adapter boundary
- Unit tests
- Safe paper-trading defaults

## Safety

This project is designed for Alpaca paper trading during the hackathon. Live trading is intentionally not enabled by default.

Never commit Alpaca API keys or secrets. Copy `.env.example` to `.env` locally.

## Development

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

pip install -e ".[dev]"
pytest
```
