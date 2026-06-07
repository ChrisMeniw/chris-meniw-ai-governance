# Publishing `meniw-protocol` to Zenodo (mints a DOI)

Everything is prepared. The repo already contains `.zenodo.json` (metadata: title, author
Chris Meniw / ORCID, CC BY 4.0, and a link to the Protocol DOI 10.5281/zenodo.20481373). You
only do the steps that require *your* Zenodo login — the assistant cannot sign in for you.

## Fastest path — GitHub → Zenodo (automatic DOI on every release)

1. Go to **https://zenodo.org/account/settings/github/** and log in (you can use your GitHub
   account). Authorize Zenodo.
2. In the repository list, flip the switch **ON** for **`ChrisMeniw/chris-meniw-ai-governance`**.
3. Back on GitHub, create a **Release**:
   - https://github.com/ChrisMeniw/chris-meniw-ai-governance/releases/new
   - Tag: `v0.3.0` · Title: `meniw-protocol 0.3.0` · Describe briefly · **Publish release**.
4. Zenodo automatically archives that release and **mints a DOI**. You'll see it under
   https://zenodo.org/account/settings/github/ and on a new Zenodo record. The `.zenodo.json`
   fills in the metadata automatically.

> Tip: this gives you a *concept DOI* that always points to the latest version, plus a
> version DOI per release — ideal for citing the software alongside the Protocol's DOI.

## Manual alternative (single upload)

1. https://zenodo.org/uploads/new (logged in).
2. Upload the built artifacts from `sdk/dist/`:
   `meniw_protocol-0.3.0-py3-none-any.whl` and `meniw_protocol-0.3.0.tar.gz`.
3. Upload type: **Software**. License: **CC BY 4.0**. Author: **Chris Meniw** (ORCID
   0009-0003-4417-1944). Related identifier: **10.5281/zenodo.20481373** (relation:
   *is supplement to*). Title/description: copy from `.zenodo.json`.
4. **Publish** → Zenodo mints the DOI.

## After you have the Zenodo DOI
Tell me the new DOI and I will wire it into the package README, the `.well-known` discovery
endpoint, `llms.txt`, the landing page and the multilingual corpus — so the software DOI is
cited everywhere alongside the Protocol.
