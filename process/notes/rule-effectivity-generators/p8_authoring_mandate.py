"""Generate rule_effectivity's P8 from the P7 its generator wrote.

The mandate is mechanical: P7's new artifacts ordered by what each depends on. Vocabularies and
transforms first, the contracts that compose the transforms next, the workflows that run the
contracts last.

Run from the workspace root, after p7_design_intent.py:
    python .github/process/notes/rule-effectivity-generators/p8_authoring_mandate.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("p7", HERE / "p7_design_intent.py")
p7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p7)

D, CT, CC, WF, VOCAB, row, table = p7.D, p7.CT, p7.CC, p7.WF, p7.VOCAB, p7.row, p7.table
OUT = p7.ROOT / "dossiers/rule_effectivity/p8_authoring_mandate_transformation_design_v0.md"

JUDGE_OF = {"P0": "CC_JUDGE_DOCUMENT_V1", "P1": "CC_JUDGE_DOCUMENT_V1", "P3": "CC_JUDGE_AGAINST_COMPOSITION_V2"}


def interface(code: str, direction: str) -> str:
    core = p7.machine(p7.find(dict((n, o) for o, n in CT + CC)[code]))["core"]
    fields = dict(core.get("inputs" if direction == "INPUT" else "outputs") or {})
    names = [f"{f}:{spec.get('type', 'object')}" for f, spec in fields.items()]
    if code == "CT_PURE_EVALUATE_RULES_V1" or code.startswith("CC_"):
        names += ["rule_set_id:string"] if direction == "INPUT" else ["rule_set:string", "approval_standing:string"]
    return ", ".join(names)


def main() -> None:
    order, step = [], 0
    for code, *_ in VOCAB:
        step += 1
        order.append(row(1, step, D + code, "NEW", "design", "—"))
    for _, new in CT:
        step += 1
        order.append(row(1, step, D + new, "NEW", "design", "—"))
    parsers = ", ".join(D + n for _, n in CT)
    for _, new in CC:
        step += 1
        order.append(row(2, step, D + new, "NEW", "design", parsers))
    for p, n, o, v, *_ in WF:
        step += 1
        judge = JUDGE_OF.get(p, "CC_JUDGE_AGAINST_SNAPSHOT_V2")
        order.append(row(3, step, D + p7.wf_code(p, n, v), "NEW", "design", D + judge))

    critical = [row(i, D + c) for i, c in enumerate(
        ["CT_PURE_PARSE_REGISTERS_V1", "CC_JUDGE_AGAINST_SNAPSHOT_V2", "WF_P7_DESIGN_INTENT_ADMISSIBILITY_V3"], start=1)]
    summary = [
        row("REPLACE", 15, "Three transforms, three judging contracts and nine phase workflows, each stood down by its successor naming it; not scheduled, because nothing is authored for them."),
        row("EXTEND", 0, "Nothing is extended. Ten artifacts are re-pointed at a successor and keep their identity: the nine phase intents and the construction contract."),
        row("NEW", 18, "The successors: three transforms and one judging contract rendered from the design; two observing contracts and nine phase workflows reached by invoking the generator §16 of the design declares; and three vocabularies."),
    ]
    fields = [row(D + c, "design") for c in
              [c for c, *_ in VOCAB] + [n for _, n in CT] + [n for _, n in CC] + [p7.wf_code(p, n, v) for p, n, o, v, *_ in WF]]
    caps = [row(D + n, p7.NEW_SUMMARY[n], interface(n, "INPUT"), interface(n, "OUTPUT")) for _, n in CT + CC]

    sections = [
        ("1. Build Dependency Order", table("build_order", ["Wave", "Step", "Code", "Action (REPLACE, EXTEND, NEW)", "Subdomain", "Depends On"], order, "optional")),
        ("2. Critical Path", table("critical_path", ["Position", "Code"], critical, "optional")),
        ("3. Artifact Summary", table("mandate_artifact_summary", ["Action (REPLACE, EXTEND, NEW)", "Count", "Description"], summary)),
        ("4. Subdomain Field Declarations", table("field_declarations", ["Code", "Subdomain Field"], fields)),
        ("5. New Capabilities", table("new_capabilities", ["Code", "Purpose", "Inputs", "Outputs"], caps, "optional")),
        ("6. New Intents", table("new_intents", ["Code", "Purpose", "Workflow", "Inputs"], [], "optional")),
        ("7. Cross-Subdomain Notes", table("cross_subdomain_notes", ["Code", "Note"], [
            row(D + "CC_CONSTRUCT_ARTIFACTS_V0", "A build contract re-pointed at the new register reading. It keeps its identity and its own splitting of values inside cells."),
        ], "optional")),
    ]
    head = """# Stage 8 — Authoring Mandate: transformation / design
**Stage:** 8 — Authoring Mandate
**CR:** rule_effectivity
**Status:** DRAFT
**Feeds:** Artifact Authoring

Mechanical. Stage 7's assignments re-ordered into a build sequence; nothing added, nothing dropped.

---

"""
    gate = """

---

## Gate 2 — Mandate Approval

**Gate 2 closes here**, and it freezes scope before authoring begins. After it, any departure is an
Approved Deviation recorded in the authoring manifest — never a silent change.

What is frozen is eighteen artifacts, fifteen stood down and ten re-pointed, and what reaches them:

- **The form.** A phase document carries its header and registers in one YAML Machine block,
  registers as lists of rows keyed by column, values as strings. The reader returns the header,
  sections and registers the table reader returned. Templates and the seed-to-request projection
  write the new form. No reader of tables survives the change.
- **The identity.** One register schema per phase, `registry/schema/SCHEMA_REGISTERS_P<n>_<NAME>_V0.json`,
  holding its `$id`, the digest of the rule set its workflow seals, and its revision history. Its
  shape constraints admit any block until the design unravel fills them under the same `$id`.
  Emission seals the `$id` beside the rule set and refuses a sealed rule set whose digest the
  schema does not record.
- **The verdict.** The judging names the rule set that rendered it, and reports whether the
  document's approval holds under it. The check selects the workflow sealing the rule set a
  document names, and the current one, and reports both verdicts.
- **The standing.** The header names `rule_set`, `approved_under`, `standing` and, for a migrated
  document, `migrated_from`; the vocabularies close their values.

**The proof is inside the freeze, not beside it.** Every test document — the phase corpora, the
end-to-end payloads and the fixture dossiers — is converted once by the table reader and judged in
both forms by the same rule set. The findings are compared by rule, register, row and detail; any
difference is a regression, and the table reader is deleted only when there is none. Each new
transform carries the cases the design declares. A rule-set change without a recorded revision is
refused by emission, and a probe built to do that is part of this mandate.

Outside it: values inside cells keep their text form, the rules stay in their modules, construction
keeps its own splitting of values, and no dossier approved under v5 is read.

---

## Pipeline Provenance

| Stage | Output | Status |
|-------|--------|--------|
| Stage 7 — Design Intent | Inventory, replacements, generation provenance | COMPLETE — GATE 1 APPROVED |
| Stage 8 — Authoring Mandate | This document | PENDING GATE 2 APPROVAL |
"""
    OUT.write_text(head + "\n\n---\n\n".join(f"## {t}\n\n{b}" for t, b in sections) + gate, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
