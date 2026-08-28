#!/usr/bin/env bash
#
# PGC release cut — the standard process, parameterised by release ordinal.
#
#   development on dev/<N>  →  archive history as tag history-<N>
#                           →  open dev/<N+1> from it  →  declare VERSION <N+1>
#
#   and, only when publishing:
#
#   dev/<N>  →  orphan commit  →  force onto main  →  tag <PUBLIC_VERSION>  →  push main + tag
#
# CUTTING A CYCLE AND PUBLISHING ONE ARE DIFFERENT ACTS. A cycle is cut every time development
# closes on it. A composition is published when someone decides to publish it — release 12 was cut
# and deliberately not published, because the composition it would have sealed was the one release
# 11 already sealed. So publication is opt-in: `--publish`, and never a side effect of cutting.
#
# THE REMOTES CARRY ONE COMMIT AND ONE TAG. They are a publication surface, not a development
# mirror: no dev branches, no release-<N>, no history-<N>. Everything this script archives, it
# archives locally. `history-<N>` is what makes that safe — it pins the cycle tip permanently, and
# it is the reason the 2026-08-28 rewrite lost nothing when every remote branch was deleted.
#
# The release ordinal is read from `.github/VERSION`; the public identity from
# `.github/PUBLIC_VERSION`. Neither is edited here, and neither is derived from the other.
#
# PGC versions the COMPOSITION, not each repo independently: all repos release together and the
# governance closure forces lockstep, so one monotonic integer names which composition a repo
# belongs to. The single declaration is each repo's `VERSION` file — pyproject and the Python
# version constants derive from it. Never hand-edit a version anywhere else: step 4 writes it,
# because ten repos declaring one composition is one act, and ten hand-edits is ten chances to
# leave a repo declaring the release it was just cut out of.
#
# Read this before running it. It pushes and deletes remote refs.
#
# Usage:
#   release.sh              preflight, then cut the cycle (local only — touches no remote)
#   release.sh --publish    cut the cycle AND publish it under .github/PUBLIC_VERSION
#   release.sh --check      preflight only — changes nothing, safe to run any time
#   SKIP_BUILD=1 release.sh skip the clean-rebuild gate (only when iterating; never to release)
#
# The squash message is CONTENT that changes every cycle; this script is PROCESS that does not. It
# therefore lives in `.github/process/notes/release-<N>.md`, read by convention — there is no
# flag, because a flag would be a second way to supply it, and a message typed at a prompt is
# neither reviewable in a diff beforehand nor recoverable afterwards. Write the notes file, commit
# it, run the script. The notes ship inside the release they describe, since `.github` is one of
# the squashed repos, and they accumulate as a per-release history on main.
#
set -euo pipefail

CHECK_ONLY=0
PUBLISH=0
case "${1:-}" in
  "")        ;;
  --check)   CHECK_ONLY=1 ;;
  --publish) PUBLISH=1 ;;
  -h|--help) sed -n '2,45p' "$0"; exit 0 ;;
  *) echo "unknown argument: $1 (usage: release.sh [--check|--publish])" >&2; exit 2 ;;
esac

WORKSPACE="$HOME/protocol-governed-computing"

# The release ordinal is DERIVED, never declared here. `VERSION` is the single declaration of which
# composition a repo belongs to, and this script already refuses any repo whose VERSION disagrees —
# so a second copy of that number kept here was a second declaration of the same fact, maintained by
# hand, with nothing to catch it going stale. It did: release 11 was cut and these constants were
# not bumped, so the next preflight expected every repo to be on dev/11 and reported eighty failures
# describing a release that had already shipped.
#
# Deriving it removes the step that can be missed. `.github/VERSION` is the reference copy because
# `.github` is one of the released repos and carries the notes; the other nine are still compared
# against it, so lockstep is checked exactly as before — what is no longer checkable is whether the
# reference itself is wrong, and there was never anything to check it against. The branch and tag
# preconditions catch a VERSION bumped without a cycle behind it.
RELEASE="$(cat "$WORKSPACE/.github/VERSION" 2>/dev/null || true)"
case "$RELEASE" in
  ''|*[!0-9]*) echo "cannot derive the release ordinal: $WORKSPACE/.github/VERSION is '${RELEASE:-<missing>}', expected a positive integer" >&2; exit 2 ;;
esac
NEXT=$((RELEASE + 1))

# The PUBLIC IDENTITY — declared, never derived. `.github/publications.md` carries the relation
# between successive identities and the reason each was issued; this file carries the current one.
#
# It is NOT computed from $RELEASE. The two counters advance on different occasions: the ordinal
# every cycle, the identity only on publication. An offset between them would be an inferred
# relation, which `4e` §9 refuses — a revision is declared rather than inferred from a number.
#
# The operator declares the next identity by editing this file BEFORE running --publish. The script
# never invents one: publishing under an identity nobody declared is the act the whole scheme exists
# to prevent. Forgetting to bump it is caught by the tag-collision check in preflight.
PUBLIC="$(cat "$WORKSPACE/.github/PUBLIC_VERSION" 2>/dev/null || true)"
if [ "$PUBLISH" -eq 1 ] || [ "$CHECK_ONLY" -eq 1 ]; then
  case "$PUBLIC" in
    v[0-9]|v[1-9][0-9]*) ;;
    *) echo "cannot read the public identity: $WORKSPACE/.github/PUBLIC_VERSION is '${PUBLIC:-<missing>}', expected v<positive integer>" >&2
       [ "$PUBLISH" -eq 1 ] && exit 2 ;;
  esac
fi
PUBLICATIONS="$WORKSPACE/.github/publications.md"

# What the build gate builds and claims. Named rather than defaulted, because neither tool has a
# default and neither should: no profile is privileged (6a §11) and no platform is minimal (6a §8).
GATE_STRUCTURE="STRUCTURE_BUILD_PLATFORM_CONFIG_V1"
GATE_PROFILE="REFERENCE_PLATFORM_PROFILE_V1"

# The composition — every repo that compiles, assembles, is assembled into a snapshot, reads one,
# or transforms one into the next. `snapshot_inspector` joined at release 3 (it missed release 2
# because it was not yet a git repo); `transformation` joins at release 4 and correctly
# carries no earlier tag. `.github` was excluded while it held only the org profile page; it now
# also holds the snapshot assembly contract that `snapshot_assembler` and `protocol_runtime` cite
# as the contract they implement, so it carries composition surface and releases in lockstep.
REPOS="software_governance conformance_workloads business_domains protocol_compiler \
protocol_runtime snapshot_assembler protocol_transport snapshot_inspector \
transformation .github"

# One notes file per cycle, kept whether or not the cycle is published. It was formerly the squash
# commit message, and is now simply the record of what a composition was — which is what it always
# actually was. A cycle that is cut and never published still has a notes file, and that file is
# how anyone later reconstructs what happened between two published identities.
NOTES="$WORKSPACE/.github/process/notes/release-$RELEASE.md"
MSG="$([ -f "$NOTES" ] && cat "$NOTES" || true)"

cd "$WORKSPACE"

# ---------------------------------------------------------------------------
# 0. Preflight
#
#    Every check reports rather than aborting, so one run surfaces ALL problems instead of
#    making you rediscover them one at a time. Nothing here mutates anything.
# ---------------------------------------------------------------------------
FAILED=0
fail() { printf "  FAIL  %s\n" "$*"; FAILED=$((FAILED + 1)); }
ok()   { printf "  ok    %s\n" "$*"; }

if [ "$PUBLISH" -eq 1 ]; then
  echo "Preflight for cycle $RELEASE — PUBLISHING as $PUBLIC"
else
  echo "Preflight for cycle $RELEASE — cut only, no remote will be touched"
fi
echo

echo "Release notes:"
if [ -z "$(printf '%s' "$MSG" | tr -d '[:space:]')" ]; then
  fail "no release notes — write $NOTES"
elif printf '%s' "$MSG" | grep -q "<what changed\|<state here"; then
  fail "release notes are still the template — the squash commit is the only durable record on main"
else
  ok "release notes from $NOTES ($(printf '%s\n' "$MSG" | wc -l | tr -d ' ') lines)"
fi
echo

echo "Per-repo state:"
for r in $REPOS; do
  [ -d "$r/.git" ] || { fail "$r is not a git repo"; continue; }

  [ -z "$(git -C "$r" status --porcelain)" ] || fail "$r has uncommitted changes"

  cur="$(git -C "$r" branch --show-current)"
  [ "$cur" = "dev/$RELEASE" ] || fail "$r is on '$cur', expected 'dev/$RELEASE'"

  [ -f "$r/VERSION" ] && [ "$(cat "$r/VERSION")" = "$RELEASE" ] \
    || fail "$r/VERSION is '$(cat "$r/VERSION" 2>/dev/null)', expected '$RELEASE'"

  # NO origin/dev check. Development is local: the remotes carry a published commit and its tag,
  # nothing else. `history-$RELEASE` is what preserves the cycle, and it is a local tag.

  # A pre-existing history tag would make step 2 fail partway through the ten.
  git -C "$r" rev-parse --verify -q "refs/tags/history-$RELEASE" >/dev/null 2>&1 \
    && fail "$r already has tag history-$RELEASE"

  if [ "$PUBLISH" -eq 1 ]; then
    git -C "$r" fetch -q origin 2>/dev/null || fail "$r cannot reach origin"

    # The identity must not already name something. This is the check that catches the likeliest
    # mistake by far — running --publish without having declared a new PUBLIC_VERSION first.
    git -C "$r" rev-parse --verify -q "refs/tags/$PUBLIC" >/dev/null 2>&1 \
      && fail "$r already has tag $PUBLIC — declare the next identity in .github/PUBLIC_VERSION"
    git -C "$r" ls-remote --tags origin "$PUBLIC" 2>/dev/null | grep -q . \
      && fail "$r origin already has tag $PUBLIC"
  fi

  # dev/$NEXT must not exist yet, locally or remotely.
  git -C "$r" rev-parse --verify -q "dev/$NEXT" >/dev/null 2>&1 && fail "$r already has dev/$NEXT"
done
[ "$FAILED" -eq 0 ] && ok "all $(echo $REPOS | wc -w | tr -d ' ') repos on dev/$RELEASE, clean, no tag collisions"

# The identity must be declared before it is issued, not merely well-formed. A number in a file
# that `publications.md` does not mention has not been declared — same rule the standard applies
# to itself: a revision appearing in VERSION and not in revisions.md has not been declared.
if [ "$PUBLISH" -eq 1 ]; then
  echo
  echo "Publication:"
  if grep -q "\`$PUBLIC\`" "$PUBLICATIONS" 2>/dev/null; then
    ok "$PUBLIC is declared in .github/publications.md"
  else
    fail "$PUBLIC is not declared in .github/publications.md — record what it supersedes first"
  fi
fi
echo

echo "Build gate:"
if [ "${SKIP_BUILD:-0}" = "1" ]; then
  printf "  SKIP  clean rebuild (SKIP_BUILD=1) — do not release on an unverified build\n"
else
  # Snapshot dirt BEFORE building, so the post-build check attributes only what the build
  # actually changed. Comparing raw dirtiness would blame the build for pre-existing edits.
  # Temp files, not an associative array — macOS ships bash 3.2, which has no `declare -A`.
  DIRT_DIR="$(mktemp -d)"
  trap 'rm -rf "$DIRT_DIR"' EXIT
  for r in $REPOS; do git -C "$r" status --porcelain > "$DIRT_DIR/$r.before"; done

  # EVERY domain in the composition, or the gate is not a clean-room build: an omitted domain is
  # assembled from whatever stale output happens to be on disk, and its compile against the
  # current governance closure is never proven.
  # Discovered the way the assembler discovers them — a domain is anything declaring a
  # STRUCTURE_BUILD_*_CONFIG. This list was hand-enumerated and had drifted: `book_library_mgmt`
  # and `transformation` were missing, so the gate compiled four domains, assembly refused, and the
  # "EVERY domain" comment above was false. An enumerated list of everything is a list that goes
  # stale the next time a domain is added.
  DOMAIN_ROOTS=("$WORKSPACE/software_governance")
  for d in "$WORKSPACE"/conformance_workloads/workloads/* "$WORKSPACE"/business_domains/*; do
    [[ -d "$d" ]] && DOMAIN_ROOTS+=("$d")
  done
  DOMAIN_ROOTS+=("$WORKSPACE/snapshot_inspector" "$WORKSPACE/transformation")

  BUILDABLE=()
  for root in "${DOMAIN_ROOTS[@]}"; do
    [[ -d "$root/registry" ]] || continue
    [[ -n "$(find "$root/registry" -maxdepth 3 -name 'STRUCTURE_BUILD_*_CONFIG_V*.md' -print -quit 2>/dev/null)" ]] || continue
    BUILDABLE+=("$root")
    rm -rf "$root/snapshot/compiled"
  done
  rm -rf snapshot

  BUILD_OK=1
  # The gate NAMES what it builds. compile.sh and assemble.sh have no defaults: a platform is
  # whatever a build config declares (6a §8) and a snapshot must name the profile it claims
  # (1b §11). Naming them here is the act those rules require, not boilerplate.
  protocol_compiler/compile.sh "$GATE_STRUCTURE" >/tmp/pgc_rel_build.log 2>&1 || BUILD_OK=0
  if [[ $BUILD_OK -eq 1 ]]; then
    for root in "${BUILDABLE[@]}"; do
      [[ "$root" == "$WORKSPACE/software_governance" ]] && continue   # compile.sh builds the platform
      protocol_compiler/compile_domain.sh "$root" >>/tmp/pgc_rel_build.log 2>&1 || { BUILD_OK=0; break; }
    done
  fi
  if [[ $BUILD_OK -eq 1 ]] && PGC_SNAPSHOT_PROFILE="$GATE_PROFILE" snapshot_assembler/assemble.sh >>/tmp/pgc_rel_build.log 2>&1; then
    ok "clean rebuild + assemble + composition conformance"
    grep -E "^\[conformance\]|snapshot_id" /tmp/pgc_rel_build.log | sed 's/^/        /'
  else
    fail "clean rebuild failed — see /tmp/pgc_rel_build.log"
    tail -5 /tmp/pgc_rel_build.log | sed 's/^/        /'
  fi
  # Compiled output is gitignored; if that ever changes, the release would carry build noise.
  for r in $REPOS; do
    git -C "$r" status --porcelain | diff -q - "$DIRT_DIR/$r.before" >/dev/null 2>&1 \
      || fail "$r was dirtied BY THE BUILD — compiled output is not gitignored"
  done
fi
echo

if [ "$FAILED" -ne 0 ]; then
  echo "PREFLIGHT FAILED — $FAILED problem(s). Nothing was changed."
  exit 1
fi
echo "PREFLIGHT PASSED"
if [ "$CHECK_ONLY" -eq 1 ]; then
  echo "(--check: stopping before any mutation)"
  exit 0
fi
echo
N_REPOS="$(echo $REPOS | wc -w | tr -d ' ')"
if [ "$PUBLISH" -eq 1 ]; then
  echo "PUBLISHING REWRITES EACH REMOTE. main is force-pushed to a new orphan commit and its"
  echo "previous history becomes unreachable. Everything is kept locally; nothing is kept there."
  read -r -p "Cut cycle $RELEASE and publish it as $PUBLIC across $N_REPOS repos? [y/N] " reply
else
  read -r -p "Cut cycle $RELEASE across $N_REPOS repos? (no remote will be touched) [y/N] " reply
fi
[ "$reply" = "y" ] || { echo "aborted"; exit 1; }

# ---------------------------------------------------------------------------
# 1. Publish — orphan the cycle onto main  (--publish only)
#
#    An ORPHAN, not a squash. A squash-merge leaves the previous main commits reachable, which is
#    the shape this process deliberately left behind: the remote is a publication surface carrying
#    one commit, and an orphan is the only thing that yields "one commit and nothing else".
#
#    Built from dev/$RELEASE rather than from main. main is a publication, not a development line;
#    orphaning main would publish the previous publication again.
#
#    The tree is verified against dev/$RELEASE before anything is pushed. An orphan takes whatever
#    the index holds, and a stray file would be published permanently under a declared identity.
# ---------------------------------------------------------------------------
if [ "$PUBLISH" -eq 1 ]; then
  for r in $REPOS; do
    git -C "$r" checkout -q --orphan "publish-$PUBLIC"
    git -C "$r" commit -q -m "Protocol-Governed Computing — $PUBLIC"

    want="$(git -C "$r" rev-parse "dev/$RELEASE^{tree}")"
    got="$(git -C "$r" rev-parse "publish-$PUBLIC^{tree}")"
    [ "$want" = "$got" ] || { echo "ABORT: $r orphan tree does not match dev/$RELEASE" >&2; exit 1; }

    git -C "$r" tag -a "$PUBLIC" -m "Protocol-Governed Computing $PUBLIC" "publish-$PUBLIC"
    git -C "$r" push --force origin "publish-$PUBLIC:main"
    git -C "$r" push origin "$PUBLIC"

    git -C "$r" branch -f main "publish-$PUBLIC"
    git -C "$r" checkout -q "dev/$RELEASE"
    git -C "$r" branch -q -D "publish-$PUBLIC"
  done
fi

# ---------------------------------------------------------------------------
# 2. Archive the cycle as a TAG — local, and the reason nothing is lost
#
#    A branch is a mutable pointer; a tag is the archival primitive. These tags are why deleting
#    every remote branch on 2026-08-28 lost nothing: history-9, history-10 and history-11 already
#    pinned the exact cycle tips, so the commits remained reachable without the branch names.
#
#    Not pushed. The remote carries the publication, not the development that produced it.
# ---------------------------------------------------------------------------
for r in $REPOS; do
  git -C "$r" tag -a "history-$RELEASE" "dev/$RELEASE" -m "unsquashed history for cycle $RELEASE"
done

# ---------------------------------------------------------------------------
# 3. Open the next cycle — FROM dev/$RELEASE, not from main
#
#    This is the one place the rewrite changes meaning rather than mechanism. It used to branch
#    from main, which held the squash and therefore the content. main is now an orphan with no
#    ancestry, so branching from it would restart development on a single commit and sever every
#    cycle from the one before it.
#
#    -D is required rather than -d: history-$RELEASE already pins the tip, so nothing is lost, but
#    git has no merge relation to reason about.
# ---------------------------------------------------------------------------
for r in $REPOS; do
  git -C "$r" checkout -q -b "dev/$NEXT" "dev/$RELEASE"
  git -C "$r" branch -q -D "dev/$RELEASE"
done

# ---------------------------------------------------------------------------
# 4. Declare the cycle just opened
#
#    `VERSION` is the single declaration of which composition a repo belongs to, so dev/$NEXT is
#    not honestly open until every repo on it reads $NEXT. Doing it here rather than by hand means
#    the first commit of the new cycle is work rather than bookkeeping.
#
#    Not pushed — there is no remote dev branch to push to. This is the point at which the absence
#    of an offsite copy of work in progress becomes real, and it is a backup problem rather than a
#    branching one: resist solving it by pushing dev branches, which would undo the publication
#    surface this process exists to keep.
#
#    Runs only after step 3 completed for EVERY repo: `set -e` aborts at the first failure above,
#    so a partially cut cycle never reaches here. That is the intent — an unresolved problem must
#    not be papered over by moving versions forward.
# ---------------------------------------------------------------------------
for r in $REPOS; do
  printf '%s\n' "$NEXT" > "$r/VERSION"
  git -C "$r" add VERSION
  git -C "$r" commit -q -m "VERSION bump to $NEXT"
done

# ---------------------------------------------------------------------------
# 5. Verify
# ---------------------------------------------------------------------------
for r in $REPOS; do
  printf "%-22s on %-8s VERSION %-4s %s%s\n" "$r" \
    "$(git -C "$r" branch --show-current)" \
    "$(cat "$r/VERSION")" \
    "$(git -C "$r" tag --list "history-$RELEASE" | tr '\n' ' ')" \
    "$([ "$PUBLISH" -eq 1 ] && printf '%s main=%s' "$PUBLIC" "$(git -C "$r" rev-parse --short main)")"
done
echo
if [ "$PUBLISH" -eq 1 ]; then
  echo "Published as $PUBLIC. Each remote now carries one commit on main and the tag $PUBLIC."
  echo "Record the identity in .github/publications.md if anything about it changed."
else
  echo "Cycle $RELEASE cut locally. Nothing was published; no remote was touched."
fi
echo "Next cycle: reinstall editable packages, rebuild clean."
