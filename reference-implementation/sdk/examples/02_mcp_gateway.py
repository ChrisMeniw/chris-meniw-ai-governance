"""
MCP gateway: gate every tool call an MCP server exposes.

This simulates an MCP server's call_tool handler. Drop `guard_mcp_call` into your real handler
and every tool call passes the Meniw gate before it runs.

    python 02_mcp_gateway.py
"""
from meniw_protocol import MeniwGate, ProhibitedActionError
from meniw_protocol.adapters import guard_mcp_call

gate = MeniwGate.from_default(ledger_path="mcp.ledger.jsonl")


# --- your real MCP tools (executors) ---------------------------------------
def real_call_tool(name, arguments):
    return {"tool": name, "result": "ok", "args": arguments}


# --- map a tool call to risk categories (your detector) --------------------
LETHAL_TOOLS = {"actuator_fire", "drone_strike"}

def classify(tool_name, args):
    return ["lethal"] if tool_name in LETHAL_TOOLS else []


def call_tool(name, arguments):
    """The handler you expose to MCP — now Meniw-gated."""
    return guard_mcp_call(gate, name, arguments, call_fn=real_call_tool, classify=classify)


if __name__ == "__main__":
    print("search_docs:", call_tool("search_docs", {"q": "meniw protocol"}))   # allowed

    try:
        call_tool("actuator_fire", {"target": "x"})
    except ProhibitedActionError as e:
        print("actuator_fire blocked by", e.verdict.rule_id)                    # AP-1

    print("ledger verifies:", gate.ledger.verify())
