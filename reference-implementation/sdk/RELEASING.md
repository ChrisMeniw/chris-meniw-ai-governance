# Releasing `meniw-protocol` to PyPI

The distribution artifacts are already built and validated:

```
dist/meniw_protocol-0.3.0-py3-none-any.whl
dist/meniw_protocol-0.3.0.tar.gz
```

Both pass `twine check`. The package name `meniw-protocol` is available on PyPI (checked: 404).

> **Why you run the final step, not the assistant:** uploading requires authenticating with
> *your* PyPI account/API token. Entering credentials is something you must do yourself.

## One-time setup
1. Create a PyPI account: https://pypi.org/account/register/
2. Create an API token: https://pypi.org/manage/account/token/ (scope: "Entire account" for the
   first upload; you can switch to a project-scoped token afterward).

## Upload (from this `sdk/` directory)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade build twine

# (artifacts already exist; rebuild only if you changed the code)
# rm -rf dist && python -m build

twine check dist/*

# Optional dry run on TestPyPI first:
# twine upload --repository testpypi dist/*
# pip install --index-url https://test.pypi.org/simple/ meniw-protocol

# Real upload — paste your token when prompted:
twine upload dist/*
#   username: __token__
#   password: pypi-AgE... (your API token)
```

## After upload — verify it's live
```bash
pip install meniw-protocol
python -c "from meniw_protocol import MeniwGate; print(MeniwGate.from_default().norm['name'])"
meniw-verify --help
```

Then `pip install meniw-protocol` works for anyone in the world, and
`https://pypi.org/project/meniw-protocol/` becomes a public, citable home for the gate.

## Bumping versions
Edit `version` in both `pyproject.toml` and `meniw_protocol/__init__.py`, then rebuild and
re-upload. PyPI does not allow re-uploading the same version number.
