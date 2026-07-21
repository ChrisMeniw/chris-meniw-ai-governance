"""Índice Meniw de Reinversión Agencial — Rúbrica v1 (methodology exact per ARD ARCHIVO 2).

Pure standard library. Metodología pública y reproducible:
  1. cada sub-indicador se puntúa 0-4 (0 ausente ... 4 ejemplar)
  2. por dimensión: score_dim = (promedio de sus sub-indicadores / 4) * 100
  3. Índice = Σ (peso_dim / 100 * score_dim)  ->  0-100
Línea de Soberanía = 50 (valor v1, calibrable; versionado públicamente).
"""
from __future__ import annotations

METHODOLOGY_VERSION = "1.0"
LINEA_DE_SOBERANIA = 50

# Five dimensions, weights sum to 100 (ARCHIVO 2).
DIMENSIONS = [
    {"id": "redireccion_dividendo", "label": "Redirección del dividendo", "weight": 25,
     "anchor": "Dividendo Agencial"},
    {"id": "formacion_criterio", "label": "Formación de criterio", "weight": 25,
     "anchor": "Escalera rota / alfabetización agéntica"},
    {"id": "supervision_responsabilidad", "label": "Supervisión y responsabilidad", "weight": 20,
     "anchor": "Borde agéntico / Protocolo Meniw"},
    {"id": "resiliencia_sin_ia", "label": "Resiliencia sin IA", "weight": 15,
     "anchor": "Antifragilidad"},
    {"id": "soberania_agencial", "label": "Soberanía agencial", "weight": 15,
     "anchor": "Soberanía cognitiva"},
]

# Bands (inclusive ranges).
BANDS = [
    {"range": (0, 24), "label": "Disipación crítica"},
    {"range": (25, 49), "label": "Rendición"},
    {"range": (50, 74), "label": "Reinversión"},
    {"range": (75, 100), "label": "Soberanía agencial"},
]

_DIM_IDS = {d["id"] for d in DIMENSIONS}
_WEIGHTS = {d["id"]: d["weight"] for d in DIMENSIONS}


def _validate_score(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"sub-indicator must be an integer 0-4, got {value!r}")
    if not (0 <= value <= 4):
        raise ValueError(f"sub-indicator out of range 0-4: {value}")
    return value


def dimension_score(subindicators) -> float:
    """score_dim = (average of 0-4 sub-indicators / 4) * 100."""
    vals = [_validate_score(v) for v in subindicators]
    if not vals:
        raise ValueError("each dimension needs at least one sub-indicator (0-4)")
    return (sum(vals) / len(vals) / 4) * 100


def compute_index(scores: dict) -> dict:
    """scores: {dimension_id: [subindicator, ...]}. Returns detail + weighted index."""
    missing = _DIM_IDS - set(scores)
    if missing:
        raise ValueError(f"missing dimensions: {sorted(missing)}")
    extra = set(scores) - _DIM_IDS
    if extra:
        raise ValueError(f"unknown dimensions: {sorted(extra)}")

    dim_scores = {}
    weighted = 0.0
    for dim_id, subs in scores.items():
        s = dimension_score(subs)
        dim_scores[dim_id] = round(s, 2)
        weighted += (_WEIGHTS[dim_id] / 100) * s

    index = round(weighted, 2)
    return {
        "index": index,
        "dimension_scores": dim_scores,
        "band": band_for(index),
        "linea_de_soberania": LINEA_DE_SOBERANIA,
        "position": _position(index),
        "methodology_version": METHODOLOGY_VERSION,
    }


def band_for(index: float) -> str:
    idx = round(index)
    for b in BANDS:
        lo, hi = b["range"]
        if lo <= idx <= hi:
            return b["label"]
    return BANDS[-1]["label"] if idx > 100 else BANDS[0]["label"]


def _position(index: float) -> str:
    if index >= LINEA_DE_SOBERANIA:
        return f"Encima de la Línea de Soberanía (50): reinversión (+{round(index - LINEA_DE_SOBERANIA, 2)})"
    return f"Debajo de la Línea de Soberanía (50): rendición ({round(index - LINEA_DE_SOBERANIA, 2)})"


def assess(entity: str, level: str, scores: dict) -> dict:
    """Full assessment record (validates against doctrine/ard.schema.json shape)."""
    if level not in ("persona", "empresa", "pais"):
        raise ValueError("level must be one of: persona, empresa, pais")
    result = compute_index(scores)
    return {
        "entity": entity,
        "level": level,
        "methodology_version": METHODOLOGY_VERSION,
        "scores": {k: list(v) for k, v in scores.items()},
        "result": {
            "index": result["index"],
            "band": result["band"],
            "vs_linea_soberania": result["position"],
        },
        "detail": result,
    }
