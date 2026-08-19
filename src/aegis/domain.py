from enum import StrEnum

from pydantic import BaseModel, Field


class MarketRegime(StrEnum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class OptionStrategy(StrEnum):
    BULL_CALL_SPREAD = "bull_call_spread"
    BEAR_PUT_SPREAD = "bear_put_spread"
    LONG_STRADDLE = "long_straddle"
    PROTECTIVE_PUT = "protective_put"
    NO_TRADE = "no_trade"


class TradeProposal(BaseModel):
    symbol: str
    strategy: OptionStrategy
    regime: MarketRegime
    confidence: float = Field(ge=0.0, le=1.0)
    max_loss: float = Field(ge=0.0)
    max_profit: float = Field(ge=0.0)
    thesis: str = ""

    @property
    def risk_reward(self) -> float:
        if self.max_loss == 0:
            return 0.0
        return self.max_profit / self.max_loss


class RiskDecision(BaseModel):
    approved: bool
    reasons: list[str] = Field(default_factory=list)


class TradeDecision(BaseModel):
    proposal: TradeProposal
    risk: RiskDecision
