# Fixed Scope

Family revision: `f476ea5c06506a3efba1d773a5d42818c9190601`.

The following constraints are fixed by the commission and profile, rather than selected by the realization:

- one governed system;
- one tenant;
- one sealed snapshot accepted whole and executed against governed state;
- inspection required;
- no external protocol boundary during this profile's scope;
- no replication;
- no attestation beyond family requirements;
- profile identity `NPP-E`;
- authorized inputs limited to the commission, `REVISION`, `NPP-E-scope.md`, `NPP-E.md`, and the 32 `spec` documents.

**Sources:** `NPP-E-scope.md` Commission-fixed scope table; `task_build_a_realization.md` §§2-4; `NPP-E.md` §§1-2.

The chosen implementation stack and canonicalization scheme are not fixed scope; they are recorded as author determinations in `determinations.md`.
