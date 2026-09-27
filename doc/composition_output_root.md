# Two compositions can overwrite each other's output

Held in `doc/` as a follow-on. Nothing is broken today; the hazard appeared the moment one surface
began serving more than one composition, and the mechanism that would prevent it does not exist yet.

## What can happen

The compiler's output root defaults to `<platform>/snapshot` and is overridden by
`PGC_SNAPSHOT_ROOT`. A build configuration declares the *subpaths within* that root —
`compiled/canonical`, `compiled/vocabulary`, `compiled/trust` — and does not declare the root.

So nothing refuses this:

```bash
PGC_SNAPSHOT_ROOT=.../software_governance/snapshot \
  protocol_compiler compile --structure STRUCTURE_BUILD_PLATFORM_MULTIWORKER_CONFIG_V2
```

The multi-worker composition is written over the single-node one. Both builds report success, the
output is internally consistent, and what is on disk is no longer what the reader believes: a
directory named for one composition holding another. The next assembly seals it.

## Why it is new

While one surface served one composition, the root could be supplied by the invocation without
consequence — there was nothing else it could collide with. Placement became composable, a second
build configuration appeared, and the same freedom became a way for two compositions to occupy one
location.

A naming habit — `snapshot/`, `snapshot_mw/` — makes the collision less likely and prevents nothing.
The `snapshot_*/` ignore rule records the habit; it does not enforce it.

## The shape of the fix

The rule established while making placement composable applies unchanged:

> A property that must differ per composition belongs to the composition — not to the surface, and
> not to the invocation.

The output root is that shape. Declare it where every other path is already declared:

```yaml
output_configuration:
  root: snapshot_mw
  artifacts:
    layer: PROTOCOL_BUILD_ROOT
    subpath: compiled/canonical
```

`output_configuration` is a free-form object in `SCHEMA_STRUCTURE_V0`, so this needs no schema
change, and build configurations already declare paths — this adds no new kind of thing.

**Additive, so the blast radius is nil.** Declared root where present, current behaviour otherwise:
`snapshot/` stays `snapshot/`, and `regression.sh`, the runbook and `pgc_install`'s README keep
working untouched.

## What declaring it buys beyond tidiness

The collision becomes **checkable** rather than merely unlikely. Two build configurations naming one
root is a refusable condition a rule can state. Output carrying a marker of which configuration
wrote it makes an overwrite detectable after the fact rather than inferred from surprise.

Neither is possible while the root is an argument: an invocation cannot be checked against a
declaration that does not exist.

## What not to do

**Do not derive the root from the configuration's name.** `snapshot_platform_multiworker_config_v1/`
is accurate and unusable, and mechanical derivation makes the path a function of a name rather than
a declaration — the same reason the compiler reads `placement_mode` from an artifact instead of
parsing it out of the artifact's code. A short name the configuration chooses is explicit where a
derived one is inferred.
