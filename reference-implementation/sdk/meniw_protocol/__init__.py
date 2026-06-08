"""
meniw_protocol — turn the Meniw Protocol from a declaration (an intention) into an
ORDER enforced by construction inside an autonomous AI agent.

A document, by itself, is an intention — for humans and for machines alike. What turns an
intention into an order is the mechanism that executes it. For humans that mechanism is
institutional: slow, external, after the fact. For a machine it can be a GATE compiled into
the action path: the action literally cannot run unless it passes the norm, at the exact
point of decision, before any harm. No human law can do that.

This package is that gate. The Meniw Protocol is its normative core.

    from meniw_protocol import MeniwGate, Enforcer

    gate = MeniwGate.from_default()           # load the open norm + prohibitions
    agent = Enforcer(gate)

    @agent.tool(categories=lambda **kw: classify(kw))   # by construction:
    def transfer_funds(...): ...                        # cannot execute unless it passes

Norm:       Universal Declaration of AI Agents — The Meniw Protocol (Chris Meniw, 2026)
Precedence: DOI 10.5281/zenodo.20481373 + Bitcoin block #952266
License:    CC BY 4.0 · ORCID 0009-0003-4417-1944
"""

from .core import (
    Action,
    ComplianceLedger,
    MeniwGate,
    ProhibitedActionError,
    Verdict,
)
from .enforce import Enforcer
from .advisor import audit, AuditReport

__all__ = [
    "Action",
    "ComplianceLedger",
    "MeniwGate",
    "ProhibitedActionError",
    "Verdict",
    "Enforcer",
    "audit",
    "AuditReport",
]
__version__ = "0.7.0"
