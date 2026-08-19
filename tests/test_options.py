from datetime import date

from aegis.options import OptionCandidate, score_candidate


def test_mid_price() -> None:
    option = OptionCandidate("SPY", 600, date(2026, 9, 18), "call", 2.0, 2.4, 500)
    assert option.mid == 2.2


def test_tight_liquid_contract_scores_higher() -> None:
    good = OptionCandidate("SPY", 600, date(2026, 9, 18), "call", 2.0, 2.1, 1000, 0.50)
    poor = OptionCandidate("SPY", 600, date(2026, 9, 18), "call", 1.0, 1.5, 10, 0.20)
    assert score_candidate(good) > score_candidate(poor)
