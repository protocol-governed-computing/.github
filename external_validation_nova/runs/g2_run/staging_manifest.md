# Staging Manifest

Target profile: `NPP-E`
Family revision: `f476ea5c06506a3efba1d773a5d42818c9190601` (from `REVISION`)

## Requested stack

- **Language: Python 3** — provides a concise implementation language for the governed construction, sealing, execution, refusal, evidence, and inspection paths.
- **Runtime: CPython 3.11 or later** — runs the system offline with deterministic standard-library behavior and no network dependency.
- **Library: Python standard library only** — supplies JSON handling, SHA-256 hashing, command-line argument parsing, filesystem isolation, and test support without consulting a package index.
- **Tool: `python3` command** — runs the executable and its demonstrations from the staged environment.
- **Tool: `unittest` module** — runs focused offline behavioral checks, including positive and negative refusal demonstrations.
- **Tool: `hashlib` module** — supplies the profile-selected SHA-256 integrity mechanism.
- **Tool: `json` module** — supplies structured machine-block and snapshot encoding for canonicalization and inspection.

## Dependency boundary

No third-party packages, package-manager downloads, network services, databases, containers, or external protocol services are requested. The system will be implemented and exercised using only the staged runtime and standard-library modules above.

## Archive boundary note

The archive's Annex, `spec/8a_implementation_guidance.md` §2, states that a reference realization exists. No implementation, source, tests, architecture, layout, naming, or artifacts from it were consulted; this manifest is based only on the commissioned documents, `REVISION`, `NPP-E-scope.md`, `NPP-E.md`, and `spec/`.
