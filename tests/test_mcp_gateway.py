import pytest

from aegis.mcp_gateway import AlpacaMCPGateway


class FakeMCP:
    def call_tool(self, name, arguments):
        return {"tool": name, "arguments": arguments}


def test_reads_account_positions_orders() -> None:
    gateway = AlpacaMCPGateway(FakeMCP())
    assert gateway.account()["tool"] == "get_account"
    assert gateway.positions()["tool"] == "get_all_positions"
    assert gateway.orders(10)["arguments"] == {"limit": 10}


def test_rejects_unapproved_order() -> None:
    gateway = AlpacaMCPGateway(FakeMCP())
    with pytest.raises(PermissionError):
        gateway.submit_approved_order({"paper": True}, risk_approved=False)


def test_rejects_non_paper_order() -> None:
    gateway = AlpacaMCPGateway(FakeMCP())
    with pytest.raises(PermissionError):
        gateway.submit_approved_order({"paper": False}, risk_approved=True)
