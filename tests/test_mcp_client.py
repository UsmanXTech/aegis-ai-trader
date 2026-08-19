from aegis.mcp_client import AlpacaMcpClient


def test_client_has_default_alpaca_server_command() -> None:
    client = AlpacaMcpClient()
    assert client.command == ("uvx", "alpaca-mcp-server", "serve")


def test_client_accepts_custom_launcher() -> None:
    client = AlpacaMcpClient(("python", "fake_server.py"))
    assert client.command == ("python", "fake_server.py")
