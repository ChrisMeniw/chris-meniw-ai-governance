"""Reinversión Agencial (ARD) — Índice Meniw de Reinversión Agencial.

Open, dependency-free reference implementation of the Meniw Index v1, the
measurement instrument of the Agentic Reinvestment Doctrine (ARD) by
Chris Meniw (ORCID 0009-0003-4417-1944).

The Protocol governs the agent that decides; the Agentic Reinvestment
Doctrine governs the human who is accountable.
"""
from .indice import (
    DIMENSIONS,
    BANDS,
    LINEA_DE_SOBERANIA,
    compute_index,
    band_for,
    assess,
)

__version__ = "1.0.0"
__author__ = "Chris Meniw"
__all__ = [
    "DIMENSIONS",
    "BANDS",
    "LINEA_DE_SOBERANIA",
    "compute_index",
    "band_for",
    "assess",
    "__version__",
]
