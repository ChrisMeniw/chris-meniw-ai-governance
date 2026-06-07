"""MCP (Model Context Protocol) gateway adapter.

MCP is where, in 2026, agent tool-calls flow through a server. This wraps the
`tools/call` step so a prohibited call is blocked before the server executes it — turning an
MCP server into a Meniw-conformant choke point for every tool it exposes.

    from meniw_protocol import MeniwGate
    from meniw_protocol.adapters import guard_mcp_call

    # inside your MCP server's call_tool handler:
    result = guard_mcp_call(gate, name, arguments, call_fn=real_call_tool,
                            classify=my_classifier)
"""

from __future__ import annotations

from typing import Any, Callable

from ..core import Action, MeniwGate, ProhibitedActionError


def guard_mcp_call(gate: MeniwGate,
                   tool_name: str,
                   arguments: dict,
                   call_fn: Callable[[str, dict], Any],
                   classify: Callable[[str, dict], list[str]] | None = None,
                   irreversible: Callable[[str, dict], bool] | None = None,
                   context: dict | None = None) -> Any:
    """Gate an MCP tool call. Raises ProhibitedActionError if the Protocol blocks it."""
    cats = classify(tool_name, arguments) if classify else []
    irr = irreversible(tool_name, arguments) if irreversible else False
    action = Action(name=tool_name, categories=list(cats or []), irreversible=irr, details=dict(arguments))
    out = gate.governed_execute(action, dict(context or {}), lambda a: call_fn(tool_name, arguments))
    if not out["executed"]:
        raise ProhibitedActionError(out["verdict"], out["receipt"])
    return out["result"]
