"""Generate CLM CR-1 P8 authoring mandate from the P7 registers.

Kept as evidence for lesson 3 of `../clm-process-check.md`: the CLM CR-1 dossier's P8 was written
by this script, not by hand, and nothing in the phase checks records that. It is the script as it ran.

Do not run it to regenerate the dossier. It writes over the dossier file in place. P8 is
derived from P7, and running it re-derives the mandate from whatever P7 then holds.
"""
from pathlib import Path

from transformation.design.read import parse_text

CR = Path("/Users/bp/protocol-governed-computing/business_domains/causal_language_model/cr_dossiers/cr_01_model_response")
P7 = CR / "p7_design_intent_clm_model_response_v0.md"
OUT = CR / "p8_authoring_mandate_clm_model_response_v0.md"
SUB = "model_response"

from transformation.design.evaluate import ParsedDocument

_text = P7.read_text()
_h, _s, _r = parse_text(_text)
DOC = ParsedDocument(header=_h, sections=_s, registers=_r, raw=_text, path=str(P7))


def rows(name):
    block = DOC.register(name)
    if block is None or block.table is None:
        return []
    return [r for r in block.table.rows if "NONE IDENTIFIED" not in " ".join(r.values())]


def cell(row, prefix):
    return next((v.strip() for k, v in row.items() if k.startswith(prefix)), "")


new = [(cell(r, "Family"), cell(r, "Code"), cell(r, "Capability")) for r in rows("new_artifacts")]
codes = {c for _, c, _ in new}
fam = {c: f for f, c, _ in new}
deps: dict[str, list[str]] = {c: [] for c in codes}


def add(code, dep):
    if dep and dep != code and dep not in deps[code]:
        deps[code].append(dep)


structure = next(c for f, c, _ in new if f == "STRUCTURE")
for r in rows("cc_composition"):
    cc = cell(r, "CC Code")
    add(cc, cell(r, "Capability"))
    if cell(r, "Store") not in ("", "—"):
        add(cc, structure)
for r in rows("molecule_steps"):
    add(cell(r, "CT Code"), cell(r, "Target"))
ns = next(iter(codes)).split("::")[0]
for r in rows("execution_topology"):
    wf = cell(r, "Workflow")
    node = cell(r, "Runs") or cell(r, "Node")
    if node.startswith("EXIT"):
        continue
    add(wf, node if "::" in node else f"{ns}::{node}")
for r in rows("artifact_properties"):
    if cell(r, "Property").startswith("emit."):
        add(cell(r, "Artifact"), cell(r, "Value"))
for r in rows("rb_declarations"):
    rb = cell(r, "RB Code")
    add(rb, cell(r, "Binds WF"))
    add(rb, cell(r, "Storage Structure"))

# waves by longest path over authored dependencies
wave: dict[str, int] = {}


def depth(c):
    if c not in wave:
        wave[c] = 1 + max((depth(d) for d in deps[c] if d in codes), default=0)
    return wave[c]


for c in codes:
    depth(c)
ORDER = ["STRUCTURE", "VOCAB", "AC", "EV", "CT", "CC", "IN", "WF", "RB"]
declared = [c for _, c, _ in new]
ordered = sorted(codes, key=lambda c: (wave[c], ORDER.index(fam[c]), declared.index(c)))

# critical path: follow the deepest authored dependency back from the deepest artifact
tail = max(ordered, key=lambda c: (wave[c], -ordered.index(c)))
path = [tail]
while True:
    authored = [d for d in deps[path[-1]] if d in codes]
    if not authored:
        break
    path.append(max(authored, key=lambda d: (wave[d], -declared.index(d))))
path.reverse()

counts = {}
for f, _, _ in new:
    counts[f] = counts.get(f, 0) + 1

fields = {}
for r in rows("interface_fields"):
    fields.setdefault((cell(r, "Artifact"), cell(r, "Direction")), []).append(f"{cell(r, 'Field')}:{cell(r, 'Type')}")
admits = {}
for r in rows("execution_topology"):
    if cell(r, "Node Type") == "IN":
        admits[cell(r, "Node")] = cell(r, "Workflow")


def table(register, header, body, flags=""):
    out = [f"<!-- register:{register}{(' ' + flags) if flags else ''} -->", "| " + " | ".join(header) + " |",
           "|" + "|".join("-" * (len(h) + 2) for h in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in body] or ["| NONE IDENTIFIED |"]
    return "\n".join(out) + "\n"


waves = sorted(set(wave.values()))
lines = [f"""# Stage 8 — Authoring Mandate: causal_language_model / model_response

**Stage:** 8 — Authoring Mandate
**CR:** cr_01_model_response
**Status:** DRAFT
**Feeds:** Artifact Authoring

The {len(new)} artifacts Stage 7 designed, scheduled in dependency order. Nothing is added here and
nothing is dropped: the mandate orders the build, it does not decide it. Every artifact the design
reuses already exists in the composition and is named only as a dependency.

---

## 1. Build Dependency Order

""", table("build_order", ["Wave", "Step", "Code", "Action (REPLACE, EXTEND, NEW)", "Subdomain", "Depends On"],
           [(wave[c], i, c, "NEW", SUB, ", ".join(deps[c]) or "—") for i, c in enumerate(ordered, 1)]),
    f"""
Each artifact sits in the earliest wave its authored dependencies allow. Wave 1 holds everything that
depends only on the platform: the store declaration, the vocabulary, the actors, the business moments,
the six atoms, the entry points and the three contracts built from reused transforms alone. Wave 2 adds
the pass molecule and the contracts that address a store or a new atom. Wave 3 adds the response
molecule and the four staff workflows. The writing contract waits on the response molecule, the
submission workflow on the writing contract, and the runtime binding, which binds every workflow,
comes last.

---

## 2. Critical Path

""", table("critical_path", ["Position", "Code"], [(i, c) for i, c in enumerate(path, 1)]),
    f"""
The longest chain runs from the model's offer through both writing molecules, the writing contract
and the submission workflow to the runtime binding. No user prompt can be answered until it is
complete.

---

## 3. Artifact Summary

""", table("mandate_artifact_summary", ["Action (REPLACE, EXTEND, NEW)", "Count", "Description"],
           [("NEW", len(new), ", ".join(f"{counts[k]} {k}" for k in ["AC", "IN", "WF", "CC", "CT", "EV", "VOCAB", "RB", "STRUCTURE"])
             + " — every identity Stage 7 assigned")]),
    """
---

## 4. Subdomain Field Declarations

""", table("field_declarations", ["Code", "Subdomain Field"], [(c, SUB) for c in ordered]),
    """
---

## 5. New Capabilities

""", table("new_capabilities", ["Code", "Purpose", "Inputs", "Outputs"],
           [(c, cap, ", ".join(fields.get((c, "INPUT"), [])), ", ".join(fields.get((c, "OUTPUT"), [])))
            for f, c, cap in new if f == "CT"], flags="optional"),
    """
---

## 6. New Intents

""", table("new_intents", ["Code", "Purpose", "Workflow", "Inputs"],
           [(c, cap, admits[c], ", ".join(fields.get((c, "INPUT"), []))) for f, c, cap in new if f == "IN"], flags="optional"),
    """
---

## 7. Cross-Subdomain Notes

""", table("cross_subdomain_notes", ["Code", "Note"], [
        (f"{ns}::CC_CONFIRM_MODEL_STAFF_AUTHORIZED_V0", "Checks the staff member's asserted credentials against rules this design fixes, and grants nothing. Who is model staff is decided by the business's existing arrangements, which assert it through the ingress."),
        (f"{ns}::CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0", "Checks the customer against the requester's permitted customers as the business's existing arrangements assert them, and grants nothing."),
    ], flags="optional"),
    """
No model_response artifact writes into a store another subdomain owns.

---

## Pipeline Provenance

| Stage | Output | Status |
|-------|--------|--------|
| Stage 7 — Design Intent | p7_design_intent_clm_model_response_v0.md | GATE 1 APPROVED |
| Stage 8 — Authoring Mandate | This document | PENDING GATE 2 APPROVAL |
| Artifact Authoring | per build_order | PENDING |
"""]
OUT.write_text("".join(lines))
print(OUT.name, len(ordered), "steps,", len(waves), "waves; critical path", " -> ".join(c.split("::")[1] for c in path))
