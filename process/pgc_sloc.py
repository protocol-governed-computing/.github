"""How much of PGC is declared behaviour, and how much is implementation — per repo and per layer.

Behaviour is the YAML Machine block of every governed artifact: a `.md` whose block declares an
`artifact_kind`, wherever it lives. Implementation is Python SLOC — non-blank, non-comment, docstrings
excluded — split into runtime code, tests (`testbed/`, `tests/`, `test_*.py`) and tooling
(`scripts/`, `tools/`). Dossier markdown is counted apart, as design record.

Compiled snapshots, caches, virtualenvs, build output and fixture dossiers are excluded. Plain
`.yaml` files are listed separately; the only one today is the generated surface map.

Run:  python .github/process/pgc_sloc.py
"""

from __future__ import annotations

import io
import os
import re
import tokenize
from collections import defaultdict
from pathlib import Path

W = Path(__file__).resolve().parents[2]
SKIP = {".git", ".venv", "__pycache__", "snapshot", "build", "data", "traces", "node_modules",
        ".idea", "compiled", "fixture_dossiers"}
MACHINE = re.compile(r"```yaml\n(.*?)```", re.S)
COLUMNS = ["artifacts", "yaml_artifact", "yaml_file", "py_impl", "py_test", "py_tools", "dossier_md"]

PLATFORM = ["software_governance", "conformance_workloads", "protocol_compiler", "snapshot_assembler",
            "protocol_runtime", "protocol_transport", "snapshot_inspector", "transformation"]
LAYERS = {
    "governance surface": ["software_governance"],
    "conformance workload": ["conformance_workloads"],
    "toolchain": ["protocol_compiler", "snapshot_assembler", "protocol_runtime", "protocol_transport",
                  "snapshot_inspector"],
    "transformation": ["transformation"],
}


def yaml_sloc(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip() and not line.strip().startswith("#"))


def py_sloc(path: Path) -> int:
    """Lines carrying code: comments, blank lines and docstrings are not counted."""
    source = path.read_text(errors="ignore")
    code: set[int] = set()
    docs: set[int] = set()
    structural = (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING)
    previous = None
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type in (tokenize.COMMENT, tokenize.NL, tokenize.ENDMARKER):
            continue
        if tok.type in structural:
            previous = tok
            continue
        span = range(tok.start[0], tok.end[0] + 1)
        # A string standing alone as a statement is a docstring.
        is_doc = tok.type == tokenize.STRING and (previous is None or previous.type in structural)
        (docs if is_doc else code).update(span)
        previous = tok
    return len(code - docs)


def python_kind(rel: Path) -> str:
    if any(p in ("testbed", "tests", "test") for p in rel.parts) or rel.name.startswith("test_"):
        return "py_test"
    if "scripts" in rel.parts or "tools" in rel.parts:
        return "py_tools"
    return "py_impl"


def measure(root: Path) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.endswith(".egg-info")]
        for name in filenames:
            path = Path(dirpath) / name
            rel = path.relative_to(root)
            if name.endswith(".py"):
                out[python_kind(rel)] += py_sloc(path)
            elif name.endswith((".yaml", ".yml")):
                out["yaml_file"] += yaml_sloc(path.read_text(errors="ignore"))
            elif name.endswith(".md"):
                text = path.read_text(errors="ignore")
                if "cr_dossiers" in rel.parts or "dossiers" in rel.parts:
                    out["dossier_md"] += sum(1 for line in text.splitlines() if line.strip())
                elif "artifact_kind:" in text:
                    out["artifacts"] += 1
                    out["yaml_artifact"] += sum(yaml_sloc(m) for m in MACHINE.findall(text))
    return out


def main() -> int:
    rows = [(repo, measure(W / repo)) for repo in PLATFORM]
    domains = W / "business_domains"
    business = sorted(d for d in os.listdir(domains) if (domains / d / "registry").is_dir())
    rows += [(f"bd/{d}", measure(domains / d)) for d in business]

    print(f"{'repo':<26}" + "".join(f"{c:>14}" for c in COLUMNS))
    total: dict[str, int] = defaultdict(int)
    for repo, counts in rows:
        print(f"{repo:<26}" + "".join(f"{counts[c]:>14,}" for c in COLUMNS))
        for c in COLUMNS:
            total[c] += counts[c]
    print(f"{'TOTAL':<26}" + "".join(f"{total[c]:>14,}" for c in COLUMNS))

    by_repo = dict(rows)
    layers = {name: [by_repo[r] for r in repos] for name, repos in LAYERS.items()}
    layers["business domains"] = [by_repo[f"bd/{d}"] for d in business]
    print(f"\n{'layer':<22}{'behaviour':>12}{'implementation':>16}   ratio")
    for name, parts in layers.items():
        yaml = sum(p["yaml_artifact"] for p in parts)
        py = sum(p["py_impl"] for p in parts)
        ratio = f"{yaml / py:.1f} : 1" if yaml >= py and py else f"1 : {py / yaml:.1f}" if yaml else "—"
        print(f"{name:<22}{yaml:>12,}{py:>16,}   {ratio}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
