# Changelog

All notable changes to the BodenKraft Document Standard are documented here.
The project adheres to [Semantic Versioning](https://semver.org/) and
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [1.0.0-draft] — 2026-04-18

### Added
- Initial standard specification (`BODENKRAFT_DOC_STANDARD.md`).
- JSON Schema for the `bodenkraft:` frontmatter block
  (`schema/bodenkraft-frontmatter.json`).
- Quarto Lua filter for runtime validation
  (`filters/bodenkraft-frontmatter-validate.lua`).
- Minimal example document (`examples/minimal-document.qmd`).
- CI workflow validating schema self-consistency and example frontmatter
  (`.github/workflows/validate.yml`).
- Dual licensing: CC BY 4.0 for the standard text, MIT for tooling.

### Notes
- Inspired by EASA Form 1 / AS 9100, ISO 9001, and the W3C Verifiable
  Credentials Data Model.
- DID namespaces split between `bodenkraft.farm` (standard / documents
  / certificates) and issuer domains such as `groundup.farm` (signing
  authorities).
