#!/usr/bin/env bash
# Publish the component releases whose Zenodo deposits the composition names by DOI.
#
#   publish_component_releases.sh             publish a GitHub release of $PUBLIC on each component
#   publish_component_releases.sh --verify    list which components have a Zenodo record at $PUBLIC
#
# `release.sh --publish-composition` names every component by its version DOI, and `compose_release.py`
# refuses to compose until all of them exist. A component's DOI is minted when a *GitHub release* of
# its tag is published — pushing the tag alone does not fire the Zenodo webhook. Those releases were
# made by hand in every cycle, from memory, and in v4 the missing step read as a network error. This
# is that step, written down.
#
# Safe to repeat: a component already released at $PUBLIC is skipped, so a partial run is finished by
# running it again. It publishes nothing unless Zenodo answers first — a release published during an
# outage mints no DOI and needs a per-repository webhook redelivery afterwards, which the usual token
# cannot do. A component without a Zenodo release webhook is refused before anything is published.
#
# Wait a minute or two after publishing, then run --verify: every component must show a record.
set -u
WORKSPACE=~/protocol-governed-computing
ORG=protocol-governed-computing
PUBLIC="$(cat "$WORKSPACE/.github/PUBLIC_VERSION" 2>/dev/null || true)"
[ -n "$PUBLIC" ] || { echo "no public identity in .github/PUBLIC_VERSION" >&2; exit 2; }

# The list compose_release.py names, read from it rather than copied, so the two cannot disagree.
COMPONENTS="$(cd "$WORKSPACE/.github/process" && python3 -c 'from compose_release import COMPONENTS; print(" ".join(COMPONENTS))')" \
  || { echo "cannot read COMPONENTS from compose_release.py" >&2; exit 2; }
if [ "${1:-}" = "--verify" ]; then
  # Read the way the composition reads them — compose_release's paged query and title match.
  cd "$WORKSPACE/.github/process" && python3 - "$PUBLIC" <<'PY'
import sys
from compose_release import COMPONENTS, ORCID, zenodo_records
public = sys.argv[1]
records = zenodo_records(ORCID)
missing = 0
for repo in COMPONENTS:
    hit = next((h for h in records if f"({repo})" in (h["metadata"].get("title") or "")
                and h["metadata"].get("version") == public), None)
    print(f"  {'OK     ' if hit else 'MISSING'}  {repo:<24} {hit['doi'] + '  ' + hit['created'] if hit else ''}")
    missing += hit is None
print(f"\n  {len(COMPONENTS) - missing}/{len(COMPONENTS)} components have a record at {public}")
sys.exit(1 if missing else 0)
PY
  exit $?
fi

# Zenodo first: a release published while it is unreachable mints nothing.
curl -sf -o /dev/null --max-time 20 "https://zenodo.org/api/records?size=1" \
  || { echo "ABORT: Zenodo is not answering — nothing published. Try again later." >&2; exit 1; }

# Every webhook before any release, so a missing one stops the run rather than a component.
for repo in $COMPONENTS; do
  hooks="$(gh api "repos/$ORG/$repo/hooks" --jq '[.[]|select(.events[]=="release")]|length' 2>/dev/null || echo 0)"
  [ "${hooks:-0}" -ge 1 ] || {
    echo "ABORT: $repo has no Zenodo release webhook — its release would mint nothing." >&2
    echo "  Enable it at https://zenodo.org/account/settings/github/ (select the repo, THEN flip" >&2
    echo "  the switch), and re-run. Nothing has been published." >&2
    exit 1; }
done

published=0; skipped=0
for repo in $COMPONENTS; do
  if gh release view "$PUBLIC" -R "$ORG/$repo" >/dev/null 2>&1; then
    echo "  SKIP       $repo — already released at $PUBLIC"
    skipped=$((skipped + 1)); continue
  fi
  # --verify-tag: the tag must already be pushed; a release never creates one.
  if gh release create "$PUBLIC" -R "$ORG/$repo" --verify-tag \
       --title "Protocol-Governed Computing — $repo $PUBLIC" \
       --notes "Component of the Protocol-Governed Computing composition $PUBLIC."; then
    echo "  PUBLISHED  $repo"
    published=$((published + 1))
  else
    echo "ABORT: release of $repo at $PUBLIC failed — $published published so far; re-run to finish." >&2
    exit 1
  fi
done
echo
echo "  $published published, $skipped already released. Wait a minute or two, then:"
echo "    $0 --verify"
