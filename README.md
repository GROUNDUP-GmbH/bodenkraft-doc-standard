# BodenKraft Document Standard

> **What this is.** The BodenKraft Document Standard defines how documents
> across all BodenKraft-compliant organisations are authored, versioned,
> signed, and published — so that humans can read them, machines (AI systems,
> indexers, CI) can parse them, and auditors can trace every claim to a
> source.
>
> **Analogy.** BodenKraft plays the role of ISO 9000 / AS 9100 for soil-health,
> MRV and agri-software documentation. Ground UP GmbH is both the **issuer**
> of the standard and an **adopter**. Other organisations may also adopt it.

## Status

- **Current version:** `v1.0.0-draft`
- **License (text):** [CC BY 4.0](./LICENSE-CC-BY-4.0)
- **License (tooling):** [MIT](./LICENSE-MIT)
- **Issuer:** Ground UP GmbH (FN 481220 b, Vienna)
- **Canonical DID namespace (documents):** `did:web:bodenkraft.farm:...`
- **Canonical DID namespace (issuers):** `did:web:<issuer-domain>:issuer:<org>`

## What's in this repo

| Path | Purpose |
|------|---------|
| [`BODENKRAFT_DOC_STANDARD.md`](./BODENKRAFT_DOC_STANDARD.md) | The normative specification |
| [`schema/bodenkraft-frontmatter.json`](./schema/bodenkraft-frontmatter.json) | JSON Schema for the `bodenkraft:` YAML block (CI-validatable) |
| [`filters/bodenkraft-frontmatter-validate.lua`](./filters/bodenkraft-frontmatter-validate.lua) | Quarto Lua filter that validates every rendered document |
| [`includes/`](./includes/) | Shared LaTeX preamble and SCSS theme for consistent look & feel |
| [`examples/minimal-document.qmd`](./examples/minimal-document.qmd) | Smallest possible valid document |
| [`.github/workflows/validate.yml`](./.github/workflows/validate.yml) | CI that validates schema consistency on every push |

## How to adopt it in your repo

### Option A: Git submodule (recommended)

```bash
cd your-repo
git submodule add https://github.com/GROUNDUP-GmbH/bodenkraft-doc-standard.git docs/_bodenkraft_standard
```

Then in your `_quarto.yml`:

```yaml
filters:
  - docs/_bodenkraft_standard/filters/bodenkraft-frontmatter-validate.lua

format:
  pdf:
    include-in-header:
      - docs/_bodenkraft_standard/includes/bodenkraft-pdf-preamble.tex
  html:
    theme:
      - cosmo
      - docs/_bodenkraft_standard/includes/bodenkraft-light.scss
```

### Option B: Copy (for experimentation only)

Copy the needed files directly. Remember to track upstream changes manually.

## How to author a document

Every document starts with a two-block YAML frontmatter:

```yaml
---
title: "Your Document Title"
author:
  - name: "Author Name"
    affiliation: "Your Org"
date: "YYYY-MM-DD"
lang: "en"

bodenkraft:
  doc_id: "BK-PDD-VM0042-AT-HU-001"
  doc_type: "pdd"
  doc_version: "0.1.0-draft"
  doc_status: "draft"
  classification: "Internal"
  did: "did:web:bodenkraft.farm:pdd:vm0042-at-hu-001"
---
```

See [`BODENKRAFT_DOC_STANDARD.md`](./BODENKRAFT_DOC_STANDARD.md) for the full
field reference, controlled vocabularies, and lifecycle rules.

## Governance

- The standard is maintained by **Ground UP GmbH** as the current issuer.
- Proposed changes go through Pull Requests against this repo.
- Breaking changes require a MAJOR version bump and a migration note in
  [`CHANGELOG.md`](./CHANGELOG.md).
- Every release is tagged with SemVer (`v1.0.0`, `v1.1.0`, `v2.0.0`, ...).

## Contact

Ground UP GmbH · Iglasegasse 21-23, A-1190 Vienna · https://groundup.farm
