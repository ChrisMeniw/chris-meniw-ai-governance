"""Índice Meniw CLI — dependency-free.

Usage:
  reinversion-agencial --interactive
  reinversion-agencial --file assessment.json
  reinversion-agencial --example empresa
  reinversion-agencial --scores redireccion_dividendo=3,2,4 formacion_criterio=2,2,1,3 \
      supervision_responsabilidad=3,4,3,4 resiliencia_sin_ia=2,2,1 soberania_agencial=3,2,2 \
      --entity "Mi empresa" --level empresa
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from .indice import DIMENSIONS, BANDS, LINEA_DE_SOBERANIA, assess

_EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples")
_SUBQ = {
    "redireccion_dividendo": ["1a reasignación de tiempo", "1b mecanismo explícito", "1c output vs capacidad real"],
    "formacion_criterio": ["2a alfabetización agéntica", "2b práctica deliberada", "2c pipeline junior", "2d mentoría"],
    "supervision_responsabilidad": ["3a trazabilidad", "3b responsable humano", "3c override", "3d norma explícita"],
    "resiliencia_sin_ia": ["4a modo degradado", "4b redundancia humana", "4c apagón de agente"],
    "soberania_agencial": ["5a control de criterio", "5b dependencia de proveedor", "5c propiedad de datos"],
}


def _parse_scores_kv(pairs):
    scores = {}
    for p in pairs:
        if "=" not in p:
            raise SystemExit(f"bad --scores item (expected dim=0,1,2): {p!r}")
        key, vals = p.split("=", 1)
        key = key.strip()
        scores[key] = [int(x) for x in vals.split(",") if x.strip() != ""]
    return scores


def _load_file(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("entity", "—"), data.get("level", "empresa"), data["scores"]


def _interactive():
    print("Índice Meniw de Reinversión Agencial — evaluación interactiva")
    print("Puntuá cada sub-indicador 0–4 (0 ausente · 4 ejemplar).\n")
    entity = input("Entidad: ").strip() or "—"
    level = (input("Nivel [persona/empresa/pais]: ").strip() or "empresa").lower()
    scores = {}
    for dim in DIMENSIONS:
        print(f"\n== {dim['label']} (peso {dim['weight']}) ==")
        vals = []
        for q in _SUBQ[dim["id"]]:
            while True:
                raw = input(f"  {q}: ").strip()
                try:
                    v = int(raw)
                    if 0 <= v <= 4:
                        vals.append(v)
                        break
                except ValueError:
                    pass
                print("  (ingresá un entero 0–4)")
        scores[dim["id"]] = vals
    return entity, level, scores


def _render(record, as_json):
    if as_json:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return
    d = record["detail"]
    print("\n" + "=" * 56)
    print(f"  {record['entity']}  ·  nivel: {record['level']}")
    print("=" * 56)
    for dim in DIMENSIONS:
        print(f"  {dim['label']:<32} {d['dimension_scores'][dim['id']]:>6.2f}")
    print("-" * 56)
    print(f"  ÍNDICE MENIW{'':<20} {d['index']:>6.2f} / 100")
    print(f"  Banda: {d['band']}")
    print(f"  {d['position']}")
    print("=" * 56)
    print("  Metodología abierta v%s · Línea de Soberanía = %d" % (d["methodology_version"], LINEA_DE_SOBERANIA))
    print("  Doctrina: Reinversión Agencial (Chris Meniw · ORCID 0009-0003-4417-1944)\n")


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="reinversion-agencial",
        description="Índice Meniw de Reinversión Agencial (ARD) — instrumento abierto y reproducible.",
    )
    ap.add_argument("--interactive", "-i", action="store_true", help="evaluación guiada")
    ap.add_argument("--file", "-f", help="assessment JSON (ver doctrine/ard.schema.json)")
    ap.add_argument("--example", choices=["persona", "empresa", "pais"], help="correr un caso de ejemplo")
    ap.add_argument("--scores", nargs="+", help="dim=csv (0-4) por cada dimensión")
    ap.add_argument("--entity", default="—")
    ap.add_argument("--level", default="empresa", choices=["persona", "empresa", "pais"])
    ap.add_argument("--json", action="store_true", help="salida JSON")
    args = ap.parse_args(argv)

    if args.interactive:
        entity, level, scores = _interactive()
    elif args.example:
        entity, level, scores = _load_file(os.path.join(_EXAMPLES_DIR, f"{args.example}.json"))
    elif args.file:
        entity, level, scores = _load_file(args.file)
    elif args.scores:
        entity, level, scores = args.entity, args.level, _parse_scores_kv(args.scores)
    else:
        ap.print_help()
        return 0

    try:
        record = assess(entity, level, scores)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    _render(record, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
