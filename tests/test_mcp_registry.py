from aegis.mcp_registry import McpToolRegistry


def test_indexes_tools() -> None:
    registry = McpToolRegistry({
        "tools": [
            {"name": "get_account", "description": "Read trading account", "inputSchema": {"type": "object"}},
            {"name": "submit_order", "description": "Submit a paper order", "inputSchema": {"type": "object"}},
        ]
    })
    assert registry.get("get_account").name == "get_account"
    assert registry.find("account") [0].name == "get_account"


def test_missing_tool_is_explicit() -> None:
    registry = McpToolRegistry({"tools": []})
    try:
        registry.get("missing")
    except KeyError as exc:
        assert "MCP tool not available" in str(exc)
        return
    raise AssertionError("missing MCP tool should fail")
