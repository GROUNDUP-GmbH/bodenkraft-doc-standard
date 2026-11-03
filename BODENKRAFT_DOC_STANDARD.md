---
title: "BodenKraft Document Standard"
subtitle: "The authoring, metadata, and publication contract for all BodenKraft-compliant documents"
author:
  - name: "Ground UP GmbH"
    affiliation: "Iglasegasse 21-23, A-1190 Vienna"
date: "2026-04-18"
lang: en

bodenkraft:
  doc_id: "BK-STD-DOC-001"
  doc_type: "standard"
  doc_version: "1.0.1-draft"
  doc_status: "draft"
  classification: "Public"
  did: "did:web:bodenkraft.farm:standard:doc-001"
  governs:
    - "all BodenKraft-compliant published documents"
  methodology: null
  fact_sources:
    - type: "inspiration"
      ref: "EASA Form 1 / AS 9100"
    - type: "inspiration"
      ref: "ISO 9001:2015"
    - type: "inspiration"
      ref: "W3C Verifiable Credentials Data Model v2.0"
    - type: "inspiration"
      ref: "W3C Decentralized Identifiers (DIDs) v1.0"
  signatories: []
  language_variants: ["en"]
---

## 1. Purpose

This standard defines **how every BodenKraft-compliant document is authored,
structured, versioned, signed, and published**, so that:

1. **Humans** can read it as a normal Markdown/Quarto document.
2. **Machines** (AI systems like Jóska, OpenAgDB indexer, CI pipelines, DID
   resolvers) can parse its metadata, resolve its references, and validate
   its claims programmatically.
3. **Auditors** (Verra VVB, ICAO CORSIA reviewers, tax authorities,
   notified bodies) can trace every statement to a verifiable source with
   reproducible evidence.

The standard is inspired by aviation-grade document control (EASA Form 1,
AS 9100), quality management (ISO 9001), and the W3C Verifiable Credentials
data model.

## 2. Role & Scope

### 2.1 BodenKraft as a standard

BodenKraft is a **standards framework**  analogous to ISO 9000 or AS 9100.
It is **not** a company and **not** a product brand (though "BodenKraft"
is also used as a trademark for product lines that comply with the
standard).

### 2.2 Ground UP GmbH as current issuer

Ground UP GmbH (FN 481220 b, Vienna) is the current **issuer** of the
BodenKraft Document Standard and its own first **adopter**. The issuer
role may in future be delegated to a separate standards body.

### 2.3 Scope

This standard applies to all documents that are meant to be published,
reviewed, signed, or audited under a BodenKraft-compliant process. It does
**not** apply to:

- Source code (governed by code-level linting and docstring standards).
- Ephemeral working notes or agent transcripts.
- Third-party documents cited but not authored under this standard.

## 3. The Two-Block Frontmatter

Every document begins with YAML frontmatter containing exactly two sections:
**Block A (Quarto standard fields)** and **Block B (`bodenkraft:` ontology)**.

```yaml
---
# Block A  Quarto standard (drives rendering)
title: "Human-readable title"
subtitle: "Optional subtitle"
author:
  - name: "Full Name"
    affiliation: "Your Org"
date: "YYYY-MM-DD"
lang: "de" | "en" | "hu" | ...

# Block B  BodenKraft ontology (drives machine consumption)
bodenkraft:
  doc_id: "BK-<TYPE>-<TOPIC>-<NNN>"
  doc_type: "pdd | whitepaper | charter | contract | rulebook | manifest | pitch | standard | monitoring-plan | annex | catalog"
  doc_version: "SemVer, for example, 1.2.0 or 0.1.0-draft"
  doc_status: "draft | review | approved | superseded | retracted"
  classification: "Public | Internal | Confidential | Restricted"
  did: "did:web:bodenkraft.farm:<type>:<id>"
  issuer_did: "did:web:<issuer-domain>:issuer:<org>"
  governs: []
  supersedes: []
  superseded_by: null
  methodology:
    name: null
    version: null
    source: null
  fact_sources: []
  signatories: []
  language_variants: []
---
```

## 4. Field Reference

### 4.1 Block A  Quarto Standard

| Field | Required | Notes |
|-------|:--------:|-------|
| `title` | ? | Human-readable, sentence case |
| `subtitle` | ? | Optional one-liner |
| `author` | ? | Array of objects with `name`, optional `affiliation`, `orcid`, `email` |
| `date` | ? | ISO 8601 (YYYY-MM-DD)  date of last substantive edit |
| `lang` | ? | ISO 639-1 code  controls hyphenation, babel, cite style |

### 4.2 Block B  `bodenkraft:` Ontology

| Field | Required | Purpose |
|-------|:--------:|---------|
| `doc_id` | ? | Unique, stable identifier. Format: `BK-<TYPE>-<TOPIC>-<NNN>`. Never reused. |
| `doc_type` | ? | Controlled vocabulary (see §5.1) |
| `doc_version` | ? | Semantic Versioning. Suffix `-draft` allowed while `doc_status: draft`. |
| `doc_status` | ? | Lifecycle state (see §5.2) |
| `classification` | ? | Disclosure level (see §5.3) |
| `did` | ? | Decentralized Identifier for the document itself. Canonical form: `did:web:bodenkraft.farm:<type>:<id>`. |
| `issuer_did` | ? | DID of the organisation that issues/signs this document. Defaults to Ground UP GmbH when authored under Ground UP. Example: `did:web:groundup.farm:issuer:gmbh`. |
| `governs` | ? | List of systems, modules, or processes this document is authoritative for. |
| `supersedes` | ? | List of `doc_id@version` values this document replaces. |
| `superseded_by` | ? | Set by the successor when this document is superseded. |
| `retraction_reason` | ?? | Required when `doc_status: retracted`. |
| `methodology` | ? | Named methodology reference (for example, VM0042 v2.2). |
| `fact_sources` | ? | Array of sources the document relies on (see §6). |
| `signatories` | ? | Array of signer objects: `{ name, role, date, signature_ref }`. |
| `language_variants` | ? | List of other `lang` codes where this document exists as a parallel variant. |

## 5. Controlled Vocabularies

### 5.1 `doc_type`

| Value | Description |
|-------|-------------|
| `pdd` | Project Design Document (Verra VM0042, VT0014) |
| `whitepaper` | Public-facing strategy / technology whitepaper |
| `charter` | Foundational governance document (for example, Tokenomics Charter) |
| `contract` | Legally binding agreement (farmer contract, CORSIA purchase agreement) |
| `rulebook` | Internal rules of engagement |
| `manifest` | Philosophical statement of principles |
| `pitch` | Investor / partner presentation material |
| `standard` | A document defining a standard (like this one) |
| `monitoring-plan` | Client-specific monitoring configuration per VM0042 |
| `annex` | Formal annex to another document |
| `catalog` | Auto-generated catalog derived from structured data (for example, OpenAgDB) |

### 5.2 `doc_status`  Document Lifecycle

```
draft  ???  review  ???  approved  ???  superseded
                                  ???   retracted
```

| State | Meaning |
|-------|---------|
| `draft` | Authoring in progress, no external circulation |
| `review` | Frozen content under review by nominated reviewers |
| `approved` | Signed, effective, canonical |
| `superseded` | Historical, replaced by `superseded_by` |
| `retracted` | Withdrawn, must not be used (requires `retraction_reason`) |

### 5.3 `classification`

| Level | Description | Distribution |
|-------|-------------|--------------|
| `Public` | No restriction | Website, GitHub Pages, investor pitches |
| `Internal` | Issuer team + contracted partners | Private repo, Team Drive |
| `Confidential` | Specific named recipients only | Named-access share, encrypted |
| `Restricted` | Requires NDA + specific authorisation | Out-of-band, tracked chain of custody |

## 6. `fact_sources`  Source Schema

Every non-trivial claim in a document should be backed by an entry here:

```yaml
fact_sources:
  - type: "standard"
    ref: "VM0042 v2.2 §8.1.2"
    path: "external/verra/VM0042v2.2.pdf"
    excerpt: "SOC_stock = SOC_conc × BD × depth ..."
  - type: "measurement"
    ref: "Berend Kft 2021-2023 SOC sampling campaign"
    path: "data/measurements/berend_kft/soc_2021_2023.parquet"
  - type: "calculation"
    ref: "SOMA calibration run 2026-03-15"
    path: "docs/pdd/vm0042-eu/03-soma-calibration.ipynb"
    commit: "a1b2c3d"
  - type: "literature"
    ref: "Nevalainen et al. 2022"
    doi: "10.5194/gi-11-93-2022"
  - type: "assumption"
    ref: "Protocol multiplier values (1.0-2.0)"
    rationale: "Initial calibration pending network validation"
  - type: "dataset"
    ref: "OpenAgDB plant record"
    openagdb_id: "plant_phacelia_tanacetifolia"
    commit: "e4f5g6h"
```

### Supported `type` values

`standard`, `measurement`, `calculation`, `literature`, `assumption`,
`inspiration`, `dataset`.

## 7. Fact-Classification Badges

Inside the document body, **every numeric claim and normative statement
must be badged**. The badges are machine-parseable and tie back to
`fact_sources`:

| Badge (Quarto callout) | Legacy marker | Meaning |
|-----------------------|---------------|---------|
| `::: {.fact ref="..."}` | ? FAKT | Established fact from a standard document |
| `::: {.measured ref="..."}` | ? GEMESSEN | Measured value from an identified instrument / lab |
| `::: {.calculated ref="..."}` | ? BERECHNET | Computed via a named formula with named inputs |
| `::: {.assumption rationale="..."}` | ?? ANNAHME | Assumed value  must include rationale |
| `::: {.unknown owner="..." due="..."}` | ? UNBEKANNT | Gap  must include resolver and deadline |

Example:

```markdown
::: {.fact ref="VM0042v2.2-8.1.2"}
SOC stock is calculated as the product of SOC concentration, bulk density,
and sampling depth.
:::

::: {.measured ref="berend-kft-2021-2023"}
Pilot farm Berend Kft recorded ?SOC = +0.28 % (0-30 cm) over 12 months.
:::

::: {.assumption rationale="Pending Regenified tier audit 2026-Q3"}
Protocol multiplier of 1.4 for Regenified Tier 3 participants.
:::
```

The Quarto Lua filter `bodenkraft-frontmatter-validate.lua` checks that
every badge `ref` resolves to an entry in `fact_sources`.

## 8. File Naming & Location

```
docs/
??? <doc_type>/
?   ??? <slug>/
?       ??? index.qmd            # Main entry point
?       ??? <NN>-<section>.qmd   # Numbered sections
?       ??? <NN>-<section>.ipynb # Executable sections
?       ??? _metadata.yml        # Local overrides
```

- `doc_id` is the canonical reference. The directory slug is a
  human-friendly alias and may differ.
- Numbered section files (for example, `10-front-matter.qmd`) preserve ordering.

## 9. Versioning Rules

- Follow **Semantic Versioning** (SemVer 2.0.0) for `doc_version`.
  - **MAJOR**: Breaking change  invalidates prior audits or citations.
  - **MINOR**: Substantive content addition, no breakage.
  - **PATCH**: Typos, clarifications, formatting.
- A `doc_status: approved` document **must not** be edited in place. Any
  change creates a new version; the prior version is archived with
  `superseded_by` pointing to the new `doc_id@version`.
- Git commits that modify an `approved` document must reference the
  approving signatory decision (for example, `Ref: DEC-2026-042  CFO approval`).

## 10. DID & Signature Architecture

### 10.1 Separation of Standard and Issuer namespaces

| Namespace | Purpose | Example |
|-----------|---------|---------|
| `did:web:bodenkraft.farm:...` | Documents, certificates, standard artefacts | `did:web:bodenkraft.farm:pdd:vm0042-at-hu-001` |
| `did:web:<issuer>.<tld>:issuer:<org>` | The organisation that signs/issues | `did:web:groundup.farm:issuer:gmbh` |

### 10.2 Signature chain

1. Document `did` is minted in the standard namespace.
2. Issuer `issuer_did` signs the document's content hash (for example, SHA-256 of
   the rendered canonical form) using a key published at the issuer's
   DID Document.
3. The signature is stored either in `signatories[].signature_ref` (URI
   to a detached signature) or on an anchoring ledger (RDDL / Planetmint).

### 10.3 Multiple issuers over time

A document may later be issued by a different organisation (for example, a
notified body signs off on a PDD). In that case a new version is
produced with additional entries in `signatories`.

## 11. CI Enforcement

The Lua filter `bodenkraft-frontmatter-validate.lua` runs during Quarto
rendering and calls the JSON Schema at `schema/bodenkraft-frontmatter.json`.
A build **fails** if:

- A rendered document is missing the `bodenkraft:` block.
- A required field is missing or violates its enum.
- `doc_id` collides with another document in the tree.
- `supersedes` references a non-existent `doc_id`.
- `classification: Public` is set but the render target is marked internal.
- A body badge references a non-existent `fact_sources` entry.

## 12. AI / Agent Integration

Every rendered HTML page emits a JSON-LD block in its `<head>` exposing
the `bodenkraft:` metadata plus resolved DIDs and section hashes. This
enables AI systems (such as Jóska) to:

1. **Index by metadata**  retrieval by `doc_id`, `doc_type`, `governs`,
   `methodology`  not by raw full-text.
2. **Cite with integrity**  when an AI cites a fact, it references the
   `doc_id@version` and the `fact_sources` entry, not a URL.
3. **Detect staleness**  refuse to quote from a document whose
   `doc_status` is `superseded` or `retracted`, warn the user.
4. **Replay audits**  every AI response can be replayed by resolving
   cited `doc_id@version` from the git history.

## 13. Relationship to Existing Documents

Migration paths for Ground UP legacy documents:

| Legacy | Future location (within adopter repo) | Notes |
|--------|---------------------------------------|-------|
| `docs/latex/pdd/main.tex` | `docs/pdd/vm0042-eu/index.qmd` | Preserve section numbering; LaTeX preamble re-used via `include-in-header`. |
| `docs/latex/whitepaper/main.tex` | `docs/whitepaper/v2/index.qmd` | Rewrite as v2 (aligned with Tokenomics Charter). |
| `docs/latex/contracts/farmer_contract/` | `docs/contracts/farmer/` | DE/HU/EN variants per `language_variants`. |
| `docs/business_model/RULEBOOK_*.md` | Remain Markdown; add `bodenkraft:` frontmatter. | Non-breaking. |
| `docs/RULEBOOK_OPENAGDB.md` (OpenAgDB repo) | Same file; add `bodenkraft:` frontmatter. | Cross-repo; same standard. |

## 14. Writing Language

Documents under this standard use **ASD-STE100 Simplified Technical English**
(Issue 9, 2025-01-15) as their writing language.

This standard governs the metadata of a document. ASD-STE100 governs the
sentences. A document can pass the schema check and still fail the reader.

### 14.1 Limits

| Rule | Limit |
|------|-------|
| Sentence length in a procedure | 20 words |
| Sentence length in a description | 25 words |
| Sentences in a paragraph | 6 |
| Words in a multi-word noun | 3 |
| Punctuation | no semicolon |
| Verb forms | infinitive, imperative, simple present, simple past, simple future, past participle as adjective |
| Voice | active; passive only in a description, when the agent is unknown |
| Spelling | American English |

### 14.2 Words

- Use a word that is approved in the ASD-STE100 dictionary, a technical noun or
  a technical verb.
- A technical noun comes from the project glossary. Keep it short. Use the same
  name for the same item in every document.
- Do not use phrasal verbs, contractions, Latin abbreviations or slang.

### 14.3 Check before you publish

```bash
python3 tools/ste100_check.py <files or directories> --mode auto
```

The tool checks the mechanical rules in section 14.1. It does not check the
dictionary, and it does not replace a reader.

### 14.4 The dictionary

The ASD-STE100 dictionary is licensed, and ASD reserves all rights. It is not in
this repository. A derived machine-readable copy for our own text checks is in
the internal repository, folder `70_Meta/ste100/`. Do not copy that file into a
public repository.

### 14.5 Scope

This section applies to documents that a reader must act on: specifications,
manuals, contracts, procedures and error catalogues. It does not apply to
internal working notes or transcripts.

## 15. Open Items

::: {.unknown owner="Stefan Fölser" due="2026-05-01"}
Final decision on DID method for anchoring (`did:web`, `did:key` or
custom RDDL method) and signing-key custody (HSM, cloud KMS, or
hardware-embedded secure element).
:::

::: {.unknown owner="Stefan Fölser" due="2026-05-15"}
Domain registration of `bodenkraft.farm` and `groundup.farm` DID webroots
(`.well-known/did.json`).
:::

## 16. Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.1-draft | 2026-11-03 | Section 14: writing language ASD-STE100, checker tool |
| 1.0.0-draft | 2026-04-18 | Initial draft  supersedes implicit LaTeX-only conventions in Ground UP legacy repos |
