"""LangChain adapter.

Wrap any LangChain tool (or plain callable) so its invocation must pass the Meniw gate.
Works with a real `langchain_core.tools.BaseTool` or any object with a `.name` and a
`.run`/`__call__`. No hard dependency on LangChain.

    from meniw_protocol import MeniwGate
    from meniw_protocol.adapters import governed_tool

    safe_tool = governed_tool(gate, my_tool, classify=my_classifier)
"""

from __future__ import annotations

from typing import Any, Callable

from ..core import Action, MeniwGate, ProhibitedActionError


def governed_tool(gate: MeniwGate,
                  tool: Any,
                  classify: Callable[[str, dict], list[str]] | None = None,
                  irreversible: bool = False,
                  context: dict | None = None) -> Callable[..., Any]:
    """Return a callable that runs `tool` only if the Meniw gate allows it."""
    name = getattr(tool, "name", getattr(tool, "__name__", "tool"))
    run = getattr(tool, "run", None) or getattr(tool, "invoke", None) or tool

    def governed(*args, **kwargs):
        cats = classify(name, kwargs) if classify else []
        action = Action(name=name, categories=list(cats or []), irreversible=irreversible, details=kwargs)
        out = gate.governed_execute(action, dict(context or {}), lambda a: run(*args, **kwargs))
        if not out["executed"]:
            raise ProhibitedActionError(out["verdict"], out["receipt"])
        return out["result"]

    governed.__name__ = f"governed_{name}"
    return governed
