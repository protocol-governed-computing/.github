#!/usr/bin/env python3
"""
Regenerate `pgc_release` — the published composition — from the sealed snapshot.

WHY THIS IS A SECOND PHASE, NOT PART OF `release.sh --publish`.

`pgc_release` names the nine component version DOIs as `hasPart`. Those DOIs do not exist until
Zenodo has minted them, and Zenodo mints them only after `--publish` has pushed each component's
tag and a GitHub release has fired. So the composition cannot be assembled in the same pass that
publishes its parts: the inputs are not in the world yet. Anything that pretended otherwise would
either publish a composition naming DOIs it invented, or hard-code last release's.

The ordering is therefore:

    release.sh --publish            nine repos + .github published, Zenodo mints nine DOIs
    (wait for the mints)
    release.sh --publish-composition    this script, then commit/tag/push pgc_release

This script is idempotent and touches no remote. It rewrites the working tree of `pgc_release`
and stops; `release.sh` does the git work.

The component DOIs are DISCOVERED, not declared. A declared list is a second copy of a fact Zenodo
already holds, maintained by hand, with nothing to catch it going stale — the same failure the
release ordinal had before it was derived. Discovery fails hard when a component's record is
missing, which is the honest outcome: the composition is not assemblable until every part is.
"""

import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ORCID = "0009-0007-3810-6520"
STANDARD_CONCEPT = "10.5281/zenodo.22150615"

# Order is the composition's own: surface, workloads, domains, then the toolchain that
# produces and consumes the snapshot. It is not alphabetical and should not be sorted.
COMPONENTS = [
    "software_governance",
    "conformance_workloads",
    "business_domains",
    "protocol_compiler",
    "protocol_runtime",
    "snapshot_assembler",
    "protocol_transport",
    "snapshot_inspector",
    "transformation",
]


def die(msg):
    print(f"compose_release: {msg}", file=sys.stderr)
    sys.exit(1)


def zenodo_records(orcid):
    """Every record for this author, newest first. One request, then matched locally."""
    q = urllib.parse.urlencode(
        {"q": f'creators.orcid:"{orcid}"', "sort": "newest", "size": "100"}
    )
    url = f"https://zenodo.org/api/records?{q}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r).get("hits", {}).get("hits", [])
    except Exception as e:
        die(f"cannot reach Zenodo: {e}")


def component_dois(public, records):
    """
    Match on the repo name in parentheses in the record title, at this public identity.
    The component deposits are titled e.g. `... Protocol Compiler (protocol_compiler)`, so the
    repo name is carried in the metadata rather than inferred from ordering.
    """
    found, missing = {}, []
    for repo in COMPONENTS:
        hit = next(
            (
                h
                for h in records
                if f"({repo})" in (h.get("metadata", {}).get("title") or "")
                and h.get("metadata", {}).get("version") == public
            ),
            None,
        )
        if hit is None:
            missing.append(repo)
        else:
            found[repo] = hit["doi"]
    if missing:
        die(
            f"no Zenodo record at {public} for: {', '.join(missing)}\n"
            f"  the composition names its parts by DOI, so it cannot be assembled until every\n"
            f"  component is minted. Check the GitHub-Zenodo webhook on each repo:\n"
            f"    gh api repos/protocol-governed-computing/<repo>/hooks --jq '.[].events'"
        )
    return found


def standard_doi(records):
    hit = next(
        (
            h
            for h in records
            if h.get("conceptdoi") == STANDARD_CONCEPT
        ),
        None,
    )
    if hit is None:
        die(f"no Zenodo record found under the standard's concept DOI {STANDARD_CONCEPT}")
    return hit["doi"], hit.get("metadata", {}).get("version", "?")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True
    ).stdout.strip()


def main():
    ws = Path(__file__).resolve().parents[2]
    public = (ws / ".github" / "PUBLIC_VERSION").read_text().strip()
    ordinal = (ws / ".github" / "VERSION").read_text().strip()
    snapshot = ws / "snapshot"
    target = ws / "pgc_release"

    if not (snapshot / "manifest.json").is_file():
        die(f"no sealed snapshot at {snapshot}")
    if not (target / ".git").is_dir():
        die(f"{target} is not a git repo")

    manifest = json.loads((snapshot / "manifest.json").read_text())
    conf = json.loads((snapshot / "conformance" / "composition.json").read_text())

    if conf.get("status") != "PASSED":
        die(f"composition conformance is {conf.get('status')}, refusing to publish it")

    records = zenodo_records(ORCID)
    dois = component_dois(public, records)
    std_doi, std_ver = standard_doi(records)

    # --- snapshot: replace wholesale, so a retired artifact cannot survive into a release -----
    staged = target / "snapshot"
    if staged.exists():
        subprocess.run(["rm", "-rf", str(staged)], check=True)
    subprocess.run(["cp", "-R", str(snapshot), str(staged)], check=True)
    for junk in staged.rglob(".DS_Store"):
        junk.unlink()

    n_files = sum(1 for p in staged.rglob("*") if p.is_file())
    domains = [d["domain"] for d in manifest["domains"]]

    # --- MANIFEST -----------------------------------------------------------------------------
    rows = []
    for repo in COMPONENTS:
        commit = git(ws / repo, "rev-parse", public)
        contributes = "yes" if repo in manifest["provenance"]["source_commits"] else "—"
        rows.append(f"| `{repo}` | {dois[repo]} | `{commit[:12]}` | {contributes} |")

    man = f"""# PGC {public} — composed platform: deposit manifest

**Public identity:** {public}
**Assembler ordinal:** {manifest['provenance']['assembler_version']}
**Profile:** {manifest['profile']}

**Sealed snapshot id**
`{manifest['snapshot_id']}`

**Composite hash**
`{manifest['composite_hash']}`

## What this deposit is

The *composition* — a single governance surface assembling {len(domains)} governed domains,
including mutually unrelated business domains, over {conf['artifacts_examined']} protocol artifacts.
Claims about domain independence and closure refer to this artifact, not to any one component
repository. The {len(COMPONENTS)} components are archived separately and named below as parts.

## Conformance

- Phase: `{conf['phase']}` (conformance {conf['conformance_version']}, assembler {conf['assembler_version']})
- Artifacts examined: **{conf['artifacts_examined']}**
- Rules evaluated: **{conf['rules_evaluated']}**
- Status: **{conf['status']}**
- Checked at: {conf['checked_at']}

### Governed domains ({len(domains)})

""" + "\n".join(
        f"- `{d['domain']}` — graph address `{d['graph_address_hash'][:16]}…`"
        for d in manifest["domains"]
    ) + f"""

## Standard claimed

Open Protocol-Governed Computing Standard, revision {std_ver} — {std_doi}
(archived separately; related as `references`).

## Components ({len(COMPONENTS)})

| Component | Version DOI | Commit at `{public}` | Contributes artifacts |
|---|---|---|---|
""" + "\n".join(rows) + f"""

Components marked `—` are the toolchain; they produce and consume the snapshot rather than
contributing protocol artifacts to it.

### Commit provenance

The `{public}` tags are orphan publication commits on `main`; the snapshot was assembled from the
corresponding `dev/{ordinal}` commits, so the two carry different commit ids by construction. They
are the same content: `release.sh` verifies each orphan's tree against its `dev` tree before
pushing, and aborts if they differ.

## Contents

- `snapshot/` — the sealed snapshot as assembled, {n_files} files, {len(manifest['constituents'])}
  constituents, committed expanded rather than archived, so every artifact is browsable and
  diffable between releases.
- `MANIFEST.md` — this file.
- `.zenodo.json` — deposit metadata, read by the GitHub–Zenodo integration when a release is tagged.

## Not included, and why

- **`.github`** — workspace process. It is released with the components and carries its own DOI,
  but it is process rather than a part of the composition, so it is not named as `hasPart`.
- **`standards`** — carries its own revision identity and is archived separately; related here as
  `references`.
"""
    (target / "MANIFEST.md").write_text(man)

    # --- .zenodo.json -------------------------------------------------------------------------
    zen = json.loads((target / ".zenodo.json").read_text())
    zen["version"] = public
    zen["description"] = (
        "<p>The composed Protocol-Governed Computing reference implementation: a single "
        f"governance surface assembling {len(domains)} governed domains over "
        f"{conf['artifacts_examined']} protocol artifacts, including mutually unrelated business "
        "domains. This deposit identifies the <em>composition</em> — the artifact to which claims "
        "about domain independence and closure refer — rather than any single component "
        "repository. The component repositories are archived separately and related here as "
        "parts.</p><p>Cite this version DOI when citing the reference implementation as "
        "evidence.</p>"
    )
    zen["related_identifiers"] = [
        {"identifier": std_doi, "relation": "references", "resource_type": "software", "scheme": "doi"}
    ] + [
        {"identifier": dois[r], "relation": "hasPart", "resource_type": "software", "scheme": "doi"}
        for r in COMPONENTS
    ]
    (target / ".zenodo.json").write_text(json.dumps(zen, indent=2, ensure_ascii=False) + "\n")

    (target / "VERSION").write_text(f"{manifest['provenance']['assembler_version']}\n")

    print(f"composed {public}: {n_files} snapshot files, {len(domains)} domains, "
          f"{conf['artifacts_examined']} artifacts, {len(COMPONENTS)} parts")
    print(f"  standard  {std_doi} (revision {std_ver})")
    for r in COMPONENTS:
        print(f"  hasPart   {dois[r]}  {r}")


if __name__ == "__main__":
    main()
