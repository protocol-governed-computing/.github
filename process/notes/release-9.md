release 9 — the standard leaves the composition

Releases 2 through 8 named which version of eleven repositories went together. This one names ten,
and that is the whole of its content. **No governed artifact changed. The snapshot id is unchanged
from release 8** (`7b6f2699…`). What changed is what the composition is.

## The standard is a separate thing now

`dev/9` produced the first complete draft of the Open Protocol-Governed Computing Standard — 31
documents across seven normative parts, non-normative front matter, and an annex. It is no longer a
member of this composition. It has its own repository, its own history, and its own revision
identity: `draft-1`.

The reason is stated by the standard itself. Its Conformance Model says a revision "identifies the
family obligations against which discharge is evaluated. It does not identify an implementation
revision, a platform version, or a software release." But `standards/VERSION` read `9`, lockstepped
with ten repositories by this script — so the standard's revision number moved because a workload was
rebuilt. **A standard versioned by the cadence of the thing it governs is not independent of it**,
and the document that says so was in the repository doing it.

Removing `standards` from `REPOS` is therefore not tidying. It is the composition ceasing to version
something that was never part of it.

## Where the rest of it went

`standards` had accumulated four purposes. Three were not the standard:

- **the release process** — this script, the runbook, five closure checks, and the release notes —
  moved to `.github/process/`. The workspace root is not a repository, so these had no home and had
  been living in `standards` for that reason rather than for a good one.
- **the reference platform profile** moved to `.github/`. A profile shipped inside the standard is
  privileged by location, and the standard says no profile is privileged.
- **the session handoff and the ruling record** moved to `.github/doc/`. They mix rulings about the
  standard with findings about this implementation, which is the one combination a repository holding
  only the standard must not carry.

The namespace migration map moved to `software_governance/doc/`, beside the ruling it implements.

## Two corrections the standard forced

The reference profile was named `NORMATIVE_PLATFORM_PROFILE_BASELINE_V1`, and its second paragraph
denied what its third asserted: *"there is no single or minimal platform"* followed immediately by
*"this is the baseline profile: the smallest PNP."* It also claimed every other profile was a
variation on it — a derivation relation stated from the wrong end, since a derived profile names its
base and not the reverse.

It is now `REFERENCE_PLATFORM_PROFILE_V1`: the profile the reference realization is developed and
demonstrated against, which is what it always was. It declares `supersedes:
NORMATIVE_PLATFORM_PROFILE_BASELINE_V0` by exact identity. The differing names are immaterial —
supersession is a declared relation between identities, never derived from a naming convention. The
predecessor is retained and unreachable, because unreachable is not absent.

The profile also now declares its admissible kind vocabulary. The standard holds that no artifact
kind is required of a governed system, and that membership of a vocabulary is a profile's selection;
the sixteen canonical kinds had been held as working material with nowhere to be. They are a
profile's declaration, and this is the profile.

## What this release does not contain

No compiler change, no runtime change, no artifact change, no schema change, no behavior change.
Every domain rebuilds to the same snapshot it produced at release 8, and composition conformance
passes over the same 398 artifacts.

What this one moves is the composition's membership, and that seemed worth a marker of its own
rather than bundling it into whatever comes next. It is the last quiet release before that:
validating this implementation against the specification it was reverse-engineered into, and moving
1,407 namespace occurrences that the specification now says are wrong.
