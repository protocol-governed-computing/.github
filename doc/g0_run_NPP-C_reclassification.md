# G0 run `NPP-C` — reclassification

The run's registers were authored under the taxonomy the worker was handed, which has since been
withdrawn from the commission. What follows is the commissioning side's classification, done after
the run, under the current scheme including **class 0 — commissioner scope**.

The profile artifact is unaffected. This corrects the accounting, not the work.

## Decision ledger

**Class 1 — realization freedom. All five stand.** Encoding, internal decomposition, process
topology, read-surface access form, and evidence representation. Each cites text that does leave it
open: `3c` §12 puts components, processes, threading and concurrency outside the standard, and `1a`
§1 admits any representation carrying the meaning without loss.

**Class 2 — seven of twelve move to class 0.**

| Entry | Was | Is | Why |
|---|---|---|---|
| profile identity is `NPP-C` | 2 | **0** | `6a` §9 requires *an* identity; the commission supplied *this* one |
| what the profile profiles | 2 | **0** | the commission's §2 scope, restated |
| inspection is required | 2 | **0** | commission's §2 |
| no external protocol boundary | 2 | **0** | commission's §2 |
| no attestation regime beyond the family | 2 | **0** | commission's §2 |
| no replication | 2 | **0** | commission's §2 |
| no multiple tenants | 2 | **0** | commission's §2 |
| what the profile excludes | 2 | **0 / 2** | the *obligation* to state exclusions is `6a` §5 and is class 2; their *content* is the commission's scope restated |

**Four stand as class 2**, and these are the entries that actually show the family delegating well:
which kinds are admissible (`2d`, `6a` §7), whether additional enforceable obligations are permitted
(`6a` §5, NP-6), which claims are supported (`6a` §5, `7a` §3), and whether the profile is derived
(`6a` §10). None cites the commission.

## Findings register

**Class 3 — two of three stand.**

- *What a checking party accepts as a trust root* — **stands**. `6a` §7 lists it by name as a
  profile decision, and the family supplies no trust-root model. Delegated and underspecified is
  exactly right.
- *What determines one system versus a composition* — **stands**.
- *What constitutes a tenant* — **moves to class 0.** The one-tenant constraint is the commission's,
  not the family's. But see the new finding below: the reclassification surfaced something the
  original entry buried.

**Class 4 — one of two stands.**

- *Is a domain or tenant a concern, an authority, or both* — **stands, narrowed to domain.** `6c` §4
  and `2b` §7.2 genuinely support more than one reading. The tenant half is class 0.
- *Does "no external protocol boundary" mean no wire protocol anywhere, or none in the claimed
  surface* — **moves to class 0.** The ambiguous phrase is the commission's own §2 wording, not the
  family's. The commission is ambiguous here; the standard is not implicated.

**Class 5 — both stand, and they are the run's most valuable output.**

- **No normative syntax, format, or schema for a profile artifact.** The family requires an identity
  and claims and supplies no form for the artifact carrying them, so a profile claim cannot be
  mechanically checked.
- **No claim vocabulary or registry.** Nothing makes claim names interoperable between profiles.

**Class 6 — neither stands. The run produced none.**

Both entries describe matters the author *declined to invent* and then proceeded past: the concrete
trust-root structure, and the authority mechanism for profile change. Class 6 is *could not proceed
without reconstructing something knowable only from a realization*. The author proceeded. Both are
better read as omissions — and the first duplicates the class 3 trust-root entry at a different
class, which is the same matter filed twice.

**That the most valuable class produced nothing is itself a result.** It is what the trial exists to
find, and this run did not find it. Whether that means the standard has no such gaps, or that one
sweep by one author does not surface them, a single run cannot say.

## A finding the reclassification surfaced

**The family uses `tenant` in `6b` and `5a` and defines it nowhere.**

**Dispositioned since, and declined — the reading below was wrong.** Both usages are illustrative
lists. `6b` §11 names *"replication, reachability, bounded staleness, agreement about which snapshot
is current, isolation between tenants"* among things an environment profile **may** require, and
`5a` §12 lists *"a version, a tenant, an authority context"* as scopes. `tenant` sits beside other
words the family neither defines nor needs to. `6b` requires that whatever a profile constrains be
*declared* — a requirement about declaration, not about tenants. Recorded in `revisions.md`.

The original reading, left as written: `6b` names tenants as an environmental constraint —
load-bearing usage — and `1a` §2 holds that a term not defined in Part I is not a PGC term.

The terminology projection cannot see this: it tracks terms a document *declares*, and nothing
declares `tenant`. It is the same shape as Finding **E** approached from the other side — E asks
when a word must become a term; this is a word that behaves like one and never was.

## Net effect

Nine findings become **seven**: three reclassified to class 0, two class 6 downgraded to class 5,
one new finding added. Twelve class 2 ledger entries become **four**.

**Finding F is untouched** by any of this. The four-kind vocabulary was the author's own, cites no
commission provision, and stands as the run's result.

**Finding A remains untestable from this run** — not disproved, not answered. It requires unaided
replication under the repaired commission.
