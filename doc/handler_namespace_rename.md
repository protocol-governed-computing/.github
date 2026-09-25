# Handler keys name a retired namespace

Deferred to v5, and held here rather than in scratch: the rename is wanted, it is only the timing
that is open. Not a defect, not reachable, and not urgent — but it reads as all three, which is why
it is written down.

## What it is

Every assertion artifact names the handler that evaluates it:

```yaml
assert_projection:
  handler: pgs_governance.registry.handlers.assert_cs_surface_closed_v0
```

`pgs_governance` is the retired RI-0 namespace. Nothing imports it. The string is a **key in a
static registry**, and the callable it resolves to lives in the current tree:

```python
# protocol_compiler/compiler/governance_engine/assertions/handlers/__init__.py
# Static handler registry (FQDN → callable)
# This is the ONLY allowed way to resolve handlers
# Any handler not in this dict MUST cause compile failure
HANDLER_REGISTRY = {
    "pgs_governance.registry.handlers.assert_cs_surface_closed_v0": assert_cs_surface_closed_v0,
    ...
}
```

## The measurement

```
registry keys                    89
  naming pgs_governance          89      every one
  naming a current namespace      0
artifacts naming a key            7
Python imports of pgs_*           0
pgc_env_check.py            PASSED      no RI-0 dependency reachable
```

It is not one stale reference. It is the naming convention, applied consistently, with nothing
behind it.

## Why it is worth doing anyway

A reader who meets `pgs_governance.registry.handlers…` inside a governance artifact concludes the
surface depends on RI-0. That conclusion is wrong and the evidence for it is right there in the
artifact. It was in fact drawn once, from this exact line, by a reader who then checked.

The environment check cannot catch it and should not be changed to try: it asserts that no RI-0
package is *reachable*, and none is. A name that resembles an import and is not one is invisible to
a check that resolves imports. That is the gap worth recording — not the name itself.

## Why it is not urgent

The rename changes no governance behavior. Same callables, same assertions, same determinations,
same refusals. It is a relabelling whose whole value is that the label stops misleading.

## Why it must be one commit

The registry key and the artifact that names it must agree. A handler not in the dict is a compile
failure **by design** — the registry's own comment says so. So a partial rename does not degrade;
it stops the build.

Any attempt at a "surgical" single-artifact repair therefore breaks the compile. That is the trap to
record: this looks like the kind of defect one fixes in one place, and it is the kind one fixes in
ninety-six or not at all.

## What doing it involves

- 89 keys in the compiler's handler registry
- 7 assertion artifacts in the governance surface
- one commit spanning both repositories, with the counts above as its evidence
- afterwards: recompile the surface, confirm the same assertions fire on the same inputs, and
  confirm that nothing else in the family named a key

Nothing else should ride along. Its value is that it is provably behaviour-neutral, and that is only
provable if it changes nothing else.
