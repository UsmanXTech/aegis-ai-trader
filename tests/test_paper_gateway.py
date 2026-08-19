import pytest

from aegis.paper_gateway import AlpacaPaperGateway


def test_missing_credentials_are_rejected() -> None:
    with pytest.raises(ValueError):
        AlpacaPaperGateway("", "")
