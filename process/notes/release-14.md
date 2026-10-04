release 14 — an editable install is not evidence that a wheel works

This cycle changes nothing about what the platform determines. Every graph address in the sealed
composition is byte-identical to the one `v2` published; only the composition ordinal differs. What
changes is whether the platform can be *obtained* by someone who was not given a workspace — which
is the same kind of precondition release 13 established for naming it.

The work was packaging: eight repositories become `pgc-*` distributions at 2.0.0 under the public
identity `v2`, and a `pgc` meta-package installs the family as one composition. Distribution names
take the `pgc-` prefix; import names are unchanged.

## What was actually done

**The acceptance criterion changed, and that is the finding.** The toolchain had been developed
against editable installs, which resolve imports from a shared development environment and a
repository root. A wheel has neither. Green-field wheel installation was therefore made the gate,
and it immediately reported defects that every prior working session had been unable to see:

- **A package list eight packages behind the tree**, among them `compiler.governance_engine` and
  every assertion handler under it. Replaced with discovery rather than enumeration.
- **Undeclared dependencies.** `transformation` named one of four; `click`, `pyyaml` and the runtime
  were satisfied only by the shared venv, so a wheel failed on import three separate ways.
- **A dependency naming a pre-rename distribution**, which would have resolved to nothing.
- **The composition ordinal unreachable from a wheel.** `VERSION` is a repo-root declaration and a
  wheel has no repo root, so the value is now staged into the package at build time by an in-tree
  backend.
- **Run-time content living outside the package.** The P0–P8 phase templates sat beside the package
  rather than inside it. They are what the pipeline reads to derive registers and rule sets, so a
  wheel that omitted them installed a pipeline that could not run.

**The in-tree backend had to travel in the sdist.** `python -m build` builds the wheel *from* the
sdist, in an isolated directory. `_build_hook.py` was not shipped, so the sdist step succeeded and
the wheel step failed with `Backend '_build_hook' is not available` — a failure invisible until the
first build performed the way a stranger would perform it. `VERSION` is shipped for a worse reason:
omitting it did not fail, because the hook skips a file that is not there. It produced a wheel whose
ordinal was silently absent.

**The declarations are deliberately not shipped.** The compiler resolves the governance surface from
`PGC_PLATFORM_ROOT` — fail-hard, cwd-independent. A registry inside a wheel would be a second
governance surface competing with the repository's, and a build could then be governed by a stale
copy. Installing the toolchain is one of two steps, and `pgc` says so when it finds no anchor.

## Why this is not bookkeeping

Every defect above was present, latent, and passing. The suite ran, the tools worked, and the
composition rebuilt bit-for-bit — while the artifact a stranger would receive was broken in five
ways. None of these were caught by testing more carefully. They were caught by changing what
counted as installed.

That is the same distinction release 12 recorded about demonstrations and this project keeps
arriving at from different directions: **a procedure that cannot fail is not evidence.** An editable
install cannot fail on a missing package, an undeclared dependency, or content outside the package,
because the repository is still there to supply what the artifact does not. The defects were not
hiding. Nothing was looking that could have seen them.

## What this release is for

Release 13 made the composition citable — nameable by someone who was not part of building it.
This one makes it obtainable by them. A DOI names what was examined; a wheel is how someone gets a
copy that runs. The project now has both, and neither required changing what the platform does.
