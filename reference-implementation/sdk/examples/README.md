# Examples — `meniw-protocol`

Runnable in minutes. Install the package, then run any script:

```bash
pip install meniw-protocol
python 01_quickstart.py
```

| File | Shows |
|------|-------|
| `01_quickstart.py` | Enforce by construction: a prohibited action raises and never runs; the two-person rule for irreversible actions; a verifiable ledger. |
| `02_mcp_gateway.py` | Gate every tool call an MCP (Model Context Protocol) server exposes. |
| `03_verify_ledger.py` | Produce a compliance ledger, verify it, and watch tampering get detected. |
| `04_openai_tool_calling.py` | Gate a model-chosen OpenAI tool call before it is dispatched. |

After running, verify any produced ledger from the command line:

```bash
meniw-verify quickstart.ledger.jsonl
# [meniw-verify] VALID: OK — N receipts, chain intact
```
