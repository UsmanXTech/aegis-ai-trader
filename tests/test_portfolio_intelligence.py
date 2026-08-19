from aegis.portfolio_intelligence import PortfolioIntelligence
from aegis.position_sync import PositionRecord


def test_portfolio_aggregation() -> None:
    positions = [
        PositionRecord("SPY250919C00500000", 1, 2.0, 230.0, 30.0, 15.0, "long", "now"),
        PositionRecord("SPY250919P00490000", 1, 1.0, 80.0, -20.0, -20.0, "long", "now"),
    ]
    snapshot = PortfolioIntelligence().analyze(positions)
    assert snapshot.total_market_value == 310
    assert snapshot.unrealized_pnl == 10
    assert len(snapshot.positions) == 2
    assert snapshot.exits_required == 0
