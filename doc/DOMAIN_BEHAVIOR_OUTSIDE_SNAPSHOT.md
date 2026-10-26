# Business Domains: Behavior Outside the Snapshot

This report covers the four domains in `business_domains`: `ai_governance`, `blockchain`,
`book_library_mgmt`, and `causal_language_model`. A domain owns only one kind of code: its
capability transform atoms, 18 of them. This report asks three questions:

- Which business decisions do those atoms make that the sealed snapshot does not state?
- Which business facts reach a workflow from the caller, when the snapshot should supply them?
- Which declarations does the code contradict?

There are two categories:

- **A: oversight or shortcut.** The snapshot could carry the fact.
- **B: cannot live in the snapshot.** The behavior is an algorithm, a realization, or something
  external. The aim is to bound it and declare it.

Bindings were read from the sealed `snapshot/tokenized/<domain>/dispatch.json`.

---

## A. Oversight or shortcut

### A1. ai_governance: the caller supplies the policy
- **`WF_PROVISION_AI_LICENSING_V0`:** the license cap comes from the caller.
  - `CC_VALIDATE_ELIGIBILITY_V0` binds `cap ← $.payload.context.cap`.
  - Its step then passes `quota ← $.inputs.cap` to `CT_PURE_CHECK_QUOTA_AVAILABLE_V0`.
- **`WF_AUTO_RECLAIM_V0`:** the reclamation threshold comes from the caller.
  - It binds `threshold_days ← $.payload.threshold_days`.
- Either way, the caller decides the rule it is judged by. A request that sends `cap: 1000000`
  passes the check, and so does one that sends `threshold_days: 0`.
- **Fix:** declare the cap and the threshold as sealed values, for example a policy or layer
  artifact bound as a literal. Remove them from the IN contract.

### A2. ai_governance: the caller supplies facts the platform can determine
- `assigned_count`, `training_completed` and `last_active_date` all come from
  `$.payload.context`.
- **`assigned_count`:**
  - The platform can count it with `CS_REGISTRY` `COUNT`, or `LIST` over the license store.
  - As it stands, the caller states its own count.
- **`training_completed`:** a boolean the caller asserts about itself. No record of it is read.
- **`evaluation_date`:**
  - The caller chooses it, so a caller can date the evaluation into the future and reclaim early.
  - The atom correctly avoids reading the clock, but `CS_CLOCK_V0` exists to supply this date as
    a recorded effect.
- **Fix:**
  - Read the count and the activity date from the domain's stores.
  - Take the evaluation date from `CS_CLOCK_V0`.
  - Hold training status as a record that a governed act writes.

### A3. ai_governance: the audit records the caller's claim, not the computed value
- `WF_AUTO_RECLAIM_V0`, node `CC_APPEND_AUDIT_EVENT_RECLAIMED`, binds
  `days_inactive ← $.payload.context.days_inactive`.
- `CT_PURE_EVALUATE_INACTIVITY_V0` computes `days_inactive`, but the audit event ignores it. The
  record of why a license was revoked carries a number the caller supplied. That number may
  differ from the one the decision used.
- **Fix:** bind the value as `$.results.<CC_RECLAIM_UNUSED_LICENSE_V0>.days_inactive`, and declare
  it among that contract's outputs.

### A4. All 8 atoms declared `refusal: never` do refuse
- The atoms are:
  - `CT_PURE_FORM_BOOK_IDENTITY_KEY_V0`
  - `CT_PURE_FORM_WORK_IDENTITY_KEY_V0`
  - `CT_PURE_FORM_MODEL_IDENTITY_KEY_V0`
  - `CT_PURE_FORM_RESPONSE_RULES_V0`
  - `CT_PURE_GROUP_RECORDS_V0`
  - `CT_PURE_SELECT_RECORDS_V0`
  - `CT_PURE_DERIVE_WALLET_ADDRESS_V0`
  - `CT_IMPURE_OFFER_NEXT_WORDS_V0`
- Each one defines a local `CTExecutionError`. The runtime recognizes that class name as a
  refusal and routes it as `VIOLATION`.
- Some of these refusals only repeat type checks the input contract already declares. Others are
  **business rules that exist only in code:**
  - an identity key over 256 characters is refused, not truncated;
  - a title or author that is empty after normalization is refused;
  - key material that is not 64 bytes, or 65 with the `04` tag, is refused;
  - an invalid regex in the `response_rules` of a time in service is refused.
- **Fix:**
  - Change these declarations to `raises`, and name each refusal condition in the artifact.
  - Give each condition a refusing case in the test vectors.
  - Make the build check that every contract using these atoms routes `VIOLATION`.

### A5. A declared limit is copied into code
- **Key length:**
  - `MAX_KEY_LENGTH = 256` is hard-coded in the three identity-key atoms.
  - Its source is `max_key_length: 256` in `CS_REGISTRY_V0` and `CS_MUTABLE_JSON_V0`, in
    `software_governance`.
  - If the platform changes it, the atoms do not follow.
  - **Fix:** bind the limit into the atom as an input from the sealed CS configuration.
- **Sensitivity order:**
  - `CC_CONFIRM_WITHIN_CEILING_V0` writes the kinds out as a literal list
    (`public, internal, confidential, restricted`).
  - `VOCAB_KIND_OF_INFORMATION_V0` already declares the same order.
  - **Fix:** bind the vocabulary by reference, so there is one source.

### A6. Identity normalization is a business rule stated only in code
- Book and work keys apply three rules:
  - case-folding;
  - whitespace collapse;
  - escaping of `|`.
- Model keys apply two:
  - canonical JSON with sorted keys and no spaces;
  - stripping of the fingerprint.
- The docstrings call these "stated business facts", yet each artifact declares only the input
  types and `identity_key: string`.
- These rules decide which records count as duplicates.
- **Fix:** state the normalization in each artifact (fold, collapse, separator, escape), and add
  vectors that pin it down. Better still, make it one platform molecule. The book and work atoms
  copy the same `_text` function between them.

### A7. causal_language_model: the record vocabulary and response policy live in atoms
- **Record outcomes:**
  - `CT_PURE_READ_HOSTED_STATE_V0` hard-codes the record outcomes `WRITING`, `STEP`,
    `RESPONDED`, `REFUSED` and `FAILED`.
  - Those outcomes are the hosted-request state machine, and the workflows that write them
    declare them.
  - If an outcome is renamed or added, the reader silently misreads the trail.
- **Hard-coded strings:**
  - `<end>`, `none`, the rule name `another_customers_account_number`, and
    `numbers_from_the_reading` are fixed strings repeated across several atoms and the host.
- **Response limit:**
  - `limit = min(maximum_response_length, longest_response)` is response policy decided in the
    reader.
- **Silent defaults** (`rules.get("freedom", 0)`, `rules.get("seed", 0)`, and a candidate with no
  `likelihood` counting as `0`):
  - `CT_PURE_FORM_RESPONSE_RULES_V0` validates `freedom`, but the choose atoms re-default it.
- **Fix:**
  - Declare the record outcomes and the markers as a vocabulary, and bind them in.
  - Compute `limit` in a declared step.
  - Have the choose atoms refuse a missing `freedom` or `seed`, rather than default it.

### A8. book_library_mgmt: grouping and selection rules are undeclared
- **`CT_PURE_GROUP_RECORDS_V0`:**
  - A record that lacks the attribute is grouped under the key `""`, not dropped.
  - Groups come back in the order they were first seen.
  - Both are deliberate, but the artifact states neither.
- **`CT_PURE_SELECT_RECORDS_V0`:**
  - It matches on equality, combined with AND.
  - A record that is not an object is skipped silently, while `GROUP` refuses it.
  - The two atoms disagree, and neither declares its behavior.
- **Fix:** declare these semantics in the artifacts and their vectors, and make the two atoms
  treat a non-object record the same way.

---

## B. Cannot live in the snapshot (bound it and declare it)

### B1. Algorithms
- **Keccak-256 address derivation** (blockchain). The constants are part of the algorithm.
- **The stop-and-choose algorithm** (causal_language_model):
  - NFKC compatibility form;
  - the number and separator grammar;
  - grounding;
  - the `(seed + position) mod window` choice.
- These are what the transform is. The C1 limit applies: only the contract and the vectors govern
  them.
- **Keep:** but each one needs complete vectors. The token-choosing atom is 171 lines of policy
  that is hard to read, so its vectors carry the governance. Check that they cover:
  - grounding on and off;
  - a number split across tokens;
  - lookalike digits;
  - the exception list;
  - the length limit.

### B2. Policy data that is governed runtime state
- `WF_PLACE_MODEL_IN_SERVICE_V0` takes `ceiling` and `response_rules`, which include regex
  patterns, from the payload, and stores them as the model's time in service.
- This is proper operational data, written by a governed act and recorded. It does not have to be
  sealed.
- **Gap:** the act is bound to an actor, but the platform does not enforce authority. So any
  caller can place a model in service with an open ceiling and no rules.
- **Bound it:**
  - Seal the shape of a permitted time in service, such as a maximum ceiling and the required
    forbidden rules.
  - Admit the act only for an authorized principal, once the platform carries one.

### B3. The external model and its host
- `causal_language_model/host/driver.py` is declared as outside PGC. Its rendering of the
  reading into a prompt (`OllamaModel.prompt`), the `top=5` candidates, and `temperature: 0` are
  all outside governance.
- A realistic boundary: the governed reading is sealed, but its rendering into model input is
  not. A host could add text that the governed record never shows.
- **Bound it:** record a digest of the rendered prompt in the opening entry. Alternatively,
  declare the rendering as a pure transform, so the record shows exactly what the model read.

### B4. The test model's adversarial behavior
- `CT_IMPURE_OFFER_NEXT_WORDS_V0` hard-codes `ANOTHER_CUSTOMERS_ACCOUNT = "87654321"`.
- It is a test realization of a step declared `ct_impure`, and replay records it. It is
  acceptable as it stands.

### B5. The blockchain browser client
- `blockchain/client` only presents. Its HTTP binding table (`bindings/http.json`) is not sealed;
  this is the platform-level gap from the earlier report.

---

## Priority

| # | Item | Why first |
|---|---|---|
| 1 | A1 caller-supplied cap and threshold | The caller sets the rule it is judged by |
| 2 | A3 audit records the caller's `days_inactive` | The evidence can contradict the decision |
| 3 | A2 caller-asserted count, training and date | The checks hold only if the caller tells the truth |
| 4 | A4 `refusal: never` contradicted by 8 atoms | Declared behavior is false; a refusal can reach a contract that does not route it |
| 5 | B2 authority over placing a model in service | Governed data, but anyone can write it |
| 6 | A5–A8 duplicated limits, undeclared normalization, hard-coded record vocabulary | Code and declarations drift apart without notice |
