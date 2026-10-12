# The Swap — rebuilt transformation replaces the oracle

The rebuild meets acceptance items 1–8 (charter §5). The swap makes it the live module: it deletes
what the rebuild superseded, records each deletion, removes the working material, and lands the
three rebuild branches on `dev/18`. I make every file change. You run every git command.

---

## 1. Preconditions

| Check | State |
|---|---|
| `regression.sh --all` on the rebuild branches | 75/75 |
| Oracle comparison, declarations, construction | identical: 193 / 884 / 189 |
| Genesis dossier P0–P8 | admissible, 0 findings |
| Swap rehearsal: published identity, supersession agreement, single instance | all pass |
| Repos clean | `.github`, `transformation`, `software_governance` on `rebuild/transformation`; `protocol_compiler`, `protocol_runtime` on `dev/18` |
| Oracle tag `oracle/transformation` | local and on origin |

Before step A, push the three rebuild branches and `dev/18` of `protocol_compiler` and
`protocol_runtime`. That backup is what makes rollback possible.

---

## 2. Decisions to make first

The charter leaves six points open or self-contradictory. Each has a recommendation.

**D1. The parked dossiers.** §6 deletes every dossier but genesis. §6 "What stays" and §9 keep
`register_format` and `version_retirement` as evidence.
*Recommend: delete them with the rest.* The oracle tag `a1be97c` holds every dossier as it stood,
the parked ones included, and the tag never moves. Evidence held by a tag is still evidence.

**D2. `scripts/testbed/delivered_copies/`.** §6 deletes it. But four regression steps read it:
`differential`, `build_payloads`, `construction_acceptance`, and `priors.py`, which they share.
*Recommend: keep it as the testbed corpus.* Deleting it means deleting or rewriting four steps that
test the live module. §6 itself spares "any payload or harness" that something reads. Amend §6.

**D3. Acceptance after the oracle.** `scripts/rebuild/` runs the oracle beside the rebuild. When the
oracle is retired, items 2–4 can no longer be re-run.
*Recommend: run all three once more immediately before step A, record the results in the swap
commit message, then delete `scripts/rebuild/`.*

**D4. The working documents.** §6 deletes them once their rulings are restated.
*Recommend:*
- Restate in `DESIGN_LANGUAGE.md` and `CLAUDE.md` only the rulings that govern the live module:
  single instance, node keys follow their contract, `supersedes` as history, typed fields through
  `structure`, `x-vocab` parameters, data parts, the allocation of §6a, and the pinned baseline.
- Leave the history (charter §8, divergences from the oracle) to the tag and git.
- Move the open genesis findings, G-2, G-3, G-4 and G-8, from `GENESIS_TRIAGE.md` into the genesis
  `delivery.md` before deleting it, so they survive.

**D5. When to rename the repository.** §6a and §10a rename `transformation` to
`transformation_compilers` in the swap itself.
*Recommend: rename in a separate change, right after the swap is green.* The rename touches 20
files across `.github`, `snapshot_assembler`, `pgc_install` and the workspace `CLAUDE.md`. It also
touches the GitHub repository, the editable install and the oracle worktree. Kept apart, a failure
names its cause: a red regression after the swap is the swap's, and one after the rename is the
rename's.

**D6. The scope of the single-instance check.** §6 runs it on `transformation` from the swap, and on
every domain after the sweep.
*Recommend: transformation, artifact and lifecycle.* All three pass in the rehearsal, and the
rebuild superseded artifacts in each. Every other namespace joins after the sweep (§10 step 7).

---

## 3. Step A — the file changes (mine, on the rebuild branches)

All six decisions were approved as recommended. Step A is done; what it found beyond this plan is
in §3a.

**A1. Delete the 28 retired identities.** Each is entered in `rebuild-retirements.yaml` with its
`superseded_by`.
- `transformation`: 25 artifacts. Stood-down CC, CT, WF, STRUCTURE and VOCAB versions, among them
  WF_P2–P8 V0/V1 and WF_P7 V2.
- `software_governance`: `lifecycle::CONSTITUTION_CHANGE_MGMT_V0`,
  `lifecycle::CONSTITUTION_CONSTRUCTION_V0` and `artifact::VOCAB_DECLARATION_REPRESENTATION_V0`.

**A2. Delete the four V0 transform modules.** `ct_pure_{parse_registers,parse_prior_phases,
evaluate_rules,attribute_provenance}_v0.py`. Nothing names them once their artifacts are gone.

**A3. Merge the ledger.** Append the 28 entries to `.github/process/retired_identities.yaml`, with
the anchors expanded, and delete `notes/rebuild-retirements.yaml`. Point the checks that read the
deferred ledger at the one ledger.

**A4. Delete the working material.**
- `dossiers/`, except `genesis/` (D1).
- `scripts/rebuild/`, after D3.
- `doc/TRANSFORMATION_UNRAVEL.md`, `REGISTER_COVERAGE_VERIFICATION.md`, `REBUILD_CHARTER.md`,
  `REBUILD_DESIGN.md` and `GENESIS_TRIAGE.md`, after D4.

**A5. Restate, then rewrite.** Restate the rulings in `DESIGN_LANGUAGE.md` (D4). Rewrite the
repository's `CLAUDE.md` for the rebuilt module, then fix the stale table-reader docstring at
`transformation/design/evaluate/document.py:104`.

**A6. Expectations.** Update `expectations.yaml` and `RUNBOOK.md` for the counts the deletions move:
- implementation closure 41 → 37 transforms;
- supersession agreement and published identity, to their rehearsal figures;
- human-block artifacts;
- the transformation conformance line: 6 proven, 0 unproven.
Add `single_instance_check` as a regression step (D6). Every count I change, I state, with its cause.

**A7. Verify.**
- `regression.sh --all` passes.
- `implementation_closure` and `pgc_env_check` pass.
- The genesis dossier is still admissible, P0–P8.

**A8. Workspace records.** Mark the charter's acceptance complete in SOTU, and update memory.

---

## 3a. What step A found

- The final oracle comparisons, at rebuild commit `0c998ba`: 193 documents identical, 884 rules
  identical, 189 artifacts rendered alike.
- `INVARIANT_RENDER_INVENTS_NOTHING_V0` named the deleted attribution transform in its prose. It was
  never published, so it was corrected in place.
- The platform surface map was stale beyond the V0s. It was regenerated: 227 artifacts.
- Three tests depended on deleted identities: `differential.py` imported the V0 modules, and three
  corpus documents cited V0 identities as present. Each now names the live version.
- `construction_acceptance` reports a delivered design of a deleted artifact as RETIRED BY RECORD.
- `README.md` and `ARCHITECTURE.md` described the old module, and were corrected.
- `regression.sh` now rebuilds pristine and catches leaks. It runs every step in its own `TMPDIR` and
  fails if anything is left there (`temp_hygiene`); it clears bytecode; and the design baseline is
  kept under `traces/`, which `--all` clears. `test_examine` leaked a directory every run (270
  removed).
- The genesis dossier is re-pinned to `37968c3e…` (503); P0–P8 admissible; P7 and P8 regenerate
  identically.
- `regression.sh --all` from a clean workspace: 77/77.

## 4. Step B — git (yours)

On the three rebuild branches, after reviewing step A:

```
cd ~/protocol-governed-computing
for r in transformation_compilers .github software_governance; do git -C $r add -A; git -C $r commit -m "Swap: <summary>"; done
for r in transformation_compilers .github software_governance; do git -C $r push origin rebuild/transformation; done
```

Squash each into `dev/18` as one commit, in this order: the platform first, so the domain compiles
against it.

```
for r in software_governance transformation_compilers .github; do
  git -C $r checkout dev/18 && git -C $r merge --squash rebuild/transformation && \
  git -C $r commit -m "Rebuild of the transformation module, swapped in (charter §10 step 6)"
done
```

Then I run `regression.sh --all` on `dev/18` in all repos. Once it passes and you have checked it:

```
for r in transformation_compilers .github software_governance; do git -C $r push origin dev/18; done
for r in transformation_compilers .github software_governance; do git -C $r branch -m rebuild/transformation archive/rebuild-transformation; done
```

The oracle tag stays.

---

## 5. Step C — the rename (a separate change, D5)

Once the swap is green on `dev/18`:
- You: rename the GitHub repository; `mv transformation transformation_compilers`; re-run the
  editable install from the new path.
- Me: re-point the path uses (not the domain name, which stays `transformation`) in
  `regression.sh`, `release.sh`, `compose_release.py`, `assemble.sh` candidates, the snapshot
  profiles, `pgc_install`, the workspace `CLAUDE.md`, and memory.
- Then `pgc_env_check`, `regression.sh --all`, and your commit in each repository it touched.

---

## 6. Rollback

Before you push `dev/18` (step B), rollback is local:
`git -C <repo> reset --hard origin/dev/18` in `transformation`, `.github` and `software_governance`.
The rebuild branches are untouched and pushed. That reset is destructive, so you decide it.

After the push, rollback is a revert commit per repository. The oracle tag holds the old module
whole.

---

## 7. After the swap

- The sweep (charter §10 step 7): 22 stood-down artifacts in other domains, one change per domain,
  through the lifecycle, judged by the rebuilt module.
- Genesis G-2, G-3, G-4 and G-8, through the lifecycle.
- The genesis gates 0, 1 and 2, closed by you.
- The flaky first `--all`: the traps in `regression.sh` stay until it is caught or retired.
