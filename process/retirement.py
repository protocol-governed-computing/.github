"""Retention and retirement — read once, by every check that used to assume retention.

`retention.yaml` declares when a replaced version is retained (`4e` SU-7). `retired_identities.yaml`
records each deletion (`4e` SU-12): the identity, who decided, the determination that no retention
condition held, and the change that deleted it. This module reads both and refuses a malformed
record. It decides nothing about the composition; the checks do that.

`naming(frontmatter, retired)` answers which retired identities a live artifact names. A
`supersedes` entry is a successor naming its predecessor, and is allowed. A key is a place, and so
is a routing target under `next`: a workflow keeps a node's name and changes what it runs.
"""
from __future__ import annotations

from pathlib import Path

import yaml

PROCESS = Path(__file__).resolve().parent
RETENTION = PROCESS / "retention.yaml"
LEDGER = PROCESS / "retired_identities.yaml"

FIELDS = ("identity", "decided_by", "determination", "change")


def retention() -> dict:
    declared = yaml.safe_load(RETENTION.read_text(encoding="utf-8")) or {}
    for key in ("stable_baseline", "conditions"):
        if key not in declared:
            raise SystemExit(f"{RETENTION.name}: missing '{key}'")
    if not isinstance(declared["conditions"], list):
        raise SystemExit(f"{RETENTION.name}: 'conditions' must be a list")
    return declared


def retired() -> dict[str, dict]:
    """Every recorded deletion, by identity. A malformed or repeated record stops the check."""
    conditions = retention()["conditions"]
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or {}
    out: dict[str, dict] = {}
    for entry in ledger.get("retired") or []:
        missing = [f for f in FIELDS if not str(entry.get(f) or "").strip()]
        if missing:
            raise SystemExit(f"{LEDGER.name}: {entry.get('identity')} lacks {', '.join(missing)}")
        identity = entry["identity"]
        if "::" not in identity:
            raise SystemExit(f"{LEDGER.name}: {identity} is not a full identity")
        if identity in out:
            raise SystemExit(f"{LEDGER.name}: {identity} recorded twice")
        unaddressed = set(conditions) - set(entry.get("conditions_not_holding") or [])
        if unaddressed:
            raise SystemExit(f"{LEDGER.name}: {identity} does not address the retention "
                             f"condition(s) {', '.join(sorted(unaddressed))}")
        out[identity] = entry
    return out


def naming(frontmatter: dict, retired_ids: dict[str, dict], domain: str) -> set[str]:
    """The retired identities a live artifact names, by full identity or by its own domain's code."""
    by_code = {fqdn.split("::")[-1]: fqdn for fqdn in retired_ids if fqdn.split("::")[0] == domain}
    found: set[str] = set()

    def walk(value, under: str | None) -> None:
        if under in ("supersedes", "next"):
            return
        if isinstance(value, dict):
            for key, inner in value.items():
                walk(inner, key)
        elif isinstance(value, list):
            for inner in value:
                walk(inner, under)
        elif isinstance(value, str):
            if value in retired_ids:
                found.add(value)
            elif value in by_code:
                found.add(by_code[value])

    walk(frontmatter, None)
    return found
