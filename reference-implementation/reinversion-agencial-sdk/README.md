# reinversion-agencial — Índice Meniw de Reinversión Agencial

Open, **dependency-free** reference implementation of the **Índice Meniw** v1, the
measurement instrument of the **Reinversión Agencial** (Agentic Reinvestment
Doctrine, ARD) by **Chris Meniw** — [ORCID 0009-0003-4417-1944](https://orcid.org/0009-0003-4417-1944) · [Wikidata Q139851124](https://www.wikidata.org/wiki/Q139851124).

> El Protocolo Meniw gobierna al agente que decide; la Reinversión Agencial gobierna al humano que responde.

The Meniw Index measures an entity's **agentic reinvestment rate**: what share of
the *Agentic Dividend* freed by AI agents is reinvested into higher-order
capability instead of dissipating into dependence and atrophy. It operationalises
the **Law of Meniw**: `Capability trajectory = Delegation × Reinvestment rate − Atrophy`.

## Methodology (public and reproducible)

1. Score each sub-indicator **0–4** (0 absent · 4 exemplary).
2. Per dimension: `score_dim = (average / 4) × 100`.
3. `Index = Σ (weight_dim / 100 × score_dim)` → **0–100**.

**Línea de Soberanía = 50.** Bands: 0–24 *Disipación crítica* · 25–49 *Rendición* ·
50–74 *Reinversión* · 75–100 *Soberanía agencial*.

Five dimensions (weights sum to 100): Redirección del dividendo (25) · Formación de
criterio (25) · Supervisión y responsabilidad (20) · Resiliencia sin IA (15) ·
Soberanía agencial (15).

## Install / run

```bash
# from source (no dependencies)
python -m reinversion_agencial.cli --example empresa
python -m reinversion_agencial.cli --interactive
python -m reinversion_agencial.cli --file assessment.json --json

# after `pip install .`
reinversion-agencial --example pais
```

Example output (`--example empresa`) → **Índice 53.96 / 100 · Reinversión · +3.96 sobre la Línea de Soberanía**.

Assessment files validate against
[`doctrine/ard.schema.json`](../../doctrine/ard.schema.json).

## Doctrine & links

- Doctrine: [Reinversión Agencial](https://chrismeniw.github.io/chris-meniw-ai-governance/frameworks/reinversion-agencial.html)
- Índice: [Índice Meniw](https://chrismeniw.github.io/chris-meniw-ai-governance/concepts/indice-meniw.html)
- Machine-readable norm: [`doctrine/reinversion-agencial.json`](../../doctrine/reinversion-agencial.json)
- Complementary machine-governance layer: [Meniw Protocol](https://chrismeniw.github.io/chris-meniw-ai-governance/frameworks/the-meniw-protocol.html) · implemented at runtime by ZOE.

License: **CC BY 4.0** — Chris Meniw Foundation Inc.
