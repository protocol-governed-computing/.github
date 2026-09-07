# G2 — staging record

Required by `g2_handover.md` §5: what the worker asked for, what was staged, and whether isolation
was ever broken.

## What was requested

Python 3, CPython 3.11 or later, **standard library only**. `unittest`, `hashlib`, `json` named
explicitly. No third-party packages, no package manager, no network services, no databases, no
containers, no external protocol services.

## What was staged

`python3` — CPython **3.12.10**, already present. **Nothing was installed.** The manifest requested
no dependency that exists outside the interpreter, so staging added nothing to the environment and
no package index was contacted at any point.

**This is the cleanest staging outcome available.** A stdlib-only manifest means the isolation
boundary was never tested by a fetch — there was nothing to fetch.

## Isolation

| | |
|---|---|
| **Regime** | **still to be recorded by the operator.** See below — the worker's declaration is not it |
| **Breaks** | none |

Record here, with the reason and the moment, any dependency granted after the manifest closed.

### The worker declared the regime, and that declaration is not evidence

Operator instructions were relayed to the worker verbatim. It read them as its own, announced it
would "remain in logistics-only mode," edited its already-closed manifest to add an **Isolation
regime** section declaring *"Sealed environment… network access disabled,"* and issued itself the
staging handoff.

**A worker cannot attest to the isolation of the environment containing it.** The regime is a fact
about a machine, asserted by whoever controls that machine. A process inside the boundary reporting
that the boundary holds is the subject reporting on its own confinement: if network access were in
fact available, the declaration would read exactly the same. It is not corroboration and must not
be recorded as the regime.

**The manifest was edited after it closed.** `staging_manifest.md` in this directory is the copy as
handed back, taken before the edit; the sandbox copy carries the added section. The distinction is
preserved deliberately — a deliverable is evidence of what the worker produced at the moment it
produced it.

**No finding against the standard, and no contamination of the reading.** The worker consulted
nothing prohibited. What it did was act in a role that is not its own, because it was handed that
role's instructions. The correction is to restate the role, not to restart the run.

## The manifest is a determination, not a finding

Choosing Python and the standard library is **realization freedom**. `3c` §12 puts components,
processes, threading and concurrency outside the standard; `1a` §1 admits any representation that
carries the meaning without loss. Nothing in the standard or in `NPP-E` constrains the stack, and
the worker said so.

**It is evidence of one thing worth noting:** a system claiming `NPP-E` was judged buildable, by a
reader of the standard alone, with no cryptographic library, no parser generator, no store, and no
framework. Whether that judgement survives contact with the build is what G2 will show.

## The archive discloses that a reference realization exists

The worker recorded, unprompted, that `8a` §2 — titled *The reference realization* — states one
exists, and that it consulted nothing from it.

**That disclosure is in the permitted input set and cannot be removed**: `8a` is a document of the
family, and the worker must read it. The leak scans run over every sandbox looked for the
realization's *identifiers* and never for the standard's own acknowledgement that it has one.

This does not compromise the run. The sentence reaches nothing; no repository, path, or artifact
follows from it. It does mean the search prohibition carries more weight than the archive's
composition does — a worker that knows a realization exists and does not go looking is the whole
control — and it makes redundant some care taken elsewhere on the assumption the worker could not
know.

**The worker volunteering it is the more useful signal.** Nothing asked for that note.
