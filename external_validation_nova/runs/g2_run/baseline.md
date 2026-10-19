# G2 baseline — the named frozen baseline for G4

`NPP-E` §9 requires a transformation's claims about the existing system to be **grounded against the
named frozen baseline**. This names it, before G4 begins, so that grounding has a fixed target
rather
than whatever the system happens to produce later.

```
snapshot:70dd9deaa723fa3d808d1bcc9d9171244a8e22378a7719961aadde3339dd80cb
family_revision: f476ea5c06506a3efba1d773a5d42818c9190601
profile: NPP-E
```

Constituent artifacts:

```
artifact:93386f38c741419fb48f2109a330ae57b399e3f575397616be5159bf6fc4800f
artifact:caa3ca8237644e5f8e27613d6b2cbb6f24966d6254d0c76be6f434528f00f237
```

**Reproduced twice from `python3 npp_e.py demo`, identical both times**, by a party that did not
build
the system. The identity is derived from content, so it can be recomputed rather than trusted —
which
is what makes it usable as a baseline at all.

**It was not recorded in any G2 deliverable.** `conformance_evidence.md` names the claim, the
profile
and the family revision, and does not state the snapshot identity the claim is about. That is a
small
gap in the evidence rather than in the system: a claim is against a subject, and the subject here
is a
snapshot that the evidence does not name.

Captured here so that G4 cannot silently ground against a moving target — and so that if the G2
system changes during G4, this remains what "the baseline" meant.
