"""
Enforcement by construction.

This is the difference between an intention and an order. A declaration an agent *may*
consult is an intention. Here, the gate is wired INTO the call path: a prohibited action
does not "get discouraged" — it raises ProhibitedActionError and never executes. Passing the
norm is a structural precondition of running the action, evaluated at the exact point of
decision, before any side effect.
"""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from .core import Action, MeniwGate, ProhibitedActionError


class Enforcer:
    """Bind tools to the gate so they cannot execute unless they pass the Protocol.

        gate  = MeniwGate.from_default(hmac_key=b"...")
        agent = Enforcer(gate)

        @agent.tool(categories=lambda **kw: detect(kw), irreversible=False)
        def send_email(to, body): ...

        send_email("x@y.com", "hi")          # runs only if the gate allows it
                                             # otherwise raises ProhibitedActionError
    """

    def __init__(self, gate: MeniwGate):
        self.gate = gate

    def tool(self,
             categories: Callable[..., list[str]] | list[str] | None = None,
             irreversible: bool = False):
        """Decorator. `categories` is either a static list or a callable(**kwargs)->list[str].

        Pass governance context to a call via the reserved kwarg `_gov` (e.g. co-signers):
            wipe_db(_gov={"cosigners": ["alice", "bob"]})
        """
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(fn)
            def wrapper(*args, **kwargs):
                context: dict[str, Any] = dict(kwargs.pop("_gov", {}) or {})
                if irreversible:
                    context.setdefault("irreversible", True)
                if callable(categories):
                    cats = list(categories(**kwargs) or [])
                elif categories:
                    cats = list(categories)
                else:
                    cats = []
                action = Action(name=fn.__name__, categories=cats,
                                irreversible=irreversible, details=dict(kwargs))
                out = self.gate.governed_execute(action, context, lambda a: fn(*args, **kwargs))
                if not out["executed"]:
                    # ORDER, not intention: the action is structurally blocked.
                    raise ProhibitedActionError(out["verdict"], out["receipt"])
                return out["result"]

            wrapper.__meniw_governed__ = True  # type: ignore[attr-defined]
            return wrapper

        return decorator

    def guard(self, name: str, categories: list[str] | None = None,
              irreversible: bool = False, context: dict | None = None) -> dict:
        """Imperative check for non-decorated call sites (e.g. dispatching a tool by name).

        Returns the governance result dict; raises ProhibitedActionError if blocked when
        used via `enforce()`.
        """
        action = Action(name=name, categories=list(categories or []), irreversible=irreversible)
        return self.gate.governed_execute(action, dict(context or {}), lambda a: None)

    def enforce(self, name: str, run: Callable[[], Any], categories: list[str] | None = None,
                irreversible: bool = False, context: dict | None = None) -> Any:
        """Run `run()` only if the named action passes; otherwise raise."""
        action = Action(name=name, categories=list(categories or []), irreversible=irreversible)
        out = self.gate.governed_execute(action, dict(context or {}), lambda a: run())
        if not out["executed"]:
            raise ProhibitedActionError(out["verdict"], out["receipt"])
        return out["result"]
