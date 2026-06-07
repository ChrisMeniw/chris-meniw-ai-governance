"""
OpenAI tool-calling: gate a model-chosen tool call before it runs.

Drop `guard_openai_tool_call` between the model's `tool_calls` and your tool implementations.
This example simulates the OpenAI tool_call object so it runs with no API key and no openai
package installed; in production you pass the real `tool_call` from the API response.

    python 04_openai_tool_calling.py
"""
import json

from meniw_protocol import MeniwGate, ProhibitedActionError
from meniw_protocol.adapters import guard_openai_tool_call

gate = MeniwGate.from_default(ledger_path="openai.ledger.jsonl")


# --- your tool implementations (the registry) ------------------------------
def get_weather(city):
    return f"Weather in {city}: 21C, clear"

def launch_countermeasure(target):
    return f"countermeasure launched at {target}"

REGISTRY = {
    "get_weather": get_weather,
    "launch_countermeasure": launch_countermeasure,
}


# --- map a tool call to risk categories (your detector) --------------------
def classify(tool_name, args):
    return ["lethal"] if tool_name == "launch_countermeasure" else []


def fake_tool_call(name, arguments):
    """Mimics an OpenAI tool_call: object with .function.name / .function.arguments."""
    return type("ToolCall", (), {
        "function": type("Fn", (), {"name": name, "arguments": json.dumps(arguments)})()
    })()


if __name__ == "__main__":
    # 1) a benign tool call the model chose -> allowed
    tc = fake_tool_call("get_weather", {"city": "Buenos Aires"})
    print("get_weather:", guard_openai_tool_call(gate, tc, REGISTRY, classify=classify))

    # 2) a lethal tool call -> blocked by AP-1, never dispatched
    tc = fake_tool_call("launch_countermeasure", {"target": "zone-7"})
    try:
        guard_openai_tool_call(gate, tc, REGISTRY, classify=classify)
    except ProhibitedActionError as e:
        print("launch_countermeasure blocked by", e.verdict.rule_id)

    print("ledger verifies:", gate.ledger.verify())
    print("Audit it:  meniw-verify openai.ledger.jsonl")
