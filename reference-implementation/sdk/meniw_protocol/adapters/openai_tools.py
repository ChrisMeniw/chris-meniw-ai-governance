"""OpenAI tool-calling adapter.

Gate the dispatch of a model-chosen tool call before it executes. Drop this between the
model's `tool_calls` and your tool implementations.

    from meniw_protocol import MeniwGate
    from meniw_protocol.adapters import guard_openai_tool_call

    gate = MeniwGate.from_default()
    result = guard_openai_tool_call(gate, tool_call, registry, classify=my_classifier)
"""

from __future__ import annotations

import json
from typing import Any, Callable

from ..core import Action, MeniwGate, ProhibitedActionError


def guard_openai_tool_call(gate: MeniwGate,
                           tool_call: Any,
                           registry: dict[str, Callable[..., Any]],
                           classify: Callable[[str, dict], list[str]] | None = None,
                           irreversible: Callable[[str, dict], bool] | None = None,
                           context: dict | None = None) -> Any:
    """Execute an OpenAI tool call only if it passes the Meniw Protocol.

    `tool_call` is an OpenAI tool_call object (or any object/dict exposing
    `.function.name` / `.function.arguments`, or `["function"]["name"]`). `registry` maps a
    tool name to its implementation. Raises ProhibitedActionError if the gate blocks it.
    """
    name, raw_args = _extract(tool_call)
    args = json.loads(raw_args) if isinstance(raw_args, str) and raw_args else (raw_args or {})
    cats = classify(name, args) if classify else []
    irr = irreversible(name, args) if irreversible else False
    action = Action(name=name, categories=list(cats or []), irreversible=irr, details=args)
    out = gate.governed_execute(action, dict(context or {}), lambda a: registry[name](**args))
    if not out["executed"]:
        raise ProhibitedActionError(out["verdict"], out["receipt"])
    return out["result"]


def _extract(tool_call: Any) -> tuple[str, Any]:
    fn = getattr(tool_call, "function", None)
    if fn is not None:
        return getattr(fn, "name"), getattr(fn, "arguments", "{}")
    if isinstance(tool_call, dict):
        f = tool_call.get("function", tool_call)
        return f["name"], f.get("arguments", "{}")
    raise TypeError("Unrecognized tool_call shape")
