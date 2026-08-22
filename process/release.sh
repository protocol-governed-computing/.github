#!/usr/bin/env bash
#
# PGC release cut — the standard process, parameterised by release ordinal.
#
#   development on dev/<N>  →  squash-merge to main  →  tag release-<N>
#                           →  archive history as tag history-<N>
#                           →  delete local branch  →  open dev/<N+1>
#
# To cut the next release, change RELEASE and NEXT below. Nothing else varies.
#
# PGC versions the COMPOSITION, not each repo independently: all repos release together and the
# governance closure forces lockstep, so one monotonic integer names which composition a repo
# belongs to. The single declaration is each repo's `VERSION` file — pyproject and the Python
# version constants derive from it. Never hand-edit a version anywhere else.
#
# Read this before running it. It pushes and deletes remote refs.
#
# Usage:
#   release.sh              preflight, then cut the release
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
case "${1:-}" in
  "")       ;;
  --check)  CHECK_ONLY=1 ;;
  -h|--help) sed -n '2,28p' "$0"; exit 0 ;;
  *) echo "unknown argument: $1 (usage: release.sh [--check])" >&2; exit 2 ;;
esac

RELEASE=10         # the release being cut  — branch dev/$RELEASE must exist and be current
NEXT=11            # the cycle to open next — branch dev/$NEXT will be created from main

WORKSPACE="$HOME/protocol-governed-computing"

# The composition — every repo that compiles, assembles, is assembled into a snapshot, reads one,
# or transforms one into the next. `snapshot_inspector` joined at release 3 (it missed release 2
# because it was not yet a git repo); `transformation` joins at release 4 and correctly
# carries no earlier tag. `.github` was excluded while it held only the org profile page; it now
# also holds the snapshot assembly contract that `snapshot_assembler` and `protocol_runtime` cite
# as the contract they implement, so it carries composition surface and releases in lockstep.
REPOS="software_governance conformance_workloads business_domains protocol_compiler \
protocol_runtime snapshot_assembler protocol_transport snapshot_inspector \
transformation .github"

# The squash commit is the ONLY durable description of this release on main — the detailed
# commits live on dev/<N> and are unreachable from main after squashing.
#
# Read by convention from the per-release notes file — one file per release, so `main` carries a
# readable history of what each composition was, independent of any commit message.
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

echo "Preflight for release $RELEASE"
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

  git -C "$r" fetch -q origin 2>/dev/null || fail "$r cannot reach origin"

  # Unpushed work would be squashed into the release but absent from the archived branch.
  git -C "$r" rev-parse --verify -q "origin/dev/$RELEASE" >/dev/null 2>&1 \
    && { [ "$(git -C "$r" rev-list --count "origin/dev/$RELEASE..dev/$RELEASE" 2>/dev/null)" = "0" ] \
         || fail "$r has commits on dev/$RELEASE not pushed to origin"; } \
    || fail "$r has no origin/dev/$RELEASE — push the branch first"

  # main must exist locally and be fast-forwardable, or step 1's pull aborts mid-release.
  git -C "$r" rev-parse --verify -q main >/dev/null 2>&1 || fail "$r has no local main branch"
  # Behind origin/main is fine — step 1 fast-forwards. AHEAD is the problem: --ff-only aborts,
  # mid-release, after other repos are already pushed.
  ahead="$(git -C "$r" rev-list --count "origin/main..main" 2>/dev/null || echo 0)"
  [ "$ahead" = "0" ] || fail "$r local main is $ahead ahead of origin/main — pull/reconcile first"

  # A pre-existing tag makes step 1 or 2 fail after other repos have already been pushed.
  for tg in "release-$RELEASE" "history-$RELEASE"; do
    git -C "$r" rev-parse --verify -q "refs/tags/$tg" >/dev/null 2>&1 \
      && fail "$r already has tag $tg"
    git -C "$r" ls-remote --tags origin "$tg" 2>/dev/null | grep -q . \
      && fail "$r origin already has tag $tg"
  done

  # dev/$NEXT must not exist yet, locally or remotely.
  git -C "$r" rev-parse --verify -q "dev/$NEXT" >/dev/null 2>&1 && fail "$r already has dev/$NEXT"
done
[ "$FAILED" -eq 0 ] && ok "all $(echo $REPOS | wc -w | tr -d ' ') repos on dev/$RELEASE, clean, synced, no tag collisions"
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
  protocol_compiler/compile.sh >/tmp/pgc_rel_build.log 2>&1 || BUILD_OK=0
  if [[ $BUILD_OK -eq 1 ]]; then
    for root in "${BUILDABLE[@]}"; do
      [[ "$root" == "$WORKSPACE/software_governance" ]] && continue   # compile.sh builds the platform
      protocol_compiler/compile_domain.sh "$root" >>/tmp/pgc_rel_build.log 2>&1 || { BUILD_OK=0; break; }
    done
  fi
  if [[ $BUILD_OK -eq 1 ]] && snapshot_assembler/assemble.sh >>/tmp/pgc_rel_build.log 2>&1; then
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
read -r -p "Cut release $RELEASE across $(echo $REPOS | wc -w | tr -d ' ') repos? [y/N] " reply
[ "$reply" = "y" ] || { echo "aborted"; exit 1; }

# ---------------------------------------------------------------------------
# 1. Squash to main, tag release-$RELEASE, push
#
#    --squash stages without committing, so the message above is authored fresh. It creates a
#    commit with NO parent link to the branch: dev/$RELEASE will never show as merged, and the
#    detailed commits are unreachable from main. That is why step 2 exists.
# ---------------------------------------------------------------------------
for r in $REPOS; do
  git -C "$r" checkout main
  git -C "$r" pull --ff-only origin main
  git -C "$r" merge --squash "dev/$RELEASE"
  git -C "$r" commit -m "$MSG"
  git -C "$r" tag -a "release-$RELEASE" -m "release $RELEASE"
  git -C "$r" push origin main
  git -C "$r" push origin "release-$RELEASE"
done

# ---------------------------------------------------------------------------
# 2. Archive the unsquashed history as a TAG
#
#    A branch is a mutable pointer — a force-push or delete loses the history silently. A tag is
#    the archival primitive and keeps those commits reachable permanently. The branch is pushed
#    too, for convenience; the tag is what guarantees the history survives.
# ---------------------------------------------------------------------------
for r in $REPOS; do
  git -C "$r" tag -a "history-$RELEASE" "dev/$RELEASE" -m "unsquashed history for release $RELEASE"
  git -C "$r" push origin "dev/$RELEASE"
  git -C "$r" push origin "history-$RELEASE"
done

# ---------------------------------------------------------------------------
# 3. Delete local branch, open the next cycle
#
#    -D is required, not -d: squash-merge left no parent link so git never sees the branch as
#    merged. Safe only because history-$RELEASE is already pushed — keep that ordering.
#    Deleting locally prevents accidental reuse of a released branch.
# ---------------------------------------------------------------------------
for r in $REPOS; do
  git -C "$r" branch -D "dev/$RELEASE"
  git -C "$r" checkout -b "dev/$NEXT" main
  git -C "$r" push -u origin "dev/$NEXT"
done

# ---------------------------------------------------------------------------
# 4. Verify
# ---------------------------------------------------------------------------
for r in $REPOS; do
  printf "%-22s on %-8s tags: %s\n" "$r" \
    "$(git -C "$r" branch --show-current)" \
    "$(git -C "$r" tag --list "release-$RELEASE" "history-$RELEASE" | tr '\n' ' ')"
done
echo
echo "Next cycle: bump each VERSION to $NEXT, reinstall editable packages, rebuild clean."
