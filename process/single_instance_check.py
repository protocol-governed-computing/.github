#!/usr/bin/env python3
"""Single instance — each artifact holds one live version.

Development is open and nothing is retained for its own sake (`retention.yaml`). So an artifact whose
meaning changes takes a new version, names its predecessor in `supersedes`, and the predecessor is
deleted and recorded in `retired_identities.yaml`. History is the release at its tag, the ledger and
`supersedes`; the live tree holds what runs.

This groups the working composition (`snapshot/`) by artifact name without its version suffix and
reports every name present in more than one version. A deleted name used again is
`published_identity_check`'s finding, not this one's.

    single_instance_check.py --namespace transformation [--namespace …]

The check runs on the namespaces named: on `transformation` from the rebuild's swap, and on every
namespace once each has deleted what it stood down.

Exit 0 when every named namespace holds each artifact in one version, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

SNAPSHOT = Path(os.environ.get("PGC_SNAPSHOT_ROOT", "snapshot"))
VERSION = re.compile(r"^(?P<name>.+)_V(?P<version>\d+)$")


def identities(root: Path) -> set[str]:
    out: set[str] = set()
    for path in (root / "canonical").rglob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        fqdn = record.get("fqdn_id") or record.get("fqdn") or (record.get("frontmatter") or {}).get("fqdn")
        if fqdn:
            out.add(fqdn)
    return out


def main(argv: list[str]) -> int:
    namespaces = [argv[i + 1] for i, arg in enumerate(argv[:-1]) if arg == "--namespace"]
    if not namespaces or len(namespaces) * 2 != len(argv):
        print(__doc__.split("\n\n")[3])
        return 2

    versions: dict[str, list[str]] = defaultdict(list)
    held = 0
    for fqdn in identities(SNAPSHOT):
        namespace, code = fqdn.split("::", 1)
        match = VERSION.match(code)
        if namespace not in namespaces or not match:
            continue
        held += 1
        versions[f"{namespace}::{match['name']}"].append(fqdn)

    findings = {name: sorted(found, key=lambda f: int(VERSION.match(f.split('::')[1])['version']))
                for name, found in versions.items() if len(found) > 1}
    if not findings:
        print(f"SINGLE INSTANCE PASSED — {held} artifacts in {', '.join(namespaces)}, each in one version")
        return 0
    for name, found in sorted(findings.items()):
        print(f"\n{name}\n   live in {len(found)} versions: {', '.join(f.split('::')[1] for f in found)}")
    print(f"\nSINGLE INSTANCE FAILED — {len(findings)} artifact(s) in {', '.join(namespaces)} live in more "
          f"than one version")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
