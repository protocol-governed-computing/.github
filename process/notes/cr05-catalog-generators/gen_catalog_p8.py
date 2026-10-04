"""Generate book_library_mgmt cr_05_catalog P8 authoring mandate from its P7. Writes the dossier file.

Kept as evidence under ruling C1, with `gen_catalog_p7.py`. P8 adds nothing: it states the P7
inventory's amendments in the mandate's registers. Do not run it after P8 is approved.
"""
from __future__ import annotations

import sys
from pathlib import Path

W = Path("/Users/bp/protocol-governed-computing")
sys.path.insert(0, str(W / ".github/process/notes/cr05-catalog-generators"))
import gen_catalog_p7 as g  # noqa: E402

OUT = W / "business_domains/book_library_mgmt/cr_dossiers/cr_05_catalog/p8_authoring_mandate_book_library_mgmt_catalog_v0.md"


def main() -> None:
    art = {s: g.machine(s) for s in g.CCS + g.WFS + g.INS}
    g.apply_decisions(art)
    fields = "\n".join(f"| {g.q(s)} | catalog |" for s in g.CCS + g.WFS + g.INS)
    caps = "\n".join(f"| {g.q(s)} | {art[s]['core']['summary']} | {', '.join(art[s]['core']['inputs'])} | "
                     f"{', '.join(art[s]['core']['outputs'])} |" for s in g.CCS)
    intents = "\n".join(f"| {g.q(s)} | {art[s]['core']['summary']} | {g.q(art[s]['core']['workflow'])} | "
                        f"{', '.join(art[s]['core']['inputs'])} |" for s in g.INS)
    OUT.write_text(f"""# Stage 8 — Authoring Mandate: book_library_mgmt / catalog

**Stage:** 8 — Authoring Mandate
**CR:** cr_05_catalog
**Status:** DRAFT
**Feeds:** Construction

IN WHAT ORDER. Mechanically derived from the design; it reconciles with Stage 7 exactly and adds
nothing. Nothing is created, so nothing is scheduled: the twenty-six redeclared artifacts are authored
whole in their subdomain.

---

## 1. Build Order

<!-- register:build_order optional -->
| Wave | Step | Code | Action (REPLACE, EXTEND, NEW) | Subdomain | Depends On |
|------|------|------|-------------------------------|-----------|------------|

---

## 2. Critical Path

<!-- register:critical_path optional -->
| Position | Code |
|----------|------|

---

## 3. Artifact Summary

<!-- register:mandate_artifact_summary -->
| Action (REPLACE, EXTEND, NEW) | Count | Description |
|-------------------------------|-------|-------------|
| EXTEND | {len(g.CCS + g.WFS + g.INS)} | The catalog's six rule-applying contracts, its ten acts and their ten gates, redeclared whole so that the catalog holds every rule it applies and checks what it records. |

---

## 4. Field Declarations

<!-- register:field_declarations -->
| Code | Subdomain Field |
|------|-----------------|
{fields}

---

## 5. New Capabilities

<!-- register:new_capabilities optional -->
| Code | Purpose | Inputs | Outputs |
|------|---------|--------|---------|
{caps}

---

## 6. New Intents

<!-- register:new_intents optional -->
| Code | Purpose | Workflow | Inputs |
|------|---------|----------|--------|
{intents}

---

## 7. Cross-Subdomain Notes

<!-- register:cross_subdomain_notes optional -->
| Code | Note |
|------|------|
| {g.q('WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0')} | Superseded and not in force; left unchanged. It still names the rules its contract no longer takes, which a superseded act may. |
""")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
