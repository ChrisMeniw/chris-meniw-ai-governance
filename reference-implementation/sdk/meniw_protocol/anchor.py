"""
Anchoring the compliance-ledger HEAD to Bitcoin via OpenTimestamps.

The ledger is already tamper-evident on its own (an internal hash-chain). Anchoring binds the
chain HEAD to the Bitcoin blockchain so a third party can prove the whole ledger existed before
a given block — independently of you and of this machine.

Honesty contract: this module NEVER fabricates a proof.
- It always writes a deterministic local CHECKPOINT of the head (fast, no network).
- If the standard OpenTimestamps `ots` CLI is installed, it also produces a real `.ots` proof
  (submitted to free calendar servers; the proof becomes Bitcoin-confirmed a few hours later).
- If `ots` is not installed, it records the head and tells you exactly how to stamp it.

Install the optional dependency to enable real Bitcoin anchoring:
    pip install "meniw-protocol[anchor]"     # or: pipx install opentimestamps-client
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

_OTS = shutil.which("ots")


def ots_available() -> bool:
    return _OTS is not None


def checkpoint(head_hex: str, out_dir: str | Path, *, seq: int | None = None,
               stamp: bool = False) -> dict:
    """Record the current ledger head. Deterministic + fast. If `stamp=True` and the `ots` CLI
    is present, also create a real OpenTimestamps proof (best-effort, never raises)."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    head_file = out / f"head-{seq if seq is not None else ts}.txt"
    head_file.write_text(head_hex + "\n", encoding="utf-8")

    rec = {"head": head_hex, "seq": seq, "ts": ts, "head_file": str(head_file), "status": "checkpointed"}
    if stamp:
        if _OTS:
            try:
                subprocess.run([_OTS, "stamp", str(head_file)], check=True,
                               capture_output=True, timeout=90)
                rec["ots_file"] = str(head_file) + ".ots"
                rec["status"] = "ots_submitted_pending_bitcoin"
            except Exception as e:  # network/calendar/timeout — stay honest, don't crash
                rec["status"] = f"ots_error:{type(e).__name__}"
        else:
            rec["status"] = "ots_not_installed"
            rec["howto"] = f'pip install "meniw-protocol[anchor]" ; then: ots stamp {head_file}'

    with (out / "anchors.log.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    return rec


def verify(head_file: str | Path) -> dict:
    """Verify the OpenTimestamps proof for a checkpoint head file (needs the `ots` CLI)."""
    head_file = Path(head_file)
    ots_file = Path(str(head_file) + ".ots")
    if not _OTS:
        return {"ok": None, "status": "ots_not_installed"}
    if not ots_file.exists():
        return {"ok": False, "status": "no_ots_proof_for_this_head"}
    try:
        r = subprocess.run([_OTS, "verify", str(ots_file)], capture_output=True, text=True, timeout=90)
        return {"ok": r.returncode == 0, "output": (r.stdout + r.stderr).strip()}
    except Exception as e:
        return {"ok": False, "status": f"error:{type(e).__name__}"}
