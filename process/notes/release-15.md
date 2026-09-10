release 15 — a crash is not a refusal

This cycle changes nothing about what the platform determines. Every domain graph address in the
sealed composition is byte-identical to the one the preceding cycle produced; only the composition
ordinal differs, and it differs because the ordinal is carried in a constituent and constituents
enter the identity. Seven domains, 410 protocol artifacts, 595 constituents, composition conformance
PASSED over five rules.

Release 14 prepared eight repositories to become `pgc-*` distributions and recorded why an editable
install could not have told us whether they worked. This cycle performed the upload. Doing so put the
platform in front of someone holding only what PyPI serves, and that vantage point reported four
defects that every prior session had been unable to see — all of them at the one boundary where this
platform executes code it does not own.

## What was actually done

**Eight distributions published.** `pgc-governance`, `pgc-compiler`, `pgc-assembler`, `pgc-runtime`,
`pgc-inspector`, `pgc-transformation`, `pgc-workloads`, `pgc-domains`, each with a wheel and an
sdist under the public identity `v2`. Three carry a patch bump to 2.0.1 for the repairs below. A ninth,
`protocol-governed-computing`, pins all eight to one composition: PyPI prohibits the short name
`pgc`, so the composition carries the full project name and installs the command `pgc`.

**The assembler declared no dependencies and imported one.** `assembler/core.py` parses the claimed
profile's YAML block, on the path `verify_snapshot → verify_profile → _profile_declaration`. The
distribution declared `dependencies = []`. In this workspace and under `pgc` the import resolved
from elsewhere; installed alone, the `verify` subcommand raised `ModuleNotFoundError` instead of
answering. The defect was invisible to every install shape except the one an outside party would use.

**The runtime crashed where it was supposed to refuse.** CT and CS handler references are sealed at
compile time and loaded by `importlib` at execution. Neither import site was guarded. A handler
module the snapshot names but the environment lacks, or a domain's optional dependency that is not
installed, escaped as a bare `ModuleNotFoundError` — past the trace, past routing, to the caller.
Both sites now refuse, and the refusals use codes `SCHEMA_TRACE_EVENT_V0` already admits:
`CT_ARTIFACT_NOT_FOUND` where the snapshot names something absent, `CT_EXECUTION_FAILED` and
`CS_EXECUTION_FAILED` where the named thing is present and cannot run. No vocabulary was invented to
describe a failure the schema had no word for; the schema had the words.

**A refusal that reached the caller carried nothing.** `_execute_ct_step` ended
`except Exception: return "VIOLATION", {}`. Every CT refusal — including the ones this cycle added —
was converted to a status with no cause, leaving an operator a result and no account of it. Both
branches now render a structured refusal into the step result through one payload builder, which is
the channel the reach refusal has always used.

**Domain cryptography became an extra.** `pgc-domains` required `pycryptodome` unconditionally, so
installing the composition pulled cryptography for everyone. Exactly one capability transform needs it, and
the workspace has said since RI-0 that domain crypto is optional and never on the core compile path.
The declaration now matches the policy: `pip install "pgc-domains[blockchain]"`.

## Why this is not bookkeeping

Three of the four are the same defect. A guard existed a line away from where it was needed —
`execute_fn` was wrapped and `import_module` was not; the CS constructor and its `execute` call were
wrapped nowhere; the CT branch caught its exception and threw away what it caught. Nothing was
missing that anyone had failed to think of. The thinking was done and applied unevenly, and no test
could report it because no test asked the environment to be incomplete.

That is the shape release 12 recorded about demonstrations and release 14 recorded about editable
installs, arriving from a third direction. **A procedure that cannot fail is not evidence, and a
platform that fails in an undeclared way has not failed in a governed one.** This project's own
doctrine is that behaviour absent from the sealed state is refused rather than improvised. A
`ModuleNotFoundError` reaching a caller is improvisation by omission: the runtime met a condition its
governance had no word for, and said so in Python's words instead of its own.

The fix that matters least is the assembler's missing dependency. The fix that matters most is that
the runtime now answers, in its own declared vocabulary, when the environment cannot supply what a
sealed snapshot names.

## What this release is for

Release 13 made the composition citable. Release 14 made it buildable as an artifact. This one makes
it installable by a stranger, and reports what that stranger's vantage point found. The platform
determines exactly what it determined before; what changed is that its failures at the boundary are
now declared outcomes rather than exceptions, and that the family can be obtained by name.
