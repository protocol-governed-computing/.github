# E0.3 — The build manifest and domain discoverability

Evidence for the ruling. No code or standard was changed to produce this.

**The question.** Does the governed design schedule the production of a domain's build manifest, or
is producing one construction machinery outside the governed design?

---

## 1. What a build manifest is

One artifact per domain, `STRUCTURE_BUILD_<DOMAIN>_CONFIG_V<n>`, kind `STRUCTURE`, governed by the
STRUCTURE constitution, living at `registry/structures/` for a business domain and at
`registry/structure/structures/` for the platform.

Every field in it is compiler configuration:

| Field | What it configures |
|---|---|
| `layer_definitions` | which source layer, which registry module, which implementation namespace |
| `identity_rules` | how a path maps to a namespace |
| `artifact_discovery` | which layers to search, which import surface, which families are admissible |
| `output_configuration` | where projections are written |

**No register of any design phase states any of these.** That is the crux: they are not facts a
design determines about a business domain, they are facts about how the compiler reads a directory.

## 2. Who consumes it

Four consumers, all of which discover a domain *by the presence of this file*:

| Consumer | How it reads the manifest |
|---|---|
| `protocol_compiler/compile_domain.sh:43` | globs `registry/structures/STRUCTURE_BUILD_*_CONFIG_V*.md`; **exits 1** if absent |
| `protocol_compiler/compiler/cli.py` | takes the STRUCTURE code as the unit of compilation |
| `.github/process/release.sh` build gate | a domain **is** anything declaring a `STRUCTURE_BUILD_*_CONFIG`; the enumeration is a `find`, deliberately not a list |
| `transformation/cli.py:745` | `--root` is validated by globbing for one; no config, not a domain root |

**Discoverability is not a separate mechanism.** There is no registry of domains anywhere. A domain
exists, to every tool in the workspace, exactly when this file is on disk where the glob will find
it. That is the whole of the discovery model.

## 3. Behaviour in its absence

- The compiler refuses: *"No STRUCTURE_BUILD_*_CONFIG manifest under `<root>`/registry/structures"*,
  exit 1.
- The release gate does not see the directory as a domain at all — it is skipped silently, because
  the gate enumerates what exists rather than checking against a list of what should.
- `construction emit --root <new domain>` refuses: *"carries no STRUCTURE_BUILD_*_CONFIG_V*.md, so
  it is not a domain root the compiler can discover."*

So the absence is **fail-loud for two consumers and silent for one** — the release gate. A founded
domain that never got a manifest would simply never be built, and nothing would say so.

## 4. What construction used to do, and why it stopped

`transformation/transformation/build/render.py:1020` still contains `build_manifest(p7, p8)`, and it
is still registered as `MANIFEST_GENERATOR` in `build/generators.py:151` with `needs_root=True` and
`derived_from_design=True`. **The generator exists and works.** What changed is that
`construction emit` no longer invokes it to *found* a manifest for a domain that has none.

The reason is recorded at `transformation/cli.py:721-729`. Nothing in any register names the domain,
so the generator inferred it:

```python
domain = norm(scheduled[0]).split("::")[0]   # render.py:1030
```

— the namespace of the first scheduled artifact. **For a business domain the namespace and the
domain are the same word, so the inference was invisible and correct by accident.** The platform
carries one namespace per concern, so the first platform emission produced a manifest declaring one
of the platform's namespaces to be a business domain importing the platform.

The `--root` guard lost its founding exception at the same time, which exposed a second defect: the
guard had been globbing only the business layout (`registry/structures/`), so it read the platform —
which uses `registry/structure/structures/` — as not a domain root. The founding exception had been
skipping the check for exactly the roots where it would have failed.

**Prior art against the other reading.** Hand-copying manifests between domains had already failed
visibly: the book library's manifest described itself as the AI governance domain and listed that
domain's subdomains, because it was copied and never corrected, and nothing governed it.

**Also measured:** when the manifest *was* inventoried as an artifact a design amends, a change
adding one subdomain was obliged to restate fifty-one derived facts it does not decide, and invented
a fifty-second — a `core.subdomain` the artifact does not carry. The only thing that actually varies
with a subdomain is one prose sentence of the summary.

### One inconsistency to fix whichever way this is ruled

`construction_emit`'s docstring still reads *"The domain's build manifest is written too when the
domain has none"* (`cli.py:696`). The comment forty lines below it says *"Construction does not found
a build manifest."* **The code follows the comment; the docstring is stale.**

## 5. How an existing domain became discoverable

None of the seven current domains was founded by construction. Each manifest was written by hand or
copied from a sibling, before the founding exception was removed. `book_library_mgmt` is the one
where the copy was caught.

**The path a new domain cannot take:** `construction emit --root <new>` refuses for want of a
manifest, and construction will not write one. So founding a domain today requires authoring the
manifest by hand, outside any governed design — which is the state the copy-drift defect came from.

---

## The two readings

### A — The governed design schedules the manifest

A design that founds a domain states the facts that vary (domain name, subdomains, families) in a
register, and construction renders the manifest from them like any other scheduled artifact.

- **Requires:** a phase register that can state a domain's identity — which does not exist today, and
  is exactly what the inference was standing in for.
- **Gains:** founding a domain is a governed act with a determination record, and discoverability is
  no longer conferred by a file appearing on disk.
- **Costs:** the design language must be able to say *"this is a domain named X"* — a fact about the
  build, not about the business. That is the boundary the SOTU flags: **without care this makes the
  manifest business governance,** which every field of it is not.
- **Watch:** the fifty-one-facts measurement is evidence against making the *whole manifest*
  designed. Reading A survives only if the design states the three varying facts and the renderer
  derives the rest.

### B — Manifest production is construction machinery, outside the design

The manifest is compiler configuration; construction may produce it as a build output, but no design
determines it and no register mentions it.

- **Requires:** something other than a design to decide *who founds a domain and on what authority*.
  Today: nobody, and the refusal is honest about that.
- **Gains:** keeps configuration out of the design language, which is what the current code does and
  what the fifty-one-facts measurement argues for.
- **Costs:** founding a domain stays an ungoverned act. A hand-written manifest is exactly what
  drifted before, and the release gate's silent skip means a wrong one is not detected — it just
  quietly builds the wrong thing, or nothing.
- **Watch:** this reading must still say what makes a *founded* domain legitimate, or an
  independent implementer asks *"how does my new domain join the executable system?"* and the answer
  is "put a file where a glob will find it."

### What the standard owes, either way

`design → construction → manifest → discoverability` needs a stated semantic relationship. Note the
asymmetry the evidence shows: **discoverability is currently conferred by file placement**, which is
the same shape as `4c` §4.1's prohibition — *"if identity is derived from address, then moving a
thing changes what it is."* Discovery derived from address is not identity derived from address, but
it is close enough that the ruling should say why the two are different, or make them consistent.

---

---

## The ruling

**Two propositions, recorded separately because they resolve in opposite directions.**

### 1. Manifest production is construction machinery, not a governed design decision

The build manifest is not a design artifact. Construction may produce it; its contents are compiler
configuration, not governed business semantics. Grounds, all measured rather than argued:

- Every field configures how the compiler reads and materializes a directory, and **no design
  register determines any of them.**
- Treating the whole manifest as designed obliged a subdomain change to restate fifty-one derived
  facts and invent a fifty-second.
- Construction's generated manifest was demonstrably unsafe — it inferred the domain from the first
  scheduled artifact, correct by accident for a business domain and wrong for the platform.
- Hand-copying produced real cross-domain drift (the book library declaring itself AI governance).

**Consequence: do not create a "manifest" design artifact kind.** Reading A is refused in its
maximal form; the manifest's derivation and physical production stay with construction.

### 2. Domain founding must still be governed

**A manifest appearing on disk cannot by itself constitute authority to introduce a domain.** This is
the hole the investigation exposed, and it does not follow from proposition 1 — it is what stops
proposition 1 from becoming a loophole.

**This requires no Draft-2 change. The standard already decides it.**

- `2e` §6: *"Nothing is admitted by being present, discoverable, referenced, or expected."* Admission
  is a governed transition with a closure, a determination, a result, and evidence.
- `2e` §2 tabulates this exact conflation as a known failure: **Admission** conflated with
  **presence** causes *"being found is being admitted."*
- `6c` §1: a domain is a subject of profiling, and whether it is an authority is *"a determination
  made under Governance Closure & Authority"* — i.e. under `2e`.

**So the RI performs the precise conflation the standard names.** A domain is admitted today by a
file being where a glob finds it. That is a realization finding, not a specification gap.

### The separation this establishes

```
design determines that a domain is ADMITTED
    → construction materializes its compiler configuration
        → the manifest makes the admitted domain DISCOVERABLE
```

**The manifest is evidence and materialization of a governed admission, never the authority for
it.** Discovery is a mechanism that serves admission; it is not a substitute for it.

### What follows, and what does not

- **Not now:** redesigning the manifest mechanism. The ruling fixes the direction, not the design.
- **Open, and now correctly shaped:** what governed act admits a domain, and where its determination
  and evidence live. `6c` is the candidate home — and note that **no domain profile exists for any
  of the six domains** (map finding 36, OPEN), so this is also the first real instance of E4's
  class C.
- **Fix either way:** `transformation/cli.py:696`'s docstring still claims construction writes a
  manifest for a domain that has none. The code follows the comment below it, not the docstring.
- **The `4c` §4.1 parallel stands but is now secondary.** Discovery by file placement is objectionable
  because `2e` §6 forbids admission by presence, which is a sharper ground than the analogy to
  identity-from-address.

---

## Reading list before ruling

```
transformation/transformation/cli.py:685-750     construction_emit — the doctrine and the guard
transformation/transformation/build/render.py:985-1070   build_manifest and the derivation
transformation/transformation/build/generators.py:95-155 the generator, still registered
protocol_compiler/compile_domain.sh:43-44        the refusal when it is absent
.github/process/release.sh:143-160               how the gate enumerates domains
```
