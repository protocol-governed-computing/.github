# End-to-End Runbook

A clean-slate build of the composition, then one check per domain.

The transformation phases are checked by a single script rather than one runbook line per phase.
The phase count grows; the runbook does not.

---

## Build

```bash
cd ~/protocol-governed-computing

~/protocol-governed-computing/protocol_compiler/compile.sh

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/conformance_workloads/workloads/collatz

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/transformation

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/snapshot_inspector

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/business_domains/ai_governance

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/business_domains/book_library_mgmt

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/business_domains/blockchain

~/protocol-governed-computing/snapshot_assembler/assemble.sh
```

Every domain that declares source must be compiled — the assembler refuses otherwise rather than
silently producing a smaller composition. If a compile step is skipped it names the command to run.

`book_library_mgmt` was missing from this list until a clean-slate run tripped over it: the domain had
source and no compiled output, the assembler refused, and every runtime check afterwards failed on a
snapshot that had never been written. A build list that omits a domain is indistinguishable from a
domain that declares no source, which is why the assembler names the command rather than proceeding.

## Check

Paste the whole block. It runs from a clean state every time --- the domain validations accumulate
into their data roots and refuse a root that already has their stores, so the block clears them
first.

```bash
# generators agree with what they produce
python ~/protocol-governed-computing/.github/process/governance_closure.py
python ~/protocol-governed-computing/.github/process/human_block_fidelity.py
python ~/protocol-governed-computing/transformation/scripts/emit_rule_sets.py --check
python ~/protocol-governed-computing/transformation/scripts/testbed/build_payloads.py --check
PYTHONPATH=~/protocol-governed-computing/snapshot_inspector \
  python ~/protocol-governed-computing/snapshot_inspector/scripts/author_transport_contracts.py --check
python ~/protocol-governed-computing/.github/process/frontmatter_fidelity.py

# the phase testbeds
python ~/protocol-governed-computing/transformation/scripts/testbed/meta_test.py
python ~/protocol-governed-computing/transformation/scripts/testbed/differential.py
python ~/protocol-governed-computing/transformation/scripts/testbed/e2e_phases_test.py
python ~/protocol-governed-computing/transformation/scripts/testbed/projection_test.py
python ~/protocol-governed-computing/transformation/scripts/testbed/construction_acceptance.py

# closure and environment
python ~/protocol-governed-computing/.github/process/implementation_closure.py
PYTHONPATH=~/protocol-governed-computing/snapshot_inspector \
  python ~/protocol-governed-computing/snapshot_inspector/scripts/testbed/test_inspector.py
python ~/protocol-governed-computing/.github/process/pgc_env_check.py

# execution — from empty data roots
rm -rf ~/protocol-governed-computing/data/collatz ~/protocol-governed-computing/data/ai_governance ~/protocol-governed-computing/data/book_library_mgmt \
       ~/protocol-governed-computing/data/book_library_mgmt_cr02 ~/protocol-governed-computing/data/blockchain

~/protocol-governed-computing/protocol_runtime/run.sh run --wf workload::WF_COLLATZ_CONJECTURE_V0 --payload ~/protocol-governed-computing/conformance_workloads/workloads/collatz/test_payloads/01_happy_path.json --data-root ~/protocol-governed-computing/data/collatz

mkdir -p ~/protocol-governed-computing/data/ai_governance/ai_governance/ai_licensing
cp ~/protocol-governed-computing/business_domains/ai_governance/testbed/agent_governance/seed_data/license_facts.json ~/protocol-governed-computing/data/ai_governance/ai_governance/ai_licensing/

~/protocol-governed-computing/protocol_runtime/run.sh run --wf ai_governance::WF_GOVERN_AGENT_ACTION_V0 --payload ~/protocol-governed-computing/business_domains/ai_governance/testbed/agent_governance/test_payloads/01_valid_standard_action.json --data-root ~/protocol-governed-computing/data/ai_governance

~/protocol-governed-computing/protocol_runtime/run.sh run --wf ai_governance::WF_PROVISION_AI_LICENSING_V0 --payload ~/protocol-governed-computing/business_domains/ai_governance/testbed/ai_licensing/test_payloads/provision_ai_licensing_payload.json --data-root ~/protocol-governed-computing/data/ai_governance

python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py --data-root ~/protocol-governed-computing/data/book_library_mgmt

python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation_cr02.py --data-root ~/protocol-governed-computing/data/book_library_mgmt_cr02

python ~/protocol-governed-computing/business_domains/blockchain/testbed/identity/execution_validation.py --data-root ~/protocol-governed-computing/data/blockchain

python ~/protocol-governed-computing/business_domains/blockchain/testbed/wallet/execution_validation.py --data-root ~/protocol-governed-computing/data/blockchain
```

**`frontmatter_fidelity` reads the assembled snapshot**, so it belongs after Build rather than before
it. Everything above it reads artifacts as authored and runs at any time.

**Both blockchain suites run into one root**, because a domain has one place its records live. Each
seeds people of its own so they never collide, and each refuses only its *own* stores being already
present rather than the whole root. Run identity first, then wallet; the result is
`<root>/blockchain/identity/` and `<root>/blockchain/wallet/` side by side, with one traces directory.

**The two catalog suites need separate roots.** Both write `book_library_mgmt/catalog`, so sharing one
would leave the second refusing a root the first had already filled.

**`implementation_closure`** checks both ends of the one pointer an artifact makes outside the
composition: a transform module nobody names, and an artifact naming a module that is not on disk.
Neither is visible to any phase rule, because neither has a design to judge.

**`construction_acceptance` covers two domains**, and reads them from different places on purpose.
`book_library_mgmt` is read from maintained fixtures, because its own harnesses judge those documents
and a delivered dossier goes inadmissible as the design language grows. `blockchain` is read from its
**delivered** dossiers, which works because rendering reads registers and never judges admissibility:
a dossier that would be refused at P7 today still determines exactly the artifacts it determined when
it was gated. `ai_governance` has no dossier, deliberately, so nothing determines its registry.
Pass dossiers as arguments with `--registry` to run one sequence by hand.

Every path is absolute; the `cd` is convenience only.

## Expected

Rows are in the order the block runs them.

| Check | Result |
|---|---|
| `governance_closure.py` | `GOVERNANCE CLOSURE PASSED` — every compiler handler is named by an invariant, and no layer is declared two ways |
| `human_block_fidelity.py` | `HUMAN BLOCK FIDELITY PASSED` — the prose beside a machine block declares nothing. A `RESTATED` line means delete the prose copy, never edit the machine block; a `SECTION` line means the section is named as if it states a rule. Doctrine in `software_governance/doc/HUMAN_BLOCK_TEMPLATE.md` |
| `emit_rule_sets.py --check` | every phase `OK` — the sealed rule set matches the declared one |
| `build_payloads.py --check` | `OK` — every phase payload matches the corpus document it is cut from. A `DRIFTED` line is a hand-edited payload; fix the source document and regenerate |
| `author_transport_contracts.py --check` | `OK` — every `si.` boundary contract matches the declaration that generates it. A `DRIFTED` line is a hand-edited artifact; fix the declaration, never the artifact |
| `frontmatter_fidelity.py` | `FRONTMATTER FIDELITY PASSED` — every authored Machine Block value survived compilation. The compiler may add; it may never overwrite |
| `meta_test.py` | `META PASSED` — every declared rule resolves to a check kind, and every kind is declared |
| `differential.py` | `DIFFERENTIAL PASSED` — the sealed rule set and the declared one agree on every corpus document |
| `e2e_phases_test.py` | `E2E PASSED` — every phase, both admissible and inadmissible, through the runtime |
| `projection_test.py` | `PROJECTION PASSED` — reproducible, general, and refusing an inadmissible prior |
| `construction_acceptance.py` | `93/93 artifacts reproduced across 2 domain(s) (0 field difference(s))` — `book_library_mgmt` from maintained fixtures, `blockchain` from its delivered dossiers |
| `implementation_closure.py` | `IMPLEMENTATION CLOSURE PASSED` — every transform module named by an artifact, every named module present |
| `test_inspector.py` | `PASSED: 121/121` |
| `pgc_env_check.py` | `PGC ENVIRONMENT CHECK PASSED` — no RI-0 dependency reachable |
| collatz | `SUCCESS`, `all_terminate: true` |
| govern agent action | `SUCCESS` |
| provision licensing | `SUCCESS` — the block clears `data/` first, so this is always a first run |
| `execution_validation.py` (catalog) | `23/23 criteria hold` — the catalog's nine workflows against CR-1's §15 |
| `execution_validation_cr02.py` (catalog) | `21/21 criteria hold` — CR-2's criteria, and proof the later change broke nothing |
| `execution_validation.py` (identity) | `15/15 criteria hold (2 not exercised)` — the remaining two are a timed test and the transaction half of the wallet claim, which needs a function that does not exist yet |
| `execution_validation.py` (wallet) | `9/9 criteria hold  (1 not exercised)` — the skip is a write through a consulted binding, which no act is authored to attempt |

### Choosing a store operation

`CS_MUTABLE_JSON_V0` publishes three ways to change a record, and picking the wrong one is how
blockchain/identity silently destroyed data for two change requests:

| | replace whole value | merge named fields |
|---|---|---|
| **by key** | `WRITE` | `UPDATE` |
| **by filter** | — | `UPDATE_WHERE` |

**Write what does not exist; update what does.** A step creating a record uses `WRITE`; a step
changing a record it did not create uses `UPDATE`, which sets the fields it is given and leaves the
rest alone. `WRITE` on an existing record destroys every field the caller did not supply, and it
succeeds — there is no error to notice.

`UPDATE` reports `VIOLATION` where the key is not held, so a step that changes a record can never
create one. `UPDATE_WHERE` addresses a *set*; reach for it only when you mean every record matching
a filter, never as a stand-in for a keyed update — that substitution is correct only while some
domain invariant guarantees the filter matches exactly one record, and it carries that invariant
wherever it is copied.

### Closed — identity rejections

A rejection stating no grounds was accepted for as long as one workflow carried both decisions: the
contract's steps are unconditional, so a grounds check added there would have refused acceptances
that correctly omit them. `cr_04_wallet` split the workflow into `WF_ACCEPT_ACTOR_V0` and
`WF_REJECT_ACTOR_V0`, and the reject path validates grounds unconditionally — which is the
distinction the business had already drawn by declaring two events rather than one carrying an
outcome field. The identity criteria now read `14/14`.

Worth keeping for what it demonstrates: the rule was declared at P5 §5 (*A rejection states
grounds*) and recorded at P7 as `EV_ACTOR_REJECTED_V0 | grounds_required | YES`, and realised
nowhere. Every document passed. A property is a true statement about an artifact no step consults,
which no phase rule can see and only an execution validation catches.

Both transformation verdicts complete with `Status: SUCCESS`. An inadmissible document is a correct
judgement, not a failed execution — `VIOLATION` there would mean the phase itself is broken.

`differential.py` must be run from the `transformation` directory: it imports `design_baseline` from
`e2e_phases_test`, which sits beside it. `--check` on the emitter is the cheap half of what the
differential proves — it compares counts without booting a snapshot, so it catches a rule added and
never re-emitted in a second rather than a minute.

## The catalog subdomain

`book_library_mgmt/catalog` is constructed and runs. Its nine workflows are exercised by one script,
which is the **only check in this runbook that proves the catalog does anything**:

```bash
python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py 
```

It dispatches real workflows through `protocol_runtime` against a fresh temp data root and asserts the
CR's §15 acceptance criteria — 23 of them — reading the stores it wrote rather than the status it was
handed. State accumulates deliberately across scenarios, so the order is part of the evidence and the
run is not idempotent; that is why it starts from an empty data root every time.

It takes an optional snapshot path, defaulting to `~/protocol-governed-computing/snapshot`.

**To inspect the catalog it built**, give it somewhere to keep the stores:

```bash
python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py --data-root ~/protocol-governed-computing/data/catalog_inspect
```

```
  23/23 criteria hold

  stores kept at .../data/catalog_inspect/book_library_mgmt/catalog
    book_identity_registry.jsonl 2 entries (json lines)
    books.json                   2 record(s)
    catalog_operations.jsonl     15 entries (json lines)
    copy_barcode_registry.jsonl  4 entries (json lines)
    physical_copies.json         4 record(s)
```

The path must be empty or absent — the run accumulates state across scenarios, so starting it over a
previous run's stores proves nothing. It refuses rather than emptying a directory you named.

**Two file formats, and the extension tells you which.** `CS_MUTABLE_JSON_V0` writes one JSON
object keyed by store key (`.json`); `CS_REGISTRY_V0` and `CS_APPENDONLY_JSONL_V0` write JSON Lines
(`.jsonl`). Use `jq` on the former, `jq -s` on the latter.

`CS_REGISTRY_V0` §12 declares its path a **JSONL registry file (append-only)**, and its runtime
writes one — the catalog had named those two stores `.json`, so the extension advertised a document
that could never be parsed as one. P7's `STORE_PATH_FORMAT_MISMATCH` now refuses it: a store's path
must carry the extension its storage capability writes. The correspondence is declared in
`STORE_FORMATS` in the phase's rules, because a CS states its format only in the prose of its
configuration schema and nothing machine-readable carries it.

**Why it exists, and why the other checks do not replace it.** Every document check passed —
P0–P8 ADMISSIBLE, `tc construction check` 100%, construction acceptance at 0 field differences,
conformance PASSED, `e2e_phases_test.py` green — against a composition whose stores held binding
expressions instead of records, because every cross-step source had been authored without its
`results.` root and the runtime read each one as a literal string. Document checks prove a design
determines its artifacts. Only execution proves the artifacts do anything.

Individual workflows can be dispatched directly. The payloads live in the testbed and are **derived**
from the validation suite's own helpers — regenerate rather than hand-edit them:

```bash
cd ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog
python emit_payloads.py          # -> test_payloads/01..09

P=~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/test_payloads

~/protocol-governed-computing/protocol_runtime/run.sh run \
  --wf book_library_mgmt::WF_REGISTER_BOOK_V0 \
  --payload $P/01_register_book.json \
  --data-root ~/protocol-governed-computing/data/book_library_mgmt
```

They are a **sequence against one data root**, not nine independent cases — `01` registers the book
the rest operate on, and the numbering is the order to run them in. All nine return `SUCCESS` in
order from an empty data root. Run out of order a payload is still well-formed and its workflow
refuses it, which is the catalog behaving correctly rather than a broken payload.

| Payload | Workflow |
|---|---|
| `01_register_book` | `WF_REGISTER_BOOK_V0` |
| `02_register_physical_copy` | `WF_REGISTER_PHYSICAL_COPY_V0` |
| `03_update_bibliographic_information` | `WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0` |
| `04_search_catalog` | `WF_SEARCH_CATALOG_V0` |
| `05_retrieve_book_details` | `WF_RETRIEVE_BOOK_DETAILS_V0` |
| `06_retire_physical_copy` | `WF_RETIRE_PHYSICAL_COPY_V0` |
| `07_reinstate_physical_copy` | `WF_REINSTATE_PHYSICAL_COPY_V0` |
| `08_retire_book_record` | `WF_RETIRE_BOOK_RECORD_V0` |
| `09_reinstate_book_record` | `WF_REINSTATE_BOOK_RECORD_V0` |

The five stores land under `<data-root>/book_library_mgmt/catalog/`: `books.json`,
`physical_copies.json`, `catalog_operations.jsonl`, `book_identity_registry.jsonl`,
`copy_barcode_registry.jsonl`. Inspect those to see what a workflow actually did — the status alone
does not tell you.

The nine are `WF_REGISTER_BOOK_V0` · `WF_REGISTER_PHYSICAL_COPY_V0` ·
`WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0` · `WF_RETIRE_BOOK_RECORD_V0` · `WF_RETIRE_PHYSICAL_COPY_V0` ·
`WF_REINSTATE_BOOK_RECORD_V0` · `WF_REINSTATE_PHYSICAL_COPY_V0` · `WF_SEARCH_CATALOG_V0` ·
`WF_RETRIEVE_BOOK_DETAILS_V0`. Every one takes `staff_credentials`, `authorization_rules` and
`staff_id`: authorization is read, never granted, so the caller supplies both the credentials and the
rules they are checked against. `execution_validation.py`'s `book_payload()` is the worked example.

### A change request that amends rather than authors

A defect correction creates nothing: it re-renders an artifact the composition already holds. The
registers that name what a change *creates* are therefore empty — `provisional_codes` at P5,
`new_artifacts` at P7, `build_order` and `critical_path` at P8 — and all four are optional so that
an amend-only change is expressible. Emptiness there is not an omission; it is the shape.

What carries the change instead:

- **P7 `existing_inventory`** — the artifact with Action `EXTEND`. This is what construction reads:
  `render_all` renders what the mandate schedules **and what the design amends**, because an
  extended artifact is never a build step (`BUILD_CODE_ALREADY_EXISTS` refuses to schedule an
  identity the composition already holds).
- **P7 `cc_composition` / `step_bindings`** — the artifact's full composition, not the delta. An
  amended artifact is rendered *whole*, so every step it keeps must be restated exactly. Anything
  the design does not state is dropped.
- **The `Summary` cell of the inventory row** becomes the emitted artifact's summary. Write what the
  artifact *is*, carried over unchanged — a summary describing the change silently rewrites it.

```bash
tc construction check --snapshot ~/protocol-governed-computing/snapshot $D
#   AMENDMENT NARROWS lists facts that exist now and the design does not state. For an amendment
#   some narrowing is the point — a replaced input is a lost fact — so read the list rather than the
#   count. It cannot tell a renamed step from a deleted one: renaming one step reported 13 facts
#   lost where 1 had changed. Prefer the smallest diff.
```

Verify by diffing the emitted artifact, not by trusting the measurement. CR-3's correction is two
lines; anything larger meant the design restated something imperfectly.

### After editing a governance artifact, recompile every domain

A platform artifact is copied into **every** domain's compiled output — the governance surface is
compiled per domain and the assembler collects them all. `compile.sh` alone updates only `platform`,
and the artifact index may resolve the identity to any copy.

**The copies can disagree and nothing checks.** After adding an operation to `CS_MUTABLE_JSON_V0`,
five copies existed with two different operation sets; the assembler reported
`conformance PASSED (5 rules over 376 artifacts)` and `round-trip verify: OK`. The published
capability surface kept reporting the old set while the edited artifact sat correctly compiled under
`platform`.

Run the full Build list at the top of this file after any governance edit. A single domain compile is
never enough — but the assembler now checks: `verify_snapshot` compares every copy of an artifact
identity by `content_hash` and refuses the composition when they disagree, naming the identity and
the copies. A partial recompile fails the build instead of sealing a snapshot that answers from
whichever copy the index happened to resolve.

## Constructing a design into artifacts

The loop to run after **any** edit to a dossier's P7 or P8. Skipping a step leaves the snapshot
describing a design that no longer exists:

```bash
D=~/protocol-governed-computing/business_domains/book_library_mgmt/cr_dossiers/cr_01_catalog

tc construction check $D --snapshot ~/protocol-governed-computing/snapshot
#   100% or the design does not determine its artifacts, AND no amendment narrows what it replaces.
#   `--snapshot` is what checks the second: an artifact inventoried EXTEND is rendered whole and
#   replaces its predecessor, so a design stating only the delta deletes the rest — at 100%
#   completeness, because completeness never looks at what already exists. Without the flag that
#   check does not run and says so.

python - <<'EOF'                               # construct + persist, through the governed workflow
import sys; W = "/Users/bp/protocol-governed-computing"
for r in ("software_governance", "business_domains", "transformation", "conformance_workloads"):
    sys.path.insert(0, f"{W}/{r}")
from pathlib import Path
from runtime import api
D = Path(W) / "business_domains/book_library_mgmt/cr_dossiers/cr_01_catalog"
r = api.run_workflow(
    wf_fqdn="transformation::WF_CONSTRUCT_ARTIFACTS_V0",
    payload={"design_text": (D / "p7_design_intent_book_library_mgmt_catalog_v0.md").read_text(),
             "mandate_text": (D / "p8_authoring_mandate_book_library_mgmt_catalog_v0.md").read_text(),
             "threshold": 100.0},
    snapshot_root=f"{W}/snapshot", data_root=f"{W}/data/transformation")
print(r.status, (r.surface or {}).get("written"), "artifact(s)")
EOF

# A new CT is a protocol artifact AND a Python implementation. Construction renders the first; the
# second is hand-authored at
# business_domains/<domain>/implementation/capability_transforms/atoms/<code_lower>.py
# with a callable `execute(inputs, context)` raising CTExecutionError. A CT whose module is missing
# returns nothing, its contract yields VIOLATION, and every check above this line still passes.

# promote — a separate, deliberate act; construction writes to data/, not into the domain
rsync -rc ~/protocol-governed-computing/data/transformation/construction/registry/catalog/ \
         ~/protocol-governed-computing/business_domains/book_library_mgmt/registry/catalog/

# Scoped to book_library_mgmt: its DOSSIERS list names the two catalog change requests, because
# acceptance compares a render against artifacts that already exist and only that domain was ever
# hand-authored. A domain emitted by `tc construction emit` is covered by `tc construction check`
# instead. Pass dossiers as arguments to widen it.
python ~/protocol-governed-computing/transformation/scripts/testbed/construction_acceptance.py

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/business_domains/book_library_mgmt
~/protocol-governed-computing/snapshot_assembler/assemble.sh

python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py
python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation_cr02.py
```

One validation per change request, and both are run: `execution_validation.py` asserts CR-1's
criteria and proves the later change broke nothing, `execution_validation_cr02.py` asserts CR-2's and
proves it did something. Neither substitutes for the other — every one of CR-1's criteria was
satisfied before CR-2's work existed.

Construction writes into `data/transformation/construction/registry/` through
`CS_TEXT_ARTIFACT_V0 WRITE_ALL`. **Promotion into the domain is a separate act** — a `tc construction
build` CLI was added once and removed, because it duplicated a governed path with an ungoverned one.

`construction_acceptance.py` compares what the designs render against what the registry holds, and it
renders the **sequence** — every dossier in order, a later change overriding an earlier one artifact
by artifact, exactly as promotion did. Expect **51/52 at 0 field differences**: the one miss is the
hand-authored `STRUCTURE_BUILD_BOOK_LIBRARY_MGMT_CONFIG_V0`, which no design renders.

Pass dossiers explicitly to check a different sequence, and `--registry <path>` to compare against a
registry other than the domain's. Rendering one dossier alone is only correct while one change
request owns the domain: an earlier design still renders the artifacts a later one amended, so the
differences it reports are history rather than defects.

## Serving a domain over HTTP

A domain that declares `TI_`/`TE_` artifacts is reachable from outside. The transport adapter is
domain-neutral and is **pointed** at everything; a client is a launcher, a binding table and static
files, and it lives with the domain it serves.

```bash
# blockchain/identity — three operations, one route
~/protocol-governed-computing/business_domains/blockchain/client/serve.sh
#   -> http://127.0.0.1:8000        PGC_HTTP_PORT overrides

# collatz — one operation, one route per operation
~/protocol-governed-computing/conformance_workloads/workloads/collatz/client/serve.sh

# snapshot inspection — eighteen operations sharing one route
~/protocol-governed-computing/snapshot_inspector/client/serve.sh
```

Read the startup banner before believing anything. It prints the `snapshot_id` the process booted
against and the operations that snapshot declares — **the boundary is read once, at startup**, so a
snapshot rebuilt afterwards is invisible until the process restarts. A stale server is then a
one-line comparison rather than an inference.

### The data root is an instance, not an interface

`PGC_DATA_ROOT` names *which business instance* is being driven. Nothing in the runtime or the
transport engine ties it to a user interface, and the layout is identical whatever drove it —
the domain is namespaced inside the root, not by it:

```
<data_root>/blockchain/identity/{actors.json,contact_address_registry.jsonl,actor_occurrences.jsonl}
<data_root>/traces/blockchain/<WF>/<trace_id>/<trace_id>.jsonl
```

**Point the client and the CLI at the same root.** `blockchain/client/serve.sh` defaults to
`data/blockchain`, which is what the CLI runner at the foot of this file uses, so a person registered
from a web form is the person a CLI decision is about. A root per client is two disjoint worlds that
happen to share a snapshot — you cannot then verify what you registered, and the composition's claim
that a boundary reaches the same acts the CLI does goes untested.

```bash
# register over HTTP, then decide from the CLI against the same instance
curl -s -X POST http://127.0.0.1:8000/blockchain -H 'Content-Type: application/json' \
  -d '{"operation":"blockchain.register_actor","params":{"name":"Ada","contact_address":"ada@example.test"}}'
cat ~/protocol-governed-computing/data/blockchain/blockchain/identity/actors.json
```

**Concurrency, stated so it is not discovered.** A mutable store is written atomically per file
(temp → `fsync` → `os.replace`), so a torn or half-written store is impossible, and every operation
takes a per-file lock around load → modify → save. **That lock is a `threading.Lock` in a
process-local registry** (`CS_MUTABLE_JSON_V0/impl/executor.py:20-28`), so it serializes concurrent
requests *inside one server* and does nothing at all *between processes*. A CLI run and a running
web server writing one store in the same instant can therefore still lose an update — which is
precisely the pairing a shared data root invites. Drive one at a time, or accept the race
knowingly.

### The two binding shapes

`bindings/http.json` is adapter-owned data, not an artifact. Either form is governed — an operation
resolves only if the snapshot holds a matching TI/TE pair.

```jsonc
{ "method": "POST", "path": "/collatz", "operation": "collatz.compute" }              // one act, one place
{ "method": "POST", "path": "/blockchain", "operation_in_body": true,                 // a family, one place
  "namespace": "blockchain." }
```

The namespace on the second is an **admission constraint the adapter checks textually**, never a
dispatcher it branches on. Each identity still resolves against its own TI/TE pair. Use it when a
domain expects to add acts: a new function then adds a name, not a place, and no caller learns a new
address. `si.catalog` submitted to `/blockchain` is refused `OPERATION_NOT_ADMITTED`.

### Exercising it

```bash
B=http://127.0.0.1:8000
curl -s -X POST $B/blockchain -H 'Content-Type: application/json' \
  -d '{"operation":"blockchain.register_actor","params":{"name":"Ada","contact_address":"ada@example.test"}}'
```

Expected, for blockchain/identity against a fresh `PGC_DATA_ROOT`:

| call | HTTP | Result Class |
|---|---|---|
| `register_actor` | 200 | `SUCCESS` — `sequence_number: 1`, evidence `trace:…` |
| the same registration again | 200 | `SUCCESS` — `sequence_number: 2`, one actor, no failure |
| `register_actor` with no `contact_address` | 400 | `VIOLATION` — `INPUT_MISSING`, names the field |
| `accept_actor` | 200 | `SUCCESS` — `ACTOR_ACCEPTED`, `grounds: null` |
| `accept_actor` again | 400 | `VIOLATION` — the act ran and refused |
| `reject_actor` with no `grounds` | 400 | `VIOLATION` — `INPUT_MISSING`, names `grounds` |
| `reject_actor` on an unregistered address | 404 | `NOT_FOUND` |
| an act the domain does not offer | 404 | `OPERATION_NOT_FOUND` |
| an identity outside the route's namespace | 400 | `OPERATION_NOT_ADMITTED` |

**Rows 3 and 5 are both `VIOLATION` and mean different things** — the boundary could not read the
request, versus the act ran and refused. The governed Result Class set has no kind for the second,
so they are told apart by `errors[]`: `INPUT_MISSING` naming a field, against `handler status
VIOLATION`. A client that switches on Result Class alone will conflate them.

The `evidence` reference resolves under the `/traces` mount, so the record of what happened is one
request away from the answer reporting it. `/snapshot` mounts the sealed composition read-only.

### Serving the compiled workflow beside the form

Because `/snapshot` is mounted, a screen can show the DAG the runtime actually traverses, live from
the sealed composition:

```html
<img src="/snapshot/behavior_logic/<domain>/<WF_CODE>/<WF_CODE>.projection.png"
     onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
```

Live means never stale — rebuild the snapshot and the picture changes with it; clean it and the
image fails soft rather than showing something that was true once. Both identity screens carry one,
as does collatz. Note what the pairing demonstrates on the verify screen: `blockchain.accept_actor`
and `blockchain.reject_actor` render the **same** graph, because two public names reach one workflow
and each boundary declaration holds its own constants.

### What a client may not do

The page collects, sends, and renders. It holds no rule, validates nothing, and keeps no copy of
what the business holds. Concretely, in `blockchain/client/web/`: **no `required` attribute and no
`type="email"`** — those are client-side judgement, and the platform's refusal naming the field is
what the caller should see instead. A control may carry an *operation identity* (accept and reject
are two acts, so each is an `<option>` value); it may not carry a mapping, a schema, or a default.
The one thing a page may keep is what the person just typed, to save retyping it — nothing the
business does may depend on it being there.

Legacy RI-0 clients at `~/pgs/pgs_blockchain/.../testbed/static/` are **read-only and lifted one
way**. Their form structure and CSS salvage; their field names, their `/api/run` endpoint and their
response envelope do not. A client that POSTs a workflow identity violates
`OPERATION_IDENTITY_INDEPENDENCE`.

## Adding a new domain

There are two paths, and the difference is not the build — it is whether the artifacts already
exist. Once a domain has a `registry/`, adding it to the composition is the ordinary loop at the
top of this file: `compile_domain.sh`, then `assemble.sh`. Nothing below changes that.

### The simple path — artifacts you already have

`ai_governance` and the catalog's first change request were both added this way, and it is correct
whenever the artifacts are authored rather than derived:

```bash
W=~/protocol-governed-computing
# 1. Hand-author registry/<subdomain>/{actors,intents,workflows,capability_contracts,...}
# 2. Hand-author registry/structures/STRUCTURE_BUILD_<DOMAIN>_CONFIG_V0.md — without it the
#    compiler cannot discover the domain at all.
$W/protocol_compiler/compile_domain.sh $W/business_domains/<domain>
$W/snapshot_assembler/assemble.sh
```

**What it costs.** No design means no P7, and no P7 means none of the composition-integrity rules
ever judges the domain — not `STEP_INTERFACE_CONFORMS`, not `STEP_INPUT_UNBOUND`, none of them.
`ai_governance` carried `timestamp: "{{timestamp}}"` in three audit contracts for as long as it has
existed: an unresolvable literal in every audit record it ever wrote, invisible because nothing was
looking. Correcting it meant hand-editing sealed artifacts, because there was no design to correct
and regenerate from.

**And the build manifest is the part that drifts.** `book_library_mgmt`'s described itself as the AI
governance domain and listed that domain's subdomains — copied from a sibling and never corrected,
because no rule governs a hand-written file. `tc construction emit` generates it from the mandate.

### The governed path — a domain the pipeline produces

Everything below is about *producing* the artifacts. A domain established by a change request has
no baseline to extend and no registry to write into, and the order matters; every deviation this
workspace has tried failed at a step that looks unrelated. Steps 1 and 5 exist only because a
dossier is involved — they say nothing about the build.

```bash
W=~/protocol-governed-computing
DOM=blockchain                                   # the namespace; artifacts are <DOM>::
CR=$W/business_domains/$DOM/cr_dossiers/cr_01_identity

# 1. Pin the baseline the CR is validated against — the composition BEFORE this domain exists.
mkdir -p $CR && tc baseline show --snapshot $W/snapshot > $CR/baseline.json

# 2. Author P0 (problem statement + seed), project P1, author P2..P8.
tc phase project --phase p1 --out $CR/p1_change_request_${DOM}_identity_v0.md $CR/p0_seed_${DOM}_identity_v0.md
tc phase check --phase p7 --snapshot $W/snapshot \
   --prior p5=$CR/p5_*.md --prior p6=$CR/p6_*.md $CR/p7_*.md

# 3. Emit. Writes the artifacts AND the domain's build manifest, which no phase designs —
#    every field of it is compiler configuration, so it is generated from the mandate.
tc construction emit $CR --root $W/business_domains/$DOM

# 4. Compile the domain against the compiled platform surface, then assemble.
$W/protocol_compiler/compile_domain.sh $W/business_domains/$DOM
$W/snapshot_assembler/assemble.sh

# 5. Re-pin and re-approve — the composition now contains the domain, so the old pin is stale.
tc baseline show --snapshot $W/snapshot > $CR/baseline.json
for p in p2 p3 p4 p5 p6 p7 p8; do tc baseline approve --phase $p --by "$USER" $CR/baseline.json; done
```

**Re-validating the CR after step 4 will fail**, with `NEW_CODE_ALREADY_EXISTS` on every artifact.
That is correct: a change request that says *create these* cannot be judged against a composition
that already holds them. To re-check or amend it, roll the composition back first:

```bash
rm -rf $W/business_domains/$DOM/{registry,snapshot} && $W/snapshot_assembler/assemble.sh
```

Editing an artifact already sealed into a released composition is a `REPLACE` in a governed change
request, not an edit. Rolling back is legitimate only while the domain is unreleased.

**The assembler refuses a domain that declares source with no compiled output**, so never write the
build manifest before the artifacts — `tc construction emit` writes both together for that reason.

### What a new domain needs beyond its artifacts

- **A capability the substrate does not offer** is a platform change, not a domain one. Declare the
  CS in `software_governance/capability_side_effects/registry/`, implement it under
  `implementation/<CODE>/runtime.py` with `execute(*, op, payload)`, and add it to
  `allowed_capability_side_effects` in `INVARIANT_CS_SURFACE_CLOSED_V1` — the platform surface is
  closed and the compiler refuses an undeclared capability. `core.category` must be one of
  `storage · external · ephemeral · execution_gateway · inspection`.
- **A capability the workflow reaches must be bound for it** in the domain's `RB_`. A capability
  composed into a contract and bound for nobody produces no handler, no trace entry and no error —
  the step is simply never reached.
- **A new CT is two things**: the artifact construction renders, and a Python implementation at
  `business_domains/<domain>/implementation/capability_transforms/atoms/<code_lower>.py`. Either half
  can go missing without anything failing until the step runs, which is what
  `.github/process/implementation_closure.py` exists to catch — run it after adding or retiring a transform.

## Running a domain's workflows from the CLI

`run.sh` boots the snapshot but needs `PGC_IMPL_ROOTS` for domain implementations. Driving the
runtime directly is what the testbeds do:

```bash
python - <<'EOF'
import json, sys, pathlib
W = "/Users/bp/protocol-governed-computing"
sys.path[:0] = [f"{W}/software_governance", f"{W}/business_domains"]
from runtime import api
P = pathlib.Path(f"{W}/business_domains/blockchain/testbed/identity/test_payloads")
for f in sorted(P.glob("*.json")):
    r = api.run_workflow(wf_fqdn="blockchain::WF_REGISTER_ACTOR_V0",
                         payload=json.loads(f.read_text()),
                         snapshot_root=f"{W}/snapshot", data_root=f"{W}/data/blockchain")
    print(f"{f.name:<36} {r.status}")
EOF
```

Stores land under `data/<domain>/<domain>/<subdomain>/`, traces under
`data/<domain>/traces/<domain>/<WF>/<trace_id>/*.jsonl`.

**Read the trace before theorising.** A `CC_START` event carries the contract's *resolved* inputs,
which is the only place a binding that resolved to `None` is visible — the artifact, the workflow
and the contract all look correct. `CC_STEP` names each capability as it runs; a step missing from
the trace entirely was never bound.

## Clean rebuild from source

The strongest check there is. Every other suite judges the composition; this judges whether the
composition can be *rebuilt* — and a `snapshot_id` that comes back unchanged proves the whole thing
derives from committed source with nothing on disk carrying state nobody can regenerate.

Safe only when every repo is clean. Both generated registries — `blockchain/registry`, written by
`tc construction emit`, and `ai_governance/registry`, hand-authored — are **tracked**, so the wipe
below removes nothing that is not derivable.

```bash
W=~/protocol-governed-computing

# 0. Refuse to start if anything is uncommitted. What is not in git is about to be lost.
for r in transformation business_domains standards software_governance snapshot_inspector \
         protocol_runtime protocol_compiler snapshot_assembler conformance_workloads; do
  printf "%-24s %s\n" $r "$(git -C $W/$r status --short | wc -l | tr -d ' ')"
done

# 1. Wipe every build output: the assembled snapshot, each domain's compiled projections, runtime data.
rm -rf $W/snapshot $W/data \
       $W/software_governance/snapshot $W/snapshot_inspector/snapshot $W/transformation/snapshot \
       $W/business_domains/*/snapshot $W/conformance_workloads/workloads/*/snapshot

# 2. Platform first — a domain resolves its references against the compiled governance surface.
$W/protocol_compiler/compile.sh

# 3. Every domain in the composition. Omitting one assembles it from stale output that no longer exists.
for d in $W/transformation $W/snapshot_inspector $W/conformance_workloads/workloads/collatz \
         $W/business_domains/ai_governance $W/business_domains/book_library_mgmt \
         $W/business_domains/blockchain; do
  $W/protocol_compiler/compile_domain.sh $d
done

$W/snapshot_assembler/assemble.sh
```

**The snapshot_id must be the one you started with.** It is content-derived over each domain's
projection hashes with provenance, timestamps and paths excluded, so a rebuild of unchanged sources
reproduces it exactly. A different id means either a source changed or something in the build is
not deterministic — and the second is the one worth chasing.

Then the full surface:

```bash
cd $W/transformation
for s in meta_test e2e_phases_test differential projection_test construction_acceptance; do
  python scripts/testbed/$s.py
done
python scripts/emit_rule_sets.py --check          # sealed rule sets match their declaration

CR=$W/business_domains/blockchain/cr_dossiers/cr_01_identity
tc phase meta                                     # rule/mechanism parity
tc baseline verify --snapshot $W/snapshot $CR/baseline.json
tc construction check $CR --snapshot $W/snapshot
```

and execute two domains against the snapshot just built, which is the only evidence that a
composition assembled from nothing still runs:

```bash
python - <<'EOF'
import json, sys, pathlib
W = "/Users/bp/protocol-governed-computing"
sys.path[:0] = [f"{W}/software_governance", f"{W}/business_domains", f"{W}/conformance_workloads"]
from runtime import api
P = pathlib.Path(f"{W}/business_domains/blockchain/testbed/identity/test_payloads")
REG = "blockchain::WF_REGISTER_ACTOR_V0"
DEC = "blockchain::WF_RECORD_VERIFICATION_DECISION_V0"
for f in sorted(P.glob("*.json")):
    wf = REG if f.name[:2] in {"01", "02", "03", "07"} else DEC
    r = api.run_workflow(wf_fqdn=wf, payload=json.loads(f.read_text()),
                         snapshot_root=f"{W}/snapshot", data_root=f"{W}/data/blockchain")
    print(f"{f.name:<36} {r.status}")
print(api.run_workflow(wf_fqdn="workload::WF_COLLATZ_CONJECTURE_V0", payload={"numbers": [27]},
                       snapshot_root=f"{W}/snapshot", data_root=f"{W}/data/workload").status)
EOF
```

Run this before a release, after any change to the compiler or assembler, and whenever a build
starts behaving differently on two machines.

## After changing a phase's rules

The rule set is declared in `transformation/design/<phase>/rules.py` and **sealed** into that phase's
workflow artifact. Editing the declaration alone leaves `tc phase check` and the governed workflow
evaluating different rule sets:

```bash
python ~/protocol-governed-computing/transformation/scripts/emit_rule_sets.py           # re-seal
~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/transformation
~/protocol-governed-computing/snapshot_assembler/assemble.sh
python ~/protocol-governed-computing/transformation/scripts/testbed/build_fixtures.py   # derive
python ~/protocol-governed-computing/transformation/scripts/testbed/build_payloads.py
```

`--check` first will name the drifted phase. Fixtures and payloads are **derived from the live
dossier** — never hand-edit one; change the dossier or the mutator in `build_fixtures.py`. A derived
fixture cannot go stale silently: the derivation raises rather than producing a wrong fixture.

A new rule needs four things, or it is untested: the check in `design/checks.py`, the `Rule` in the
phase's `rules.py`, a mutator plus `FIXTURES` row in `build_fixtures.py`, and entries in
`build_payloads.py` (source, priors, register key), `e2e_phases_test.py` (`CASES`) and
`differential.py` (`PRIORS_BY_DOCUMENT`).

## Why the phase check is a script

`e2e_phases_test.py` executes each compiled workflow through `protocol_runtime` and asserts the verdict,
finding count and rules evaluated. It is not the same evidence as the differential:

- `differential.py` drives the capability transforms directly — it proves the rule sets and the
  check logic, and nothing about workflow wiring.
- `e2e_phases_test.py` boots the assembled snapshot and dispatches workflows — it proves the IN/WF/CC
  wiring, node bindings and routing.

A workflow that bound `$.capability_result.header` across nodes passed the differential and failed
immediately under the runtime, because workflow nodes read the intent payload rather than a previous
node's result. Both checks are needed; neither substitutes for the other.

## Faster loops

```bash
tc phase list
tc phase check --phase p0 <seed.md>
tc phase check --phase p1 <register.md>
tc phase check --phase p2 <register.md> --snapshot ~/protocol-governed-computing/snapshot

cd ~/protocol-governed-computing/transformation && python scripts/testbed/differential.py
```

From P2 a phase also needs its **priors**, or the handoff between phases goes unchecked:
P1←p0 · P2←p1 · P3←p2 · P4←p3 · **P5←p0** · P6←p5 · P7←p5+p6 · P8←p7.

**P5 reads the seed, not P4.** It transforms P4's consolidation rather than restating it, so there
is no row-level obligation to check against P4 — but the subdomain purpose is authored once at P0,
has no register to travel in through P1–P4, and reappears at P5. Without the seed, P5 cannot tell an
inherited purpose from a second author's paragraph.

A phase that is *projected* rather than authored is written by the compiler, and the prior is judged
before it is projected:

```bash
D=~/protocol-governed-computing/business_domains/book_library_mgmt/cr_dossiers/cr_02_catalog
tc phase project --phase p1 $D/p0_seed_book_library_mgmt_catalog_v0.md \
   --out $D/p1_change_request_book_library_mgmt_catalog_v0.md --force
```

A seed carrying an open blocking clarification is refused rather than projected. A question found
while restating the seed amends the seed and is projected again — it never enters at P1.

```bash
D=~/protocol-governed-computing/business_domains/book_library_mgmt/cr_dossiers/cr_01_catalog
tc phase check --phase p7 $D/p7_design_intent_book_library_mgmt_catalog_v0.md \
   --prior p5=$D/p5_business_intent_book_library_mgmt_catalog_v0.md \
   --prior p6=$D/p6_governance_intent_book_library_mgmt_catalog_v0.md \
   --snapshot /tmp/pgc_cr01_design_baseline
```

A CR is judged against the composition it was **designed** against, never one that already contains
its own output — every identity it assigns would collide. Once a CR is promoted, checking its P7
against the live snapshot reports its own codes as already existing; that is the rule working, not a
defect.

CR-2's baseline is reconstructed from the commit at which its design was complete and its
construction had not run, which is exact and does not drift:

```bash
S=$(mktemp -d); OUT=/tmp/pgc_cr02_design_baseline
(cd ~/protocol-governed-computing/business_domains && git archive 32e5774 book_library_mgmt) | tar -x -C $S
~/protocol-governed-computing/protocol_compiler/compile_domain.sh $S/book_library_mgmt
W=~/protocol-governed-computing; rm -rf $OUT
PGC_SOURCE_ROOTS="$W/software_governance/snapshot/compiled:$W/conformance_workloads/workloads/collatz/snapshot/compiled:$W/business_domains/ai_governance/snapshot/compiled:$W/snapshot_inspector/snapshot/compiled:$W/transformation/snapshot/compiled:$S/book_library_mgmt/snapshot/compiled" \
  PGC_SNAPSHOT_OUT=$OUT ~/protocol-governed-computing/snapshot_assembler/assemble.sh
```

Expect **336 artifacts** — the composition of 345 less the nine CR-2 authored. CR-1's baseline is
rebuilt from *current* sources minus `book_library_mgmt`, so it moves when any other domain does;
CR-2's is anchored to a commit and does not. That baseline is reproduced on demand by
`design_baseline()` in `e2e_phases_test.py`, and is stale whenever a source domain has been recompiled
since it was built.

`tc phase check` is the right loop while authoring a document. Phases through P1 judge a document
alone and need no snapshot; from P2 a phase grounds claims against the composition, so `--snapshot`
is required for its grounding rules to be checked at all — without it they report that they could
not run rather than quietly passing. The differential
needs an assembled snapshot and compares the sealed rule set against the declared one.
