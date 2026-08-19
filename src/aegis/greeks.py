from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Greeks:
    delta: float = 0.0
    gamma: float = 0.0
    theta: float = 0.0
    vega: float = 0.0
    implied_volatility: float = 0.0


@dataclass(frozen=True)
class GreeksRisk:
    delta_exposure: float
    gamma_exposure: float
    theta_exposure: float
    vega_exposure: float


def scale_greeks(greeks: Greeks, quantity: float, contract_multiplier: int = 100) -> GreeksRisk:
    scale = quantity * contract_multiplier
    return GreeksRisk(
        delta_exposure=greeks.delta * scale,
        gamma_exposure=greeks.gamma * scale,
        theta_exposure=greeks.theta * scale,
        vega_exposure=greeks.vega * scale,
    )
