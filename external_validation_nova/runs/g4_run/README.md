# G4 run — deliverables

The governed transformation adding a lending domain to the `NPP-E` realization, and the state of the
files G4 changed.

## What is here

| | |
|---|---|
| `transform_npp_e.py`, `test_transform_npp_e.py` | the transformation and its demonstrations |
| `transformation_evidence.md` | what an outside party can check, and how |
| `determinations.md`, `unresolved.md` | the registers, as at G4 |
| `npp_e.py`, `test_npp_e.py`, `conformance_evidence.md` | **the G2 system as G4 left it** — see below |
| `evaluation.md` | the commissioning side's reading |

## Why three G2 files appear here

`g2_run/` holds the system **as at G2 close**. Three of those files changed afterwards, and both
states are kept rather than one overwriting the other:

- **`test_npp_e.py`** — six demonstrations at G2, seven now. The seventh closes the SHA-256 gap: the
  G2 suite passed unchanged when SHA-256 was swapped for MD5, so nothing bound the algorithm
  `NPP-E` selects.
- **`conformance_evidence.md`** — now records the baseline snapshot identity, which G2's copy did
  not. A claim is against a subject, and the subject was unnamed.
- **`npp_e.py`** — carried forward with the above.

## The sandbox is one codebase and is not split

`transform_npp_e.py` opens with `import npp_e`. The transformation runs *inside* the realization
rather than beside it, so the working directory stays whole; separating them by gate would break the
import and misrepresent what a transformation is.

The split lives here, in the record, where it costs nothing.
