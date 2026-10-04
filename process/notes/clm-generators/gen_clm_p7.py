"""Generate CLM CR-1 P7 design intent. Writes the dossier file.

Kept as evidence for lesson 3 of `../clm-process-check.md`: the CLM CR-1 dossier's P7 was written
by this script, not by hand, and nothing in the phase checks records that. It is the script as it ran.

Do not run it to regenerate the dossier. It writes over the dossier file in place. P7 was
edited by hand after generation — retrieval records the operation before reading the record — so a
rerun would silently revert that decision.
"""
from pathlib import Path

D = "causal_language_model"
OUT = Path("/Users/bp/protocol-governed-computing/business_domains/causal_language_model/cr_dossiers/"
           "cr_01_model_response/p7_design_intent_clm_model_response_v0.md")


def q(code): return f"{D}::{code}"


MUT, REG, APP = ("capability_side_effects::CS_MUTABLE_JSON_V0", "capability_side_effects::CS_REGISTRY_V0",
                 "capability_side_effects::CS_APPENDONLY_JSONL_V0")
ASSEMBLE, STRUCT, RULES, MEMBER, FILTER = (
    "capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0", "capability_transforms::CT_PURE_VALIDATE_RECORD_STRUCTURE_V0",
    "capability_transforms::CT_PURE_VALIDATE_PARAMETER_RULES_V0", "capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0",
    "capability_transforms::CT_PURE_FILTER_RECORDS_V0")
KINDS = "['public', 'internal', 'confidential', 'restricted']"
STRUCTURE = q("STRUCTURE_MODEL_RESPONSE_STORAGE_V0")
RB = q("RB_MODEL_RESPONSE_BINDINGS_V0")
SUB = "model_response"


def table(register, header, rows, flags="optional"):
    head = f"<!-- register:{register}{(' ' + flags) if flags else ''} -->"
    lines = [head, "| " + " | ".join(header) + " |", "|" + "|".join("-" * (len(h) + 2) for h in header) + "|"]
    if not rows:
        lines.append("| NONE IDENTIFIED |")
    for r in rows:
        lines.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(lines) + "\n"


out = []
w = out.append

w(f"""# Stage 7 — Design Intent: causal_language_model / model_response

**Stage:** 7 — Design Intent
**CR:** cr_01_model_response
**Status:** DRAFT
**Feeds:** Stage 8 — Authoring Mandate

Every binding names a field the capability declares, read from the pinned baseline
`3918d97c73a7431ecc9ef512938b34afa9028cd6e382626398750dca12defb1f`.

---

## 1. Design Decisions Resolution

""")
w(table("design_resolution", ["Decision", "Business Fact", "Resolution", "Source Finding"], [
    ("model_response is a new subdomain", "Nothing in the composition registers a model or governs how one writes",
     "A new subdomain of the causal_language_model namespace with its own two actors, five stores, one binding and five operations", "S4 design_decisions #1"),
    ("Writing is a molecule of two declared steps per pass", "The rules must act while the model writes, visibly to governance",
     "One pass is a molecule of the model's offer and the rules' choice; the response is a molecule whose loop runs one pass per position up to the longest response", "S4 design_decisions #2"),
    ("Determinism ends at the model's step", "A reader must see exactly where determinism ends",
     "Only the offer is declared ct_impure; the choice emits each pass's result, so nothing is decided on the model's offer", "S4 design_decisions #3"),
    ("A trace is reproduced from its record", "A user prompt's trace must be reproducible from what was recorded",
     "The platform records each offer where it is produced; the writing molecule's vectors state recorded offers and are proven by substituting them", "S4 design_decisions #4"),
    ("The seed is a recorded input", "Anyone reading the record can re-derive each chosen word",
     "The user prompt states a seed; it enters the rules in force, which the user prompt record keeps whole", "S4 design_decisions #5"),
    ("The test model is a realization of the model's step", "The rules must be shown to hold against a model that tries to break them",
     "The offer's implementation is the test model, which offers another customer's account number first", "S4 design_decisions #6"),
    ("The customer's account numbers travel with the user prompt", "The rule against another customer's account number is formed per user prompt",
     "The rules in force add one forbidden pattern, the account-number shape, excepting the customer's own numbers; every rule is read against the response so far joined to the candidate, so a number written across several words is stopped at the word that completes it", "S4 design_decisions #7"),
    ("Uniqueness by a formed key", "Two registrations with the same description and fingerprint are the same model",
     "A pure transform forms one key from the description and fingerprint; the registry claims it atomically, and ALREADY_EXISTS is the duplicate refusal", "S4 design_decisions #8"),
    ("State is data on the record", "A model moves into and out of service repeatedly",
     "The model record carries its state and its open time in service. Placement and withdrawal change the model's state only from the state they expect, in one conditional update, and refuse when it matched nothing; the time in service record is written after, so a failure between the two leaves a model no user prompt can reach rather than one answering under no rules", "S4 design_decisions #9"),
    ("Membership before order", "Membership is mechanism; the comparison is this subdomain's rule",
     "The stated kind is confirmed a declared kind, then compared with the ceiling by the declared order", "S4 design_decisions #10"),
    ("Retrieval raises no event", "Nothing reacts to a read",
     "Retrieval appends to the operation trail and declares no business moment", "S4 design_decisions #11"),
    ("Authorization is read, never granted", "Which staff are model staff and who may act for which customer is decided elsewhere",
     "The business's existing arrangements are the trusted source of who is model staff and whom a requester may act for; they assert both through the ingress, as the staff member's credentials and the requester's permitted customers, and model_response trusts that assertion and authenticates neither. The rules the credentials are checked against, and the schema a description is checked against, are fixed by this design and never supplied by the caller", "S4 design_decisions #12"),
    ("Every refusal is recorded with its reason", "Every user prompt is recorded, whether responded to or refused",
     "Each refusal routes to its own place in the submission, where the recording contract runs with that refusal's reason; a failure to write the response, or a store failing before the model reads, is recorded as FAILED with the stage. Not recorded: a payload the intent refuses, a second submission under a claimed identity, and a failure of the user prompt records themselves, which ends the act rejected and reports no record. A submission is traced by its user prompt record, which names the requester", "S4 constraint_register #9"),
    ("One identity, one record", "Each model the business holds has exactly one record",
     "A time in service and a user prompt are each claimed in their own register before anything is written under them; a duplicate is refused rather than overwriting or appending a second record", "S4 design_decisions #8"),
    ("The governed unit is a word", "A language model writes a response one word at a time",
     "Choosing, stopping and reading capacity are counted in words, which is exact for the test model and a simulation for a real one: a real model's tokens join this design only through a realization that offers whole words. A rule governs what its pattern can express and nothing else; the business does not claim a response is true", "S4 design_decisions #6"),
    ("How the seed draws an adventurous word", "Anyone reading the record can re-derive each chosen word",
     "The permitted candidates, most likely first and ties in offered order, are narrowed to the first freedom-plus-one; the word at position (seed plus the word's position) modulo that count is chosen. Freedom zero always chooses the most likely permitted word", "S4 design_decisions #5"),
    ("A finished response invokes no model", "An unfinished response is not a response",
     "The loop runs one pass per position to the longest response, as molecules run; once the response has finished or a rule has stopped it, the offer is handed that fact and returns no words without consulting the model, and the choice changes nothing", "S4 design_decisions #2"),
    ("The kinds of information are copied into three bindings", "The kinds are declared once, in order, least sensitive first",
     "A binding cannot read a vocabulary, so the ordered kinds are written as a literal where membership and order are checked, each copy identical to the vocabulary's entries in the same order", "S4 design_decisions #10"),
]))

w("""
---

## 2. Artifact Inventory — Existing Artifacts

""")
w(table("existing_inventory", ["FQDN", "Action (REPLACE, REUSE, EXTEND, REVIEW)", "Summary", "Reason", "Source Finding"], [
    (MUT, "REUSE", "", "Holds the model record and the time in service record, read and updated in place.", "S6 pps_artifacts_requiring_action capability_side_effects::CS_MUTABLE_JSON_V0"),
    (REG, "REUSE", "", "Register-if-absent gives the atomic claim duplicate prevention needs, on a key the subdomain forms.", "S6 pps_artifacts_requiring_action capability_side_effects::CS_REGISTRY_V0"),
    (APP, "REUSE", "", "Appends the user prompt record and the operation trail, neither of which can be amended.", "S6 pps_artifacts_requiring_action capability_side_effects::CS_APPENDONLY_JSONL_V0"),
    (ASSEMBLE, "REUSE", "", "Assembles the model, time in service and user prompt records from supplied values.", "S6 pps_artifacts_requiring_action capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0"),
    (STRUCT, "REUSE", "", "Reports what a model description lacks of the fields registration requires; a following rule refuses it when anything is reported.", "S6 pps_artifacts_requiring_action capability_transforms::CT_PURE_VALIDATE_RECORD_STRUCTURE_V0"),
    (RULES, "REUSE", "", "Confirms model staff credentials, a model's state and a response's release conditions against declared rules, and interprets each into a decision.", "S6 pps_artifacts_requiring_action capability_transforms::CT_PURE_VALIDATE_PARAMETER_RULES_V0"),
    (MEMBER, "REUSE", "", "Confirms a stated kind of information is a declared kind, and that a requester may act for the customer.", "S6 pps_artifacts_requiring_action capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0"),
    (FILTER, "REUSE", "", "Selects the one user prompt record retrieved, and interprets a record not found into a refusal.", "S6 ownership Append an entry to a trail that cannot be amended"),
    ("capability_transforms::CONSTITUTION_MOLECULES_V0", "REUSE", "", "Governs the two writing molecules and runs the loop's body once per pass.", "S6 pps_artifacts_requiring_action capability_transforms::CONSTITUTION_MOLECULES_V0"),
    ("capability_transforms::CONSTITUTION_NONDETERMINISTIC_ATOMS_V0", "REUSE", "", "Governs the model's offer: recorded when produced, replayed from the record, offered to a deterministic step.", "S6 pps_artifacts_requiring_action capability_transforms::CONSTITUTION_NONDETERMINISTIC_ATOMS_V0"),
], flags=""))

# ---------------------------------------------------------------- new artifacts
NEW = [  # capability, family, code, summary, source
    ("The authorized model staff member who registers, places, withdraws and retrieves", "AC", "AC_MODEL_STAFF_V0", "The actor whose authorization every model staff operation binds", "S5 provisional_codes AC_MODEL_STAFF_V0"),
    ("The authorized requester who submits a user prompt on behalf of a customer", "AC", "AC_REQUESTER_V0", "The actor who submits a user prompt for one customer", "S5 provisional_codes AC_REQUESTER_V0"),
    ("A request to register a model with its description and fingerprint", "IN", "IN_REGISTER_MODEL_V0", "A request to register a model with its description and fingerprint", "S5 provisional_codes IN_REGISTER_MODEL_V0"),
    ("A request to place a registered model in service with its ceiling, system prompt and response rules", "IN", "IN_PLACE_MODEL_IN_SERVICE_V0", "A request to place a registered model in service with its ceiling, system prompt and response rules", "S5 provisional_codes IN_PLACE_MODEL_IN_SERVICE_V0"),
    ("A request to withdraw a model from service", "IN", "IN_WITHDRAW_MODEL_FROM_SERVICE_V0", "A request to withdraw a model from service", "S5 provisional_codes IN_WITHDRAW_MODEL_FROM_SERVICE_V0"),
    ("A user prompt submitted on behalf of a customer", "IN", "IN_SUBMIT_USER_PROMPT_V0", "A user prompt submitted on behalf of a customer", "S5 provisional_codes IN_SUBMIT_USER_PROMPT_V0"),
    ("A request to retrieve the record of a user prompt", "IN", "IN_RETRIEVE_USER_PROMPT_RECORD_V0", "A request to retrieve the record of a user prompt", "S5 provisional_codes IN_RETRIEVE_USER_PROMPT_RECORD_V0"),
    ("Registering a model, refusing a second registration of the same model", "WF", "WF_REGISTER_MODEL_V0", "Registering a model, refusing a second registration of the same model", "S5 provisional_codes WF_REGISTER_MODEL_V0"),
    ("Opening a time in service for a registered model not already in service", "WF", "WF_PLACE_MODEL_IN_SERVICE_V0", "Opening a time in service for a registered model not already in service", "S5 provisional_codes WF_PLACE_MODEL_IN_SERVICE_V0"),
    ("Closing a model's time in service", "WF", "WF_WITHDRAW_MODEL_FROM_SERVICE_V0", "Closing a model's time in service", "S5 provisional_codes WF_WITHDRAW_MODEL_FROM_SERVICE_V0"),
    ("Admitting a user prompt, writing the response under the rules, releasing or refusing it, and recording it", "WF", "WF_SUBMIT_USER_PROMPT_V0", "Admitting a user prompt, writing the response under the rules, releasing or refusing it, and recording it", "S5 provisional_codes WF_SUBMIT_USER_PROMPT_V0"),
    ("Reading a user prompt record and recording that it was read", "WF", "WF_RETRIEVE_USER_PROMPT_RECORD_V0", "Reading a user prompt record and recording that it was read", "S5 provisional_codes WF_RETRIEVE_USER_PROMPT_RECORD_V0"),
    ("Confirm the staff member is model staff", "CC", "CC_CONFIRM_MODEL_STAFF_AUTHORIZED_V0", "Confirm the staff member is model staff", "S5 provisional_codes CC_CONFIRM_MODEL_STAFF_AUTHORIZED_V0"),
    ("Claim a user prompt's identity so a second submission under it is refused", "CC", "CC_CLAIM_USER_PROMPT_IDENTITY_V0", "Claim a user prompt's identity so a second submission under it is refused", "S5 provisional_codes CC_CLAIM_USER_PROMPT_IDENTITY_V0"),
    ("Confirm the requester may act for the customer the user prompt is for", "CC", "CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0", "Confirm the requester may act for the customer the user prompt is for", "S5 provisional_codes CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0"),
    ("Claim a model's identity so a second registration of the same model is refused", "CC", "CC_CLAIM_MODEL_IDENTITY_V0", "Claim a model's identity so a second registration of the same model is refused", "S5 provisional_codes CC_CLAIM_MODEL_IDENTITY_V0"),
    ("Record a model's description and fingerprint as its record, registered", "CC", "CC_REGISTER_MODEL_V0", "Record a model's description and fingerprint as its record, registered", "S5 provisional_codes CC_REGISTER_MODEL_V0"),
    ("Open a time in service with its ceiling, system prompt and response rules, and mark the model in service", "CC", "CC_PLACE_MODEL_IN_SERVICE_V0", "Open a time in service with its ceiling, system prompt and response rules, and mark the model in service", "S5 provisional_codes CC_PLACE_MODEL_IN_SERVICE_V0"),
    ("Close the time in service and mark the model registered", "CC", "CC_WITHDRAW_MODEL_FROM_SERVICE_V0", "Close the time in service and mark the model registered", "S5 provisional_codes CC_WITHDRAW_MODEL_FROM_SERVICE_V0"),
    ("Refuse a user prompt whose model is not registered or not in service", "CC", "CC_ADMIT_USER_PROMPT_V0", "Refuse a user prompt before the model sees it when its model is not registered or not in service", "S5 provisional_codes CC_ADMIT_USER_PROMPT_V0"),
    ("Refuse a user prompt whose kind of information is above the model's ceiling", "CC", "CC_CONFIRM_WITHIN_CEILING_V0", "Refuse a user prompt before the model sees it when it states a kind more sensitive than the ceiling", "S5 provisional_codes CC_ADMIT_USER_PROMPT_V0"),
    ("Refuse a user prompt longer than the model can read at once", "CC", "CC_CONFIRM_READING_FITS_V0", "Assemble exactly what the model reads and refuse it before the model sees it when it is too long", "S5 provisional_codes CC_ADMIT_USER_PROMPT_V0"),
    ("Write the response word by word under the rules in force", "CC", "CC_WRITE_MODEL_RESPONSE_V0", "Form the rules in force and write the response word by word under them", "S5 provisional_codes CC_WRITE_MODEL_RESPONSE_V0"),
    ("Release a written response only when it finished and no rule stopped it", "CC", "CC_CONFIRM_RESPONSE_RELEASABLE_V0", "Confirm one release condition of a written response, refusing it otherwise", "S5 provisional_codes CC_WRITE_MODEL_RESPONSE_V0"),
    ("Append the user prompt record with what the model read, the rules in force and the outcome", "CC", "CC_RECORD_USER_PROMPT_V0", "Append the user prompt record with what the model read, the rules in force and the outcome", "S5 provisional_codes CC_RECORD_USER_PROMPT_V0"),
    ("Read the record of a user prompt", "CC", "CC_RETRIEVE_USER_PROMPT_RECORD_V0", "Read the record of a user prompt", "S5 provisional_codes CC_RETRIEVE_USER_PROMPT_RECORD_V0"),
    ("Append a durable account of a performed operation to the subdomain's own trail", "CC", "CC_APPEND_MODEL_OPERATION_V0", "Append a durable account of a performed operation to the subdomain's own trail", "S5 provisional_codes CC_APPEND_MODEL_OPERATION_V0"),
    ("Form the single key claimed for a model from its description and fingerprint", "CT", "CT_PURE_FORM_MODEL_IDENTITY_KEY_V0", "Forms the single key claimed for a model from its description and fingerprint", "S5 provisional_codes CT_PURE_FORM_MODEL_IDENTITY_KEY_V0"),
    ("Decide whether a kind of information is no more sensitive than a ceiling", "CT", "CT_PURE_COMPARE_SENSITIVITY_V0", "Decides whether a kind of information is no more sensitive than a ceiling, by the declared order", "S5 provisional_codes CT_PURE_COMPARE_SENSITIVITY_V0"),
    ("Assemble exactly what the model reads and decide whether it fits", "CT", "CT_PURE_ASSEMBLE_MODEL_READING_V0", "Assembles exactly what the model reads and decides whether it fits what the model can read at once", "S5 provisional_codes CT_PURE_ASSEMBLE_MODEL_READING_V0"),
    ("Form the response rules in force for one user prompt", "CT", "CT_PURE_FORM_RESPONSE_RULES_V0", "Forms the response rules in force for one user prompt from the time in service and the customer's account numbers", "S5 provisional_codes CT_PURE_FORM_RESPONSE_RULES_V0"),
    ("The model's offer of its next words", "CT", "CT_IMPURE_OFFER_NEXT_WORDS_V0", "The model's step: offers its next words given the response so far; the one step whose result is not determined by its inputs", "S5 provisional_codes CT_IMPURE_OFFER_NEXT_WORDS_V0"),
    ("Stop forbidden words and choose one permitted word", "CT", "CT_PURE_CHOOSE_PERMITTED_WORD_V0", "Stops forbidden words among those offered and chooses one permitted word under the freedom of word choice and a stated seed", "S5 provisional_codes CT_PURE_CHOOSE_PERMITTED_WORD_V0"),
    ("One pass of writing: the model's offer, then the rules' choice", "CT", "CT_WRITE_NEXT_WORD_V0", "One pass of writing, composed of the model's offer and the rules' choice", "S5 provisional_codes CT_WRITE_NEXT_WORD_V0"),
    ("Write a response one pass per word, up to the longest response", "CT", "CT_WRITE_RESPONSE_V0", "Writes a response by repeating one pass per word, up to the longest response, carrying the response so far and the words stopped", "S5 provisional_codes CT_WRITE_RESPONSE_V0"),
    ("The moment the business records a model", "EV", "EV_MODEL_REGISTERED_V0", "The moment the business records a model", "S5 provisional_codes EV_MODEL_REGISTERED_V0"),
    ("The moment a model is placed in service and a time in service begins", "EV", "EV_MODEL_SERVICE_STARTED_V0", "The moment a model is placed in service and a time in service begins", "S5 provisional_codes EV_MODEL_SERVICE_STARTED_V0"),
    ("The moment a model is withdrawn from service and its time in service ends", "EV", "EV_MODEL_SERVICE_ENDED_V0", "The moment a model is withdrawn from service and its time in service ends", "S5 provisional_codes EV_MODEL_SERVICE_ENDED_V0"),
    ("The moment a model response is released", "EV", "EV_USER_PROMPT_RESPONDED_V0", "The moment a model response is released", "S5 provisional_codes EV_USER_PROMPT_RESPONDED_V0"),
    ("The moment a user prompt yields no response", "EV", "EV_USER_PROMPT_REFUSED_V0", "The moment a user prompt yields no response", "S5 provisional_codes EV_USER_PROMPT_REFUSED_V0"),
    ("The kinds of information, least sensitive first", "VOCAB", "VOCAB_KIND_OF_INFORMATION_V0", "The kinds of information, least sensitive first: public, internal, confidential, restricted", "S5 provisional_codes VOCAB_KIND_OF_INFORMATION_V0"),
    ("Bind the subdomain's operations to the stores and mechanisms they use", "RB", "RB_MODEL_RESPONSE_BINDINGS_V0", "Binds every model response workflow to the mechanisms and stores it uses", "S5 provisional_codes RB_MODEL_RESPONSE_BINDINGS_V0"),
    ("Declare the stores the subdomain owns", "STRUCTURE", "STRUCTURE_MODEL_RESPONSE_STORAGE_V0", "Declares the seven stores the subdomain owns and the paths they occupy", "S5 provisional_codes STRUCTURE_MODEL_RESPONSE_STORAGE_V0"),
]
w("""
---

## 3. Artifact Family Mapping — New Artifacts

""")
w(table("new_artifacts", ["Capability", "Family (AC, IN, WF, RB, CC, CT, EV, VOCAB, STRUCTURE, TI, TE)", "Code", "Summary",
                          "Owner Subdomain", "Status", "Source Finding"],
        [(c, f, q(code), s, SUB, "NEW", src) for c, f, code, s, src in NEW], flags="business_language=capability"))

WFS = ["WF_REGISTER_MODEL_V0", "WF_PLACE_MODEL_IN_SERVICE_V0", "WF_WITHDRAW_MODEL_FROM_SERVICE_V0",
       "WF_SUBMIT_USER_PROMPT_V0", "WF_RETRIEVE_USER_PROMPT_RECORD_V0"]
w("""
---

## 4. Runtime Binding (RB) Declarations

""")
w(table("rb_declarations", ["RB Code", "Binds WF", "CS Bindings", "Storage Structure", "Source Finding"],
        [(RB, q(wf), f"{MUT}, {REG}, {APP}", STRUCTURE, "S6 storage_governance A durable record of every model the business holds") for wf in WFS], flags=""))

# ---------------------------------------------------------------- topology
STAFF = q("CC_CONFIRM_MODEL_STAFF_AUTHORIZED_V0")
APPEND = q("CC_APPEND_MODEL_OPERATION_V0")
RECORD = q("CC_RECORD_USER_PROMPT_V0")
RELEASE = q("CC_CONFIRM_RESPONSE_RELEASABLE_V0")
STORE_OUT = "VIOLATION -> EXIT_REJECTED; BACKEND_ERROR -> EXIT_REJECTED"

TOPO = []  # workflow, node, runs, type, routing, source


def node(wf, n, typ, routing, runs="", src=None):
    short = n.split("::")[-1]
    TOPO.append((q(wf), n, runs, typ, routing, src or (f"S7 new_artifacts {short}" if typ in ("IN", "CC") and not runs
                                                       else f"S7 new_artifacts {runs.split('::')[-1]}" if runs
                                                       else f"S7 execution_topology {wf}")))


def staff_flow(wf, intent, first):
    node(wf, q(intent), "IN", f"ACK -> {STAFF}; NACK -> EXIT_REJECTED")
    node(wf, STAFF, "CC", f"SUCCESS -> {first}; VIOLATION -> EXIT_REJECTED")


wf = "WF_REGISTER_MODEL_V0"
staff_flow(wf, "IN_REGISTER_MODEL_V0", q("CC_CLAIM_MODEL_IDENTITY_V0"))
node(wf, q("CC_CLAIM_MODEL_IDENTITY_V0"), "CC", f"SUCCESS -> {q('CC_REGISTER_MODEL_V0')}; ALREADY_EXISTS -> EXIT_REJECTED; {STORE_OUT}")
node(wf, q("CC_REGISTER_MODEL_V0"), "CC", f"SUCCESS -> {APPEND}; {STORE_OUT}")
node(wf, APPEND, "CC", f"SUCCESS -> EXIT_REGISTERED; {STORE_OUT}")
node(wf, "EXIT_REGISTERED", "EXIT_SUCCESS", "—")
node(wf, "EXIT_REJECTED", "EXIT", "—")

wf = "WF_PLACE_MODEL_IN_SERVICE_V0"
staff_flow(wf, "IN_PLACE_MODEL_IN_SERVICE_V0", q("CC_PLACE_MODEL_IN_SERVICE_V0"))
node(wf, q("CC_PLACE_MODEL_IN_SERVICE_V0"), "CC", f"SUCCESS -> {APPEND}; NOT_FOUND -> EXIT_REJECTED; ALREADY_EXISTS -> EXIT_REJECTED; {STORE_OUT}")
node(wf, APPEND, "CC", f"SUCCESS -> EXIT_PLACED; {STORE_OUT}")
node(wf, "EXIT_PLACED", "EXIT_SUCCESS", "—")
node(wf, "EXIT_REJECTED", "EXIT", "—")

wf = "WF_WITHDRAW_MODEL_FROM_SERVICE_V0"
staff_flow(wf, "IN_WITHDRAW_MODEL_FROM_SERVICE_V0", q("CC_WITHDRAW_MODEL_FROM_SERVICE_V0"))
node(wf, q("CC_WITHDRAW_MODEL_FROM_SERVICE_V0"), "CC", f"SUCCESS -> {APPEND}; NOT_FOUND -> EXIT_REJECTED; {STORE_OUT}")
node(wf, APPEND, "CC", f"SUCCESS -> EXIT_WITHDRAWN; {STORE_OUT}")
node(wf, "EXIT_WITHDRAWN", "EXIT_SUCCESS", "—")
node(wf, "EXIT_REJECTED", "EXIT", "—")

wf = "WF_SUBMIT_USER_PROMPT_V0"
REQ = q("CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0")
ADMIT, CEIL, FITS, WRITE = (q("CC_ADMIT_USER_PROMPT_V0"), q("CC_CONFIRM_WITHIN_CEILING_V0"),
                            q("CC_CONFIRM_READING_FITS_V0"), q("CC_WRITE_MODEL_RESPONSE_V0"))
CLAIMUP = q("CC_CLAIM_USER_PROMPT_IDENTITY_V0")
node(wf, q("IN_SUBMIT_USER_PROMPT_V0"), "IN", f"ACK -> {CLAIMUP}; NACK -> EXIT_REJECTED")
node(wf, CLAIMUP, "CC", f"SUCCESS -> {REQ}; ALREADY_EXISTS -> EXIT_REJECTED; {STORE_OUT}")
node(wf, REQ, "CC", "SUCCESS -> " + ADMIT + "; VIOLATION -> RECORD_REFUSED_NOT_PERMITTED")
node(wf, ADMIT, "CC", f"SUCCESS -> {CEIL}; NOT_FOUND -> RECORD_REFUSED_NOT_REGISTERED; VIOLATION -> RECORD_REFUSED_NOT_IN_SERVICE; BACKEND_ERROR -> RECORD_FAILED_BEFORE_READING")
node(wf, CEIL, "CC", f"SUCCESS -> {FITS}; NOT_FOUND -> RECORD_REFUSED_NOT_IN_SERVICE; VIOLATION -> RECORD_REFUSED_ABOVE_CEILING; BACKEND_ERROR -> RECORD_FAILED_BEFORE_READING")
node(wf, FITS, "CC", f"SUCCESS -> {WRITE}; VIOLATION -> RECORD_REFUSED_TOO_LONG_TO_READ")
node(wf, WRITE, "CC", "SUCCESS -> CONFIRM_NO_RULE_STOPPED; VIOLATION -> RECORD_FAILED_WHILE_WRITING")
node(wf, "CONFIRM_NO_RULE_STOPPED", "CC", "SUCCESS -> CONFIRM_FINISHED; VIOLATION -> RECORD_REFUSED_BY_RULE", runs=RELEASE)
node(wf, "CONFIRM_FINISHED", "CC", "SUCCESS -> RECORD_RESPONDED; VIOLATION -> RECORD_REFUSED_UNFINISHED", runs=RELEASE)
node(wf, "RECORD_RESPONDED", "CC", f"SUCCESS -> EXIT_RESPONDED; {STORE_OUT}", runs=RECORD)
REFUSALS = ["NOT_PERMITTED", "NOT_REGISTERED", "NOT_IN_SERVICE", "ABOVE_CEILING", "TOO_LONG_TO_READ", "BY_RULE", "UNFINISHED"]
for r in REFUSALS:
    node(wf, f"RECORD_REFUSED_{r}", "CC", f"SUCCESS -> EXIT_REFUSED; {STORE_OUT}", runs=RECORD)
for r in ("BEFORE_READING", "WHILE_WRITING"):
    node(wf, f"RECORD_FAILED_{r}", "CC", f"SUCCESS -> EXIT_REJECTED; {STORE_OUT}", runs=RECORD)
node(wf, "EXIT_RESPONDED", "EXIT_SUCCESS", "—")
node(wf, "EXIT_REFUSED", "EXIT", "—")
node(wf, "EXIT_REJECTED", "EXIT", "—")

wf = "WF_RETRIEVE_USER_PROMPT_RECORD_V0"
RETR = q("CC_RETRIEVE_USER_PROMPT_RECORD_V0")
staff_flow(wf, "IN_RETRIEVE_USER_PROMPT_RECORD_V0", RETR)
node(wf, RETR, "CC", f"SUCCESS -> {APPEND}; VIOLATION -> EXIT_REJECTED; BACKEND_ERROR -> EXIT_REJECTED")
node(wf, APPEND, "CC", f"SUCCESS -> EXIT_RETRIEVED; {STORE_OUT}")
node(wf, "EXIT_RETRIEVED", "EXIT_SUCCESS", "—")
node(wf, "EXIT_REJECTED", "EXIT", "—")

w("""
---

## 5. Execution Topology

Every refusal of a submission is recorded before the act ends. The recording contract runs at eight
places in the submission, one per outcome, each handed its own outcome and reason; `Runs` names the
contract and `Node` names the place. The two release conditions run one contract at two places the
same way.

""")
w(table("execution_topology", ["Workflow", "Node", "Runs", "Node Type (IN, CC, EXIT, EXIT_SUCCESS)", "Routing", "Source Finding"],
        TOPO, flags="optional_columns=runs"))

# ---------------------------------------------------------------- composition
COMP = []  # cc, step#, name, capability, kind, op, store, consumes, produces, routing, interp, status, iface
BIND = []  # owner, step, dir, field, bound, source


def step(cc, n, name, cap, kind, op, store, consumes, produces, routing, status, iface="—", interp="—"):
    COMP.append((q(cc), n, name, cap, kind, op, store, consumes, produces, routing, interp, status, iface))


def b(owner, st, direction, field, bound, src=None):
    BIND.append((owner, st, direction, field, bound, src or f"S7 cc_composition {st}" if not owner.split("::")[-1].startswith("WF_")
                 else src or f"S7 execution_topology {st.split('::')[-1]}"))


def cb(cc, st, direction, field, bound):
    b(q(cc), st, direction, field, bound, f"S7 cc_composition {st}")


# confirm model staff
cc = "CC_CONFIRM_MODEL_STAFF_AUTHORIZED_V0"
step(cc, 1, "confirm_authorization", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "staff_credentials, authorization_rules",
     "is_authorized", "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: parameters=staff_credentials, rules=authorization_rules; out: valid=is_authorized")
cb(cc, "confirm_authorization", "INPUT", "parameters", "inputs.staff_credentials")
cb(cc, "confirm_authorization", "INPUT", "rules", "inputs.authorization_rules")
cb(cc, "confirm_authorization", "OUTPUT", "is_authorized", "capability_result.valid")

# confirm requester
cc = "CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0"
step(cc, 1, "confirm_acts_for_customer", MEMBER, "CT", "VALIDATE_SET_MEMBERSHIP", "—", "customer_id, permitted_customers",
     "acts_for_customer", "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: value=customer_id, allowed_set=permitted_customers; out: is_member=acts_for_customer")
cb(cc, "confirm_acts_for_customer", "INPUT", "value", "inputs.customer_id")
cb(cc, "confirm_acts_for_customer", "INPUT", "allowed_set", "inputs.permitted_customers")
cb(cc, "confirm_acts_for_customer", "OUTPUT", "acts_for_customer", "capability_result.is_member")

# claim identity
cc = "CC_CLAIM_MODEL_IDENTITY_V0"
step(cc, 1, "validate_description", STRUCT, "CT", "VALIDATE_RECORD_STRUCTURE", "—", "description, description_schema", "violations",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: record=description, schema=description_schema; out: violations=violations")
step(cc, 2, "require_description_complete", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "violations", "valid",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: parameters=description_findings, rules=completeness_rules; out: valid=valid")
cb(cc, "validate_description", "INPUT", "record", "inputs.description")
cb(cc, "validate_description", "INPUT", "schema", "inputs.description_schema")
cb(cc, "validate_description", "OUTPUT", "violations", "capability_result.violations")
cb(cc, "require_description_complete", "INPUT", "parameters", "{'violations': '$.results.validate_description.violations'}")
cb(cc, "require_description_complete", "INPUT", "rules", "[{'field': 'violations', 'op': 'eq', 'value': []}]")
cb(cc, "require_description_complete", "OUTPUT", "valid", "capability_result.valid")
step(cc, 3, "form_identity_key", q("CT_PURE_FORM_MODEL_IDENTITY_KEY_V0"), "CT", "FORM_MODEL_IDENTITY_KEY", "—", "description, fingerprint",
     "identity_key", "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: description=description, fingerprint=fingerprint; out: identity_key=identity_key")
step(cc, 4, "claim_identity", REG, "CS", "REGISTER", "MODEL_IDENTITY_REGISTRY", "key, target_cs, target_ref", "address",
     "SUCCESS -> exit; ALREADY_EXISTS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "ALREADY_EXISTS")
cb(cc, "form_identity_key", "INPUT", "description", "inputs.description")
cb(cc, "form_identity_key", "INPUT", "fingerprint", "inputs.fingerprint")
cb(cc, "form_identity_key", "OUTPUT", "identity_key", "capability_result.identity_key")
cb(cc, "claim_identity", "INPUT", "key", "results.form_identity_key.identity_key")
cb(cc, "claim_identity", "INPUT", "target_cs", "CS_MUTABLE_JSON_V0")
cb(cc, "claim_identity", "INPUT", "target_ref", "MODELS")
cb(cc, "claim_identity", "OUTPUT", "address", "capability_result.address")
cb(cc, "claim_identity", "OUTPUT", "result_status", "result_status")

# register model
cc = "CC_REGISTER_MODEL_V0"
step(cc, 1, "assemble_model_record", ASSEMBLE, "CT", "ASSEMBLE_RECORD", "—", "identity_key, description, fingerprint", "model_record",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: fields=model_fields; out: record=model_record")
step(cc, 2, "write_model_record", MUT, "CS", "WRITE", "MODELS", "key, value", "result_status",
     "SUCCESS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
cb(cc, "assemble_model_record", "INPUT", "fields", "{'identity_key': '$.inputs.identity_key', 'description': '$.inputs.description', 'fingerprint': '$.inputs.fingerprint', 'state': 'REGISTERED', 'time_in_service_id': ''}")
cb(cc, "assemble_model_record", "OUTPUT", "model_record", "capability_result.record")
cb(cc, "write_model_record", "INPUT", "key", "inputs.identity_key")
cb(cc, "write_model_record", "INPUT", "value", "results.assemble_model_record.model_record")
cb(cc, "write_model_record", "OUTPUT", "result_status", "result_status")

# place in service
cc = "CC_PLACE_MODEL_IN_SERVICE_V0"
step(cc, 1, "read_model_record", MUT, "CS", "READ", "MODELS", "key", "model_record",
     "SUCCESS -> continue; NOT_FOUND -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "NOT_FOUND")
step(cc, 2, "require_registered", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "model_record", "valid",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: parameters=model_state, rules=state_rules; out: valid=valid")
step(cc, 3, "confirm_ceiling_declared", MEMBER, "CT", "VALIDATE_SET_MEMBERSHIP", "—", "ceiling", "ceiling_declared",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: value=ceiling, allowed_set=kinds; out: is_member=ceiling_declared")
step(cc, 4, "claim_time_in_service", REG, "CS", "REGISTER", "TIME_IN_SERVICE_REGISTRY", "key, target_cs, target_ref", "address",
     "SUCCESS -> continue; ALREADY_EXISTS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "ALREADY_EXISTS")
step(cc, 5, "mark_in_service", MUT, "CS", "UPDATE_WHERE", "MODELS", "filter, updates", "matched_keys, updated_count",
     "SUCCESS -> continue; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
step(cc, 6, "require_transition", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "updated_count", "valid",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: parameters=transition, rules=transition_rules; out: valid=valid")
step(cc, 7, "assemble_time_in_service", ASSEMBLE, "CT", "ASSEMBLE_RECORD", "—", "time_in_service_id, identity_key, ceiling, system_prompt, response_rules",
     "time_in_service", "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: fields=time_in_service_fields; out: record=time_in_service")
step(cc, 8, "write_time_in_service", MUT, "CS", "WRITE", "TIMES_IN_SERVICE", "key, value", "result_status",
     "SUCCESS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
cb(cc, "read_model_record", "INPUT", "key", "inputs.identity_key")
cb(cc, "read_model_record", "OUTPUT", "model_record", "capability_result.value")
cb(cc, "read_model_record", "OUTPUT", "result_status", "result_status")
cb(cc, "require_registered", "INPUT", "parameters", "{'state': '$.results.read_model_record.model_record.state'}")
cb(cc, "require_registered", "INPUT", "rules", "[{'field': 'state', 'op': 'eq', 'value': 'REGISTERED'}]")
cb(cc, "require_registered", "OUTPUT", "valid", "capability_result.valid")
cb(cc, "confirm_ceiling_declared", "INPUT", "value", "inputs.ceiling")
cb(cc, "confirm_ceiling_declared", "INPUT", "allowed_set", KINDS)
cb(cc, "confirm_ceiling_declared", "OUTPUT", "ceiling_declared", "capability_result.is_member")
cb(cc, "claim_time_in_service", "INPUT", "key", "inputs.time_in_service_id")
cb(cc, "claim_time_in_service", "INPUT", "target_cs", "CS_MUTABLE_JSON_V0")
cb(cc, "claim_time_in_service", "INPUT", "target_ref", "TIMES_IN_SERVICE")
cb(cc, "claim_time_in_service", "OUTPUT", "address", "capability_result.address")
cb(cc, "claim_time_in_service", "OUTPUT", "result_status", "result_status")
cb(cc, "mark_in_service", "INPUT", "filter", "{'identity_key': '$.inputs.identity_key', 'state': 'REGISTERED'}")
cb(cc, "mark_in_service", "INPUT", "updates", "{'state': 'IN_SERVICE', 'time_in_service_id': '$.inputs.time_in_service_id'}")
cb(cc, "mark_in_service", "OUTPUT", "matched_keys", "capability_result.matched_keys")
cb(cc, "mark_in_service", "OUTPUT", "updated_count", "capability_result.updated_count")
cb(cc, "mark_in_service", "OUTPUT", "result_status", "result_status")
cb(cc, "require_transition", "INPUT", "parameters", "{'updated_count': '$.results.mark_in_service.updated_count'}")
cb(cc, "require_transition", "INPUT", "rules", "[{'field': 'updated_count', 'op': 'eq', 'value': 1}]")
cb(cc, "require_transition", "OUTPUT", "valid", "capability_result.valid")
cb(cc, "assemble_time_in_service", "INPUT", "fields", "{'time_in_service_id': '$.inputs.time_in_service_id', 'identity_key': '$.inputs.identity_key', 'ceiling': '$.inputs.ceiling', 'system_prompt': '$.inputs.system_prompt', 'response_rules': '$.inputs.response_rules', 'state': 'OPEN'}")
cb(cc, "assemble_time_in_service", "OUTPUT", "time_in_service", "capability_result.record")
cb(cc, "write_time_in_service", "INPUT", "key", "inputs.time_in_service_id")
cb(cc, "write_time_in_service", "INPUT", "value", "results.assemble_time_in_service.time_in_service")
cb(cc, "write_time_in_service", "OUTPUT", "result_status", "result_status")

# withdraw
cc = "CC_WITHDRAW_MODEL_FROM_SERVICE_V0"
step(cc, 1, "read_model_record", MUT, "CS", "READ", "MODELS", "key", "model_record",
     "SUCCESS -> continue; NOT_FOUND -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "NOT_FOUND")
step(cc, 2, "require_in_service", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "model_record", "valid",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: parameters=model_state, rules=state_rules; out: valid=valid")
step(cc, 3, "mark_registered", MUT, "CS", "UPDATE_WHERE", "MODELS", "filter, updates", "matched_keys, updated_count",
     "SUCCESS -> continue; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
step(cc, 4, "require_transition", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "updated_count", "valid",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: parameters=transition, rules=transition_rules; out: valid=valid")
step(cc, 5, "close_time_in_service", MUT, "CS", "UPDATE", "TIMES_IN_SERVICE", "key, updates", "result_status",
     "SUCCESS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
cb(cc, "read_model_record", "INPUT", "key", "inputs.identity_key")
cb(cc, "read_model_record", "OUTPUT", "model_record", "capability_result.value")
cb(cc, "read_model_record", "OUTPUT", "result_status", "result_status")
cb(cc, "require_in_service", "INPUT", "parameters", "{'state': '$.results.read_model_record.model_record.state'}")
cb(cc, "require_in_service", "INPUT", "rules", "[{'field': 'state', 'op': 'eq', 'value': 'IN_SERVICE'}]")
cb(cc, "require_in_service", "OUTPUT", "valid", "capability_result.valid")
cb(cc, "mark_registered", "INPUT", "filter", "{'identity_key': '$.inputs.identity_key', 'state': 'IN_SERVICE'}")
cb(cc, "mark_registered", "INPUT", "updates", "{'state': 'REGISTERED', 'time_in_service_id': ''}")
cb(cc, "mark_registered", "OUTPUT", "matched_keys", "capability_result.matched_keys")
cb(cc, "mark_registered", "OUTPUT", "updated_count", "capability_result.updated_count")
cb(cc, "mark_registered", "OUTPUT", "result_status", "result_status")
cb(cc, "require_transition", "INPUT", "parameters", "{'updated_count': '$.results.mark_registered.updated_count'}")
cb(cc, "require_transition", "INPUT", "rules", "[{'field': 'updated_count', 'op': 'eq', 'value': 1}]")
cb(cc, "require_transition", "OUTPUT", "valid", "capability_result.valid")
cb(cc, "close_time_in_service", "INPUT", "key", "results.read_model_record.model_record.time_in_service_id")
cb(cc, "close_time_in_service", "INPUT", "updates", "{'state': 'CLOSED'}")
cb(cc, "close_time_in_service", "OUTPUT", "result_status", "result_status")

# claim user prompt identity
cc = "CC_CLAIM_USER_PROMPT_IDENTITY_V0"
step(cc, 1, "claim_user_prompt", REG, "CS", "REGISTER", "USER_PROMPT_REGISTRY", "key, target_cs, target_ref", "address",
     "SUCCESS -> exit; ALREADY_EXISTS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "ALREADY_EXISTS")
cb(cc, "claim_user_prompt", "INPUT", "key", "inputs.user_prompt_id")
cb(cc, "claim_user_prompt", "INPUT", "target_cs", "CS_APPENDONLY_JSONL_V0")
cb(cc, "claim_user_prompt", "INPUT", "target_ref", "USER_PROMPT_RECORDS")
cb(cc, "claim_user_prompt", "OUTPUT", "address", "capability_result.address")
cb(cc, "claim_user_prompt", "OUTPUT", "result_status", "result_status")

# admit
cc = "CC_ADMIT_USER_PROMPT_V0"
step(cc, 1, "read_model_record", MUT, "CS", "READ", "MODELS", "key", "model_record",
     "SUCCESS -> continue; NOT_FOUND -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "NOT_FOUND")
step(cc, 2, "require_in_service", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "model_record", "valid",
     "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: parameters=model_state, rules=state_rules; out: valid=valid")
cb(cc, "read_model_record", "INPUT", "key", "inputs.identity_key")
cb(cc, "read_model_record", "OUTPUT", "model_record", "capability_result.value")
cb(cc, "read_model_record", "OUTPUT", "result_status", "result_status")
cb(cc, "require_in_service", "INPUT", "parameters", "{'state': '$.results.read_model_record.model_record.state'}")
cb(cc, "require_in_service", "INPUT", "rules", "[{'field': 'state', 'op': 'eq', 'value': 'IN_SERVICE'}]")
cb(cc, "require_in_service", "OUTPUT", "valid", "capability_result.valid")

# within ceiling
cc = "CC_CONFIRM_WITHIN_CEILING_V0"
step(cc, 1, "read_time_in_service", MUT, "CS", "READ", "TIMES_IN_SERVICE", "key", "time_in_service",
     "SUCCESS -> continue; NOT_FOUND -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "NOT_FOUND")
step(cc, 2, "confirm_kind_declared", MEMBER, "CT", "VALIDATE_SET_MEMBERSHIP", "—", "kind", "kind_declared",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: value=kind, allowed_set=kinds; out: is_member=kind_declared")
step(cc, 3, "compare_sensitivity", q("CT_PURE_COMPARE_SENSITIVITY_V0"), "CT", "COMPARE_SENSITIVITY", "—", "kind, time_in_service",
     "within_ceiling", "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: kind=kind, ceiling=ceiling, kinds=kinds; out: within_ceiling=within_ceiling")
cb(cc, "read_time_in_service", "INPUT", "key", "inputs.time_in_service_id")
cb(cc, "read_time_in_service", "OUTPUT", "time_in_service", "capability_result.value")
cb(cc, "read_time_in_service", "OUTPUT", "result_status", "result_status")
cb(cc, "confirm_kind_declared", "INPUT", "value", "inputs.kind")
cb(cc, "confirm_kind_declared", "INPUT", "allowed_set", KINDS)
cb(cc, "confirm_kind_declared", "OUTPUT", "kind_declared", "capability_result.is_member")
cb(cc, "compare_sensitivity", "INPUT", "kind", "inputs.kind")
cb(cc, "compare_sensitivity", "INPUT", "ceiling", "results.read_time_in_service.time_in_service.ceiling")
cb(cc, "compare_sensitivity", "INPUT", "kinds", KINDS)
cb(cc, "compare_sensitivity", "OUTPUT", "within_ceiling", "capability_result.within_ceiling")

# reading fits
cc = "CC_CONFIRM_READING_FITS_V0"
step(cc, 1, "assemble_reading", q("CT_PURE_ASSEMBLE_MODEL_READING_V0"), "CT", "ASSEMBLE_MODEL_READING", "—",
     "system_prompt, question, supporting_material, reading_capacity", "reading, reading_length",
     "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS",
     "in: system_prompt=system_prompt, question=question, supporting_material=supporting_material, reading_capacity=reading_capacity; out: reading=reading, reading_length=reading_length")
for f in ("system_prompt", "question", "supporting_material", "reading_capacity"):
    cb(cc, "assemble_reading", "INPUT", f, f"inputs.{f}")
cb(cc, "assemble_reading", "OUTPUT", "reading", "capability_result.reading")
cb(cc, "assemble_reading", "OUTPUT", "reading_length", "capability_result.reading_length")

# write response
cc = "CC_WRITE_MODEL_RESPONSE_V0"
step(cc, 1, "form_rules_in_force", q("CT_PURE_FORM_RESPONSE_RULES_V0"), "CT", "FORM_RESPONSE_RULES", "—",
     "response_rules, account_numbers, seed", "rules_in_force, positions", "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS",
     "in: response_rules=response_rules, account_numbers=account_numbers, seed=seed; out: rules_in_force=rules_in_force, positions=positions")
step(cc, 2, "write_response", q("CT_WRITE_RESPONSE_V0"), "CT", "WRITE_RESPONSE", "—", "reading, rules_in_force, positions",
     "written_response", "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS",
     "in: reading=reading, rules_in_force=rules_in_force, positions=positions; out: result=written_response")
cb(cc, "form_rules_in_force", "INPUT", "response_rules", "inputs.response_rules")
cb(cc, "form_rules_in_force", "INPUT", "account_numbers", "inputs.account_numbers")
cb(cc, "form_rules_in_force", "INPUT", "seed", "inputs.seed")
cb(cc, "form_rules_in_force", "OUTPUT", "rules_in_force", "capability_result.rules_in_force")
cb(cc, "form_rules_in_force", "OUTPUT", "positions", "capability_result.positions")
cb(cc, "write_response", "INPUT", "reading", "inputs.reading")
cb(cc, "write_response", "INPUT", "rules_in_force", "results.form_rules_in_force.rules_in_force")
cb(cc, "write_response", "INPUT", "positions", "results.form_rules_in_force.positions")
cb(cc, "write_response", "OUTPUT", "written_response", "capability_result.result")

# releasable
cc = "CC_CONFIRM_RESPONSE_RELEASABLE_V0"
step(cc, 1, "confirm_releasable", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "release_facts, release_rules", "releasable",
     "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: parameters=release_facts, rules=release_rules; out: valid=releasable")
cb(cc, "confirm_releasable", "INPUT", "parameters", "inputs.release_facts")
cb(cc, "confirm_releasable", "INPUT", "rules", "inputs.release_rules")
cb(cc, "confirm_releasable", "OUTPUT", "releasable", "capability_result.valid")

# record user prompt
RECORD_FIELDS = ["user_prompt_id", "requester_id", "customer_id", "identity_key", "kind", "question", "supporting_material",
                 "outcome", "time_in_service_id", "reading", "rules_in_force", "response", "reason"]
cc = "CC_RECORD_USER_PROMPT_V0"
step(cc, 1, "assemble_user_prompt_record", ASSEMBLE, "CT", "ASSEMBLE_RECORD", "—", ", ".join(RECORD_FIELDS), "user_prompt_record",
     "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: fields=user_prompt_fields; out: record=user_prompt_record")
step(cc, 2, "append_user_prompt_record", APP, "CS", "APPEND", "USER_PROMPT_RECORDS", "record, stream_id, actor_id",
     "record_id, sequence_number", "SUCCESS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
cb(cc, "assemble_user_prompt_record", "INPUT", "fields", "{" + ", ".join(f"'{f}': '$.inputs.{f}'" for f in RECORD_FIELDS) + "}")
cb(cc, "assemble_user_prompt_record", "OUTPUT", "user_prompt_record", "capability_result.record")
cb(cc, "append_user_prompt_record", "INPUT", "record", "results.assemble_user_prompt_record.user_prompt_record")
cb(cc, "append_user_prompt_record", "INPUT", "stream_id", "inputs.user_prompt_id")
cb(cc, "append_user_prompt_record", "INPUT", "actor_id", "inputs.requester_id")
cb(cc, "append_user_prompt_record", "OUTPUT", "record_id", "capability_result.record_id")
cb(cc, "append_user_prompt_record", "OUTPUT", "sequence_number", "capability_result.sequence_number")

# retrieve
cc = "CC_RETRIEVE_USER_PROMPT_RECORD_V0"
step(cc, 1, "read_user_prompt_entries", APP, "CS", "GET_ALL", "USER_PROMPT_RECORDS", "stream_id", "entries",
     "SUCCESS -> continue; BACKEND_ERROR -> exit", "SUCCESS")
step(cc, 2, "select_user_prompt_record", FILTER, "CT", "FILTER_RECORDS", "—", "entries, record_criteria", "user_prompt_record",
     "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: source=entries, filter=record_criteria; out: extracted=user_prompt_record")
cb(cc, "read_user_prompt_entries", "INPUT", "stream_id", "inputs.user_prompt_id")
cb(cc, "read_user_prompt_entries", "OUTPUT", "entries", "capability_result.entries")
cb(cc, "read_user_prompt_entries", "OUTPUT", "result_status", "result_status")
cb(cc, "select_user_prompt_record", "INPUT", "source", "results.read_user_prompt_entries.entries")
cb(cc, "select_user_prompt_record", "INPUT", "filter", "{'stream_id': '$.inputs.user_prompt_id'}")
cb(cc, "select_user_prompt_record", "OUTPUT", "user_prompt_record", "capability_result.extracted")

# append operation
cc = "CC_APPEND_MODEL_OPERATION_V0"
step(cc, 1, "append_operation", APP, "CS", "APPEND", "MODEL_OPERATIONS", "record, stream_id, actor_id", "record_id, sequence_number",
     "SUCCESS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
cb(cc, "append_operation", "INPUT", "record", "inputs.record")
cb(cc, "append_operation", "INPUT", "stream_id", "MODEL_OPERATIONS")
cb(cc, "append_operation", "INPUT", "actor_id", "inputs.staff_id")
cb(cc, "append_operation", "OUTPUT", "record_id", "capability_result.record_id")
cb(cc, "append_operation", "OUTPUT", "sequence_number", "capability_result.sequence_number")


# ---------------------------------------------------------------- workflow node bindings
def wb(wf, st, field, bound):
    BIND.append((q(wf), st, "INPUT", field, bound, f"S7 execution_topology {st.split('::')[-1]}"))


def staff_bindings(wf, operation, subject):
    wb(wf, STAFF, "staff_credentials", "payload.staff_credentials")
    wb(wf, STAFF, "authorization_rules", "[{'field': 'role', 'op': 'eq', 'value': 'model_staff'}]")
    wb(wf, APPEND, "staff_id", "payload.staff_id")
    wb(wf, APPEND, "operation", operation)
    wb(wf, APPEND, "record", f"{{'operation': '{operation}', 'staff_id': '$.payload.staff_id', 'subject': '{subject}'}}")


wf = "WF_REGISTER_MODEL_V0"
staff_bindings(wf, "REGISTER_MODEL", "$.results.CC_CLAIM_MODEL_IDENTITY_V0.identity_key")
wb(wf, q("CC_CLAIM_MODEL_IDENTITY_V0"), "description", "payload.description")
wb(wf, q("CC_CLAIM_MODEL_IDENTITY_V0"), "fingerprint", "payload.fingerprint")
wb(wf, q("CC_CLAIM_MODEL_IDENTITY_V0"), "description_schema", "{'reading_capacity': {'type': 'integer', 'required': True}}")
wb(wf, q("CC_REGISTER_MODEL_V0"), "identity_key", "results.CC_CLAIM_MODEL_IDENTITY_V0.identity_key")
wb(wf, q("CC_REGISTER_MODEL_V0"), "description", "payload.description")
wb(wf, q("CC_REGISTER_MODEL_V0"), "fingerprint", "payload.fingerprint")

wf = "WF_PLACE_MODEL_IN_SERVICE_V0"
staff_bindings(wf, "PLACE_MODEL_IN_SERVICE", "$.payload.identity_key")
for f in ("identity_key", "time_in_service_id", "ceiling", "system_prompt", "response_rules"):
    wb(wf, q("CC_PLACE_MODEL_IN_SERVICE_V0"), f, f"payload.{f}")

wf = "WF_WITHDRAW_MODEL_FROM_SERVICE_V0"
staff_bindings(wf, "WITHDRAW_MODEL_FROM_SERVICE", "$.payload.identity_key")
wb(wf, q("CC_WITHDRAW_MODEL_FROM_SERVICE_V0"), "identity_key", "payload.identity_key")

wf = "WF_RETRIEVE_USER_PROMPT_RECORD_V0"
staff_bindings(wf, "RETRIEVE_USER_PROMPT_RECORD", "$.payload.user_prompt_id")
wb(wf, RETR, "user_prompt_id", "payload.user_prompt_id")

wf = "WF_SUBMIT_USER_PROMPT_V0"
wb(wf, CLAIMUP, "user_prompt_id", "payload.user_prompt_id")
wb(wf, REQ, "customer_id", "payload.customer_id")
wb(wf, REQ, "permitted_customers", "payload.permitted_customers")
wb(wf, ADMIT, "identity_key", "payload.identity_key")
wb(wf, CEIL, "time_in_service_id", "results.CC_ADMIT_USER_PROMPT_V0.model_record.time_in_service_id")
wb(wf, CEIL, "kind", "payload.kind")
wb(wf, FITS, "system_prompt", "results.CC_CONFIRM_WITHIN_CEILING_V0.time_in_service.system_prompt")
wb(wf, FITS, "question", "payload.question")
wb(wf, FITS, "supporting_material", "payload.supporting_material")
wb(wf, FITS, "reading_capacity", "results.CC_ADMIT_USER_PROMPT_V0.model_record.description.reading_capacity")
wb(wf, WRITE, "response_rules", "results.CC_CONFIRM_WITHIN_CEILING_V0.time_in_service.response_rules")
wb(wf, WRITE, "account_numbers", "payload.account_numbers")
wb(wf, WRITE, "seed", "payload.seed")
wb(wf, WRITE, "reading", "results.CC_CONFIRM_READING_FITS_V0.reading")
wb(wf, "CONFIRM_NO_RULE_STOPPED", "release_facts", "{'stopped_by': '$.results.CC_WRITE_MODEL_RESPONSE_V0.written_response.stopped_by'}")
wb(wf, "CONFIRM_NO_RULE_STOPPED", "release_rules", "[{'field': 'stopped_by', 'op': 'eq', 'value': 'none'}]")
wb(wf, "CONFIRM_FINISHED", "release_facts", "{'finished': '$.results.CC_WRITE_MODEL_RESPONSE_V0.written_response.finished'}")
wb(wf, "CONFIRM_FINISHED", "release_rules", "[{'field': 'finished', 'op': 'eq', 'value': True}]")

# what each recording place knows, by how far the submission got
ALWAYS = [("user_prompt_id", "payload.user_prompt_id"), ("requester_id", "payload.requester_id"),
          ("customer_id", "payload.customer_id"), ("identity_key", "payload.identity_key"), ("kind", "payload.kind"),
          ("question", "payload.question"), ("supporting_material", "payload.supporting_material")]
TIS = [("time_in_service_id", "results.CC_ADMIT_USER_PROMPT_V0.model_record.time_in_service_id")]
READ = [("reading", "results.CC_CONFIRM_READING_FITS_V0.reading")]
RULED = [("rules_in_force", "results.CC_WRITE_MODEL_RESPONSE_V0.rules_in_force")]
PLACES = {
    "RECORD_RESPONDED": ("RESPONDED", None, TIS + READ + RULED + [("response", "results.CC_WRITE_MODEL_RESPONSE_V0.written_response.text")]),
    "RECORD_REFUSED_NOT_PERMITTED": ("REFUSED", "requester_not_permitted_for_customer", []),
    "RECORD_REFUSED_NOT_REGISTERED": ("REFUSED", "model_not_registered", []),
    "RECORD_REFUSED_NOT_IN_SERVICE": ("REFUSED", "model_not_in_service", []),
    "RECORD_REFUSED_ABOVE_CEILING": ("REFUSED", "kind_above_sensitivity_ceiling", TIS),
    "RECORD_REFUSED_TOO_LONG_TO_READ": ("REFUSED", "reading_longer_than_model_can_read", TIS),
    "RECORD_REFUSED_BY_RULE": ("REFUSED", "results.CC_WRITE_MODEL_RESPONSE_V0.written_response.stopped_by", TIS + READ + RULED),
    "RECORD_REFUSED_UNFINISHED": ("REFUSED", "longest_response_reached", TIS + READ + RULED),
    "RECORD_FAILED_BEFORE_READING": ("FAILED", "store_failed_before_the_model_read", []),
    "RECORD_FAILED_WHILE_WRITING": ("FAILED", "writing_failed", TIS + READ),
}
for place, (outcome, reason, known) in PLACES.items():
    for f, src in ALWAYS + known:
        wb(wf, place, f, src)
    wb(wf, place, "outcome", outcome)
    if reason:
        wb(wf, place, "reason", reason)

w("""
---

## 6. Capability Composition

""")
w(table("cc_composition", ["CC Code", "Step", "Step Name", "Capability", "Kind (CT, CS)", "Operation", "Store", "Consumes", "Produces",
                           "Routing", "Interpreted By", "Semantic Status", "Interface"], COMP))
w("""
---

## 7. Step Bindings

""")
w(table("step_bindings", ["Owner", "Step", "Direction (INPUT, OUTPUT)", "Field", "Bound To", "Source Finding"], BIND))

# ---------------------------------------------------------------- interface fields
F = []


def f(art, direction, field, typ, meaning, required="YES", default=""):
    F.append((q(art), direction, field, typ, required, default, meaning))


M = {
    "staff_credentials": ("object", "Who is performing the operation and their role, as the business's existing arrangements assert it"),
    "authorization_rules": ("array", "The rules the staff member's credentials are checked against, fixed by this design"),
    "staff_id": ("string", "The staff member recorded against the operation in the operation trail"),
    "description": ("object", "How the model is built, including the amount of text it can read at once"),
    "description_schema": ("object", "The fields a model description must carry, fixed by this design"),
    "fingerprint": ("string", "The training fingerprint, the provider's claim"),
    "identity_key": ("string", "The key formed from a model's description and fingerprint"),
    "time_in_service_id": ("string", "The time in service's identity, claimed once at placement"),
    "ceiling": ("string", "The most sensitive kind of information the model may read"),
    "system_prompt": ("string", "The business's standing instructions to the model for its time in service"),
    "response_rules": ("object", "The forbidden words and patterns, the account-number shape, the freedom of word choice and the longest response"),
    "user_prompt_id": ("string", "The user prompt's identity, named by the requester and claimed once"),
    "requester_id": ("string", "The requester who submits the user prompt"),
    "permitted_customers": ("array", "The customers the requester may act for, as the business's existing arrangements state"),
    "customer_id": ("string", "The customer the user prompt is for"),
    "account_numbers": ("array", "The customer's own account numbers, from the business's existing records"),
    "kind": ("string", "The most sensitive kind of information the question and its material contain"),
    "question": ("string", "What the requester asks on the customer's behalf"),
    "supporting_material": ("string", "Material carried with the question for the model to read"),
    "seed": ("integer", "The seed each adventurous word choice is drawn from"),
}
INTENTS = {
    "IN_REGISTER_MODEL_V0": ["staff_credentials", "staff_id", "description", "fingerprint"],
    "IN_PLACE_MODEL_IN_SERVICE_V0": ["staff_credentials", "staff_id", "identity_key", "time_in_service_id",
                                     "ceiling", "system_prompt", "response_rules"],
    "IN_WITHDRAW_MODEL_FROM_SERVICE_V0": ["staff_credentials", "staff_id", "identity_key"],
    "IN_SUBMIT_USER_PROMPT_V0": ["user_prompt_id", "requester_id", "permitted_customers", "customer_id", "account_numbers",
                                 "identity_key", "kind", "question", "supporting_material", "seed"],
    "IN_RETRIEVE_USER_PROMPT_RECORD_V0": ["staff_credentials", "staff_id", "user_prompt_id"],
}
for art, fields in INTENTS.items():
    for fl in fields:
        f(art, "INPUT", fl, *M[fl])

CCF = {  # cc: (inputs, outputs[(name,type,meaning)])
    "CC_CONFIRM_MODEL_STAFF_AUTHORIZED_V0": (["staff_credentials", "authorization_rules"], [("is_authorized", "boolean", "Whether the staff member is model staff")]),
    "CC_CLAIM_USER_PROMPT_IDENTITY_V0": (["user_prompt_id"], [("address", "string", "Where the claimed identity resolves to")]),
    "CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0": (["customer_id", "permitted_customers"], [("acts_for_customer", "boolean", "Whether the requester may act for the customer")]),
    "CC_CLAIM_MODEL_IDENTITY_V0": (["description", "description_schema", "fingerprint"], [("identity_key", "string", M["identity_key"][1]), ("address", "string", "Where the claimed key resolves to")]),
    "CC_REGISTER_MODEL_V0": (["identity_key", "description", "fingerprint"], [("model_record", "object", "The model's record, registered")]),
    "CC_PLACE_MODEL_IN_SERVICE_V0": (["identity_key", "time_in_service_id", "ceiling", "system_prompt", "response_rules"], [("time_in_service", "object", "The time in service opened")]),
    "CC_WITHDRAW_MODEL_FROM_SERVICE_V0": (["identity_key"], [("model_record", "object", "The model's record as it stood before withdrawal")]),
    "CC_ADMIT_USER_PROMPT_V0": (["identity_key"], [("model_record", "object", "The record of the model the user prompt names, in service")]),
    "CC_CONFIRM_WITHIN_CEILING_V0": (["time_in_service_id", "kind"], [("time_in_service", "object", "The model's open time in service, with its ceiling, system prompt and response rules")]),
    "CC_CONFIRM_READING_FITS_V0": (["system_prompt", "question", "supporting_material", "reading_capacity"],
                                   [("reading", "object", "Exactly what the model reads"), ("reading_length", "integer", "How long what the model reads is, in words")]),
    "CC_WRITE_MODEL_RESPONSE_V0": (["response_rules", "account_numbers", "seed", "reading"],
                                   [("rules_in_force", "object", "The response rules in force for this user prompt, with its seed"),
                                    ("written_response", "object", "The response as written, whether it finished, the rule that stopped it and the words stopped")]),
    "CC_CONFIRM_RESPONSE_RELEASABLE_V0": (["release_facts", "release_rules"], [("releasable", "boolean", "Whether the condition for release holds")]),
    "CC_RECORD_USER_PROMPT_V0": (RECORD_FIELDS, [("record_id", "string", "The identity of the appended user prompt record"),
                                                 ("sequence_number", "integer", "The record's position in the user prompt records")]),
    "CC_RETRIEVE_USER_PROMPT_RECORD_V0": (["user_prompt_id"], [("user_prompt_record", "array", "The record of the user prompt")]),
    "CC_APPEND_MODEL_OPERATION_V0": (["record", "staff_id", "operation"], [("record_id", "string", "The identity of the appended trail entry"),
                                                                          ("sequence_number", "integer", "The entry's position in the trail")]),
}
EXTRA = {
    "reading_capacity": ("integer", "How many words the model can read at once; words, not a real model's tokens"),
    "release_facts": ("object", "The facts of the written response one release condition reads"),
    "release_rules": ("array", "The release condition, as a rule over those facts"),
    "outcome": ("string", "RESPONDED, REFUSED or FAILED"),
    "reading": ("object", "Exactly what the model read, when it read anything"),
    "rules_in_force": ("object", "The response rules in force, when the model wrote"),
    "response": ("string", "The model response released"),
    "reason": ("string", "Why the user prompt was refused, or where it failed"),
    "record": ("object", "The account of the performed operation"),
    "operation": ("string", "The operation performed"),
}
OPTIONAL = {"CC_RECORD_USER_PROMPT_V0": {"time_in_service_id", "reading", "rules_in_force", "response", "reason"}}
for cc, (ins, outs) in CCF.items():
    for fl in ins:
        typ, meaning = M.get(fl) or EXTRA[fl]
        f(cc, "INPUT", fl, typ, meaning, "NO" if fl in OPTIONAL.get(cc, set()) else "YES")
    for name, typ, meaning in outs:
        f(cc, "OUTPUT", name, typ, meaning)

CTF = {
    "CT_PURE_FORM_MODEL_IDENTITY_KEY_V0": ([("description", "object", M["description"][1]), ("fingerprint", "string", M["fingerprint"][1])],
                                           [("identity_key", "string", M["identity_key"][1])]),
    "CT_PURE_COMPARE_SENSITIVITY_V0": ([("kind", "string", "The kind of information stated"), ("ceiling", "string", M["ceiling"][1]),
                                        ("kinds", "array", "The declared kinds, least sensitive first")],
                                       [("within_ceiling", "boolean", "Whether the kind is no more sensitive than the ceiling")]),
    "CT_PURE_ASSEMBLE_MODEL_READING_V0": ([("system_prompt", "string", M["system_prompt"][1]), ("question", "string", M["question"][1]),
                                           ("supporting_material", "string", M["supporting_material"][1]),
                                           ("reading_capacity", "integer", EXTRA["reading_capacity"][1])],
                                          [("reading", "object", "Exactly what the model reads"), ("reading_length", "integer", "How long it is, in words")]),
    "CT_PURE_FORM_RESPONSE_RULES_V0": ([("response_rules", "object", M["response_rules"][1]), ("account_numbers", "array", M["account_numbers"][1]),
                                        ("seed", "integer", M["seed"][1])],
                                       [("rules_in_force", "object", "The forbidden rules, the freedom of word choice and the seed in force"),
                                        ("positions", "array", "One position per word up to the longest response")]),
    "CT_IMPURE_OFFER_NEXT_WORDS_V0": ([("reading", "object", "Exactly what the model reads"), ("text", "string", "The response so far"),
                                       ("finished", "boolean", "Whether the response has finished, in which case no word is offered"),
                                       ("stopped_by", "string", "The rule that stopped the response, in which case no word is offered")],
                                      [("candidates", "array", "The words the model offers next, each with its likelihood")]),
    "CT_PURE_CHOOSE_PERMITTED_WORD_V0": ([("candidates", "array", "The words offered, each with its likelihood"),
                                          ("rules_in_force", "object", "The response rules in force"), ("position", "integer", "Which word this is"),
                                          ("text", "string", "The response so far"), ("finished", "boolean", "Whether the response has finished"),
                                          ("stopped_by", "string", "The rule that left no permitted word, or none"),
                                          ("stopped", "array", "The words stopped so far, each with its position and rule")],
                                         [("text", "string", "The response so far, with the chosen word"),
                                          ("finished", "boolean", "Whether the chosen word ends the response"),
                                          ("stopped_by", "string", "The rule that left no permitted word, or none"),
                                          ("stopped", "array", "The words stopped so far, with those stopped this pass")]),
    "CT_WRITE_NEXT_WORD_V0": ([("reading", "object", "Exactly what the model reads"), ("rules_in_force", "object", "The response rules in force"),
                               ("position", "integer", "Which word this is"), ("text", "string", "The response so far"),
                               ("finished", "boolean", "Whether the response has finished"),
                               ("stopped_by", "string", "The rule that left no permitted word, or none"),
                               ("stopped", "array", "The words stopped so far")],
                              [("result", "object", "The response so far, whether it finished, the rule that stopped it and the words stopped")]),
    "CT_WRITE_RESPONSE_V0": ([("reading", "object", "Exactly what the model reads"), ("rules_in_force", "object", "The response rules in force"),
                              ("positions", "array", "One position per word up to the longest response")],
                             [("result", "object", "The response as written, whether it finished, the rule that stopped it and the words stopped")]),
}
for ct, (ins, outs) in CTF.items():
    for name, typ, meaning in ins:
        f(ct, "INPUT", name, typ, meaning)
    for name, typ, meaning in outs:
        f(ct, "OUTPUT", name, typ, meaning)

EVF = {
    "EV_MODEL_REGISTERED_V0": ["identity_key", "staff_id"],
    "EV_MODEL_SERVICE_STARTED_V0": ["identity_key", "time_in_service_id", "staff_id"],
    "EV_MODEL_SERVICE_ENDED_V0": ["identity_key", "staff_id"],
    "EV_USER_PROMPT_RESPONDED_V0": ["user_prompt_id", "identity_key", "requester_id"],
    "EV_USER_PROMPT_REFUSED_V0": ["user_prompt_id", "identity_key", "requester_id"],
}
for ev, fields in EVF.items():
    for fl in fields:
        f(ev, "OUTPUT", fl, *M[fl])
f("AC_MODEL_STAFF_V0", "ATTRIBUTE", "staff_id", "string", "The staff member's identity as the business knows it")
f("AC_MODEL_STAFF_V0", "ATTRIBUTE", "authorized", "boolean", "Whether the staff member is model staff; decided by the business's existing arrangements, read here", "NO", "false")
f("AC_REQUESTER_V0", "ATTRIBUTE", "requester_id", "string", "The requester's identity as the business knows it")
f("AC_REQUESTER_V0", "ATTRIBUTE", "permitted_customers", "array", "The customers the requester may act for; decided by the business's existing arrangements, read here", "NO", "[]")

w("""
---

## 8. Interface Fields

""")
w(table("interface_fields", ["Artifact", "Direction (INPUT, OUTPUT, ATTRIBUTE)", "Field", "Type", "Required (YES, NO)", "Default", "Meaning"], F))

# ---------------------------------------------------------------- implementation
MOD = "causal_language_model.implementation.capability_transforms.atoms"
IMPL = [
    ("CT_PURE_FORM_MODEL_IDENTITY_KEY_V0", "FORM_MODEL_IDENTITY_KEY", "atom", "ct_pure", "never"),
    ("CT_PURE_COMPARE_SENSITIVITY_V0", "COMPARE_SENSITIVITY", "atom", "ct_pure", "raises"),
    ("CT_PURE_ASSEMBLE_MODEL_READING_V0", "ASSEMBLE_MODEL_READING", "atom", "ct_pure", "raises"),
    ("CT_PURE_FORM_RESPONSE_RULES_V0", "FORM_RESPONSE_RULES", "atom", "ct_pure", "never"),
    ("CT_IMPURE_OFFER_NEXT_WORDS_V0", "OFFER_NEXT_WORDS", "atom", "ct_impure", "never"),
    ("CT_PURE_CHOOSE_PERMITTED_WORD_V0", "CHOOSE_PERMITTED_WORD", "atom", "ct_pure", "returns"),
    ("CT_WRITE_NEXT_WORD_V0", "WRITE_NEXT_WORD", "molecule", "ct_impure", "returns"),
    ("CT_WRITE_RESPONSE_V0", "WRITE_RESPONSE", "molecule", "ct_impure", "returns"),
]
w("""
---

## 9. Implementation Bindings

The offer's implementation is the test model: it offers another customer's account number first, then
the words of the supporting material, then the end of the response, and nothing once the response has
finished or a rule has stopped it. A real model later joins it as a second realization of the same
declared step, offering whole words.

The choice stops a candidate when a forbidden rule's pattern matches the response so far joined to the
candidate by one space, at a match that reaches into the candidate, unless the matched characters with
spaces and dashes removed are among the rule's exceptions. It then chooses among the permitted
candidates, most likely first and ties in offered order: of the first freedom-plus-one, the one at
position (seed plus the word's position) modulo their count. The end marker `<end>` finishes the
response; any other word is appended after one space. When nothing is permitted, the rule that stopped
the most likely candidate is named and the response is left as it stood. `none` names no rule: the
response has not been stopped.

""")
w(table("implementation_bindings", ["CT Code", "Module", "Callable", "Operation", "Kind (atom, molecule)", "Purity (ct_pure, ct_impure)",
                                    "Refusal (raises, returns, never)", "Source Finding"],
        [(q(c), f"{MOD}.{c.lower()}" if k == "atom" else "", "execute" if k == "atom" else "", op, k, p, r, f"S7 new_artifacts {c}")
         for c, op, k, p, r in IMPL]))

w("""
---

## 10. Vocabulary Extensions

Every status this design routes on — ACK, NACK, SUCCESS, NOT_FOUND, ALREADY_EXISTS, VIOLATION,
BACKEND_ERROR — is already admitted. The one vocabulary authored is the kinds of information, in their
declared order.

""")
w(table("vocabulary_extensions", ["Vocabulary Code", "Extends", "Group", "Casing", "Value", "Meaning", "Source Finding"], [
    (q("VOCAB_KIND_OF_INFORMATION_V0"), "NONE", "kind_of_information", "lower_snake", v, m, "S5 provisional_codes VOCAB_KIND_OF_INFORMATION_V0")
    for v, m in [("public", "The least sensitive kind"), ("internal", "More sensitive than public"),
                 ("confidential", "More sensitive than internal"), ("restricted", "The most sensitive kind")]]))

w("""
---

## 11. Runtime Policies

""")
w(table("runtime_policies", ["RB Code", "Capability", "Key", "Value", "Source Finding"],
        [(RB, cs, "structure", STRUCTURE, "S7 rb_declarations RB_MODEL_RESPONSE_BINDINGS_V0") for cs in (MUT, REG, APP)]))

PROPS = [(q("AC_MODEL_STAFF_V0"), "type", "ENDUSER", "S5 provisional_codes AC_MODEL_STAFF_V0"),
         (q("AC_REQUESTER_V0"), "type", "ENDUSER", "S5 provisional_codes AC_REQUESTER_V0"),
         (q("WF_REGISTER_MODEL_V0"), "emit.EXIT_REGISTERED", q("EV_MODEL_REGISTERED_V0"), "S4 gap_register GAP-20"),
         (q("WF_PLACE_MODEL_IN_SERVICE_V0"), "emit.EXIT_PLACED", q("EV_MODEL_SERVICE_STARTED_V0"), "S4 gap_register GAP-20"),
         (q("WF_WITHDRAW_MODEL_FROM_SERVICE_V0"), "emit.EXIT_WITHDRAWN", q("EV_MODEL_SERVICE_ENDED_V0"), "S4 gap_register GAP-20"),
         (q("WF_SUBMIT_USER_PROMPT_V0"), "emit.EXIT_RESPONDED", q("EV_USER_PROMPT_RESPONDED_V0"), "S4 gap_register GAP-20"),
         (q("WF_SUBMIT_USER_PROMPT_V0"), "emit.EXIT_REFUSED", q("EV_USER_PROMPT_REFUSED_V0"), "S4 gap_register GAP-20"),
         (q("EV_USER_PROMPT_REFUSED_V0"), "moment", "refusal", "S0 business_events User Prompt Refused"),
         (STRUCTURE, "layer", "DOMAINS", "S5 provisional_codes STRUCTURE_MODEL_RESPONSE_STORAGE_V0")]
w("""
---

## 12. Artifact Properties

""")
w(table("artifact_properties", ["Artifact", "Property", "Value", "Source Finding"], PROPS))

w("""
---

## 13. STRUCTURE Stores

""")
w(table("structure_stores", ["Store Name", "Storage Type (CS_APPENDONLY_JSONL_V0, CS_MUTABLE_JSON_V0, CS_REGISTRY_V0)", "Proposed Path", "Used By", "Source Finding"], [
    ("MODELS", "CS_MUTABLE_JSON_V0", "causal_language_model/model_response/models.json", q("CC_REGISTER_MODEL_V0"), "S6 storage_governance A durable record of every model the business holds"),
    ("MODEL_IDENTITY_REGISTRY", "CS_REGISTRY_V0", "causal_language_model/model_response/model_identity_registry.jsonl", q("CC_CLAIM_MODEL_IDENTITY_V0"), "S6 storage_governance A claim on each model's identity, held once"),
    ("TIME_IN_SERVICE_REGISTRY", "CS_REGISTRY_V0", "causal_language_model/model_response/time_in_service_registry.jsonl", q("CC_PLACE_MODEL_IN_SERVICE_V0"), "S6 storage_governance A claim on each time in service's identity, held once"),
    ("USER_PROMPT_REGISTRY", "CS_REGISTRY_V0", "causal_language_model/model_response/user_prompt_registry.jsonl", q("CC_CLAIM_USER_PROMPT_IDENTITY_V0"), "S6 storage_governance A claim on each user prompt's identity, held once"),
    ("TIMES_IN_SERVICE", "CS_MUTABLE_JSON_V0", "causal_language_model/model_response/times_in_service.json", q("CC_PLACE_MODEL_IN_SERVICE_V0"), "S6 storage_governance A durable record of every time in service"),
    ("USER_PROMPT_RECORDS", "CS_APPENDONLY_JSONL_V0", "causal_language_model/model_response/user_prompt_records.jsonl", q("CC_RECORD_USER_PROMPT_V0"), "S6 storage_governance A record of every user prompt that cannot be amended"),
    ("MODEL_OPERATIONS", "CS_APPENDONLY_JSONL_V0", "causal_language_model/model_response/model_operations.jsonl", q("CC_APPEND_MODEL_OPERATION_V0"), "S6 storage_governance A trail of performed operations that cannot be amended"),
]))

w("""
---

## 14. Transport Bindings

""")
w(table("transport_bindings", ["Artifact", "Direction (INGRESS, EGRESS)", "Operation", "Handler Kind (WF_INVOCATION, SNAPSHOT_READ)", "Handler Target", "Field", "Bound To", "Source Finding"], []))

counts = {}
for _, fam, *_ in NEW:
    counts[fam] = counts.get(fam, 0) + 1
order = ["AC", "IN", "WF", "CC", "CT", "EV", "VOCAB", "RB", "STRUCTURE"]
w("""
## 15. Artifact Summary

""")
w(table("artifact_summary", ["Action (REPLACE, EXTEND, NEW)", "Subdomain", "Count", "Artifacts"],
        [("NEW", SUB, len(NEW), ", ".join(f"{counts[k]} {k}" for k in order))], flags=""))

w("""
---

## 16. Generation Provenance

*Every artifact this design schedules is authored: construction renders it from the registers
above and it is its own source of truth. Nothing here is reached by invoking a generator.*

""")
w(table("generation_provenance", ["Artifact", "Generator", "Generator Sources", "Source Finding"], []))

w("""
---

## 17. Declared Reach

Every act reads only what model_response owns.

""")
w(table("declared_reach", ["Act", "Consults", "Source Finding"], []))

SW = q("WF_SUBMIT_USER_PROMPT_V0")
DIS = [
    ("Register a model", "Its description and fingerprint match a registered model.", q("WF_REGISTER_MODEL_V0"), q("CC_CLAIM_MODEL_IDENTITY_V0"), "ALREADY_EXISTS", "S0 operation_refusals #1"),
    ("Place a model in service", "The model is not registered.", q("WF_PLACE_MODEL_IN_SERVICE_V0"), q("CC_PLACE_MODEL_IN_SERVICE_V0"), "NOT_FOUND", "S0 operation_refusals #2"),
    ("Place a model in service", "The model is already in service.", q("WF_PLACE_MODEL_IN_SERVICE_V0"), q("CC_PLACE_MODEL_IN_SERVICE_V0"), "VIOLATION", "S0 operation_refusals #3"),
    ("Withdraw a model from service", "The model is not in service.", q("WF_WITHDRAW_MODEL_FROM_SERVICE_V0"), q("CC_WITHDRAW_MODEL_FROM_SERVICE_V0"), "VIOLATION", "S0 operation_refusals #4"),
    ("Withdraw a model from service", "The model is not in service.", q("WF_WITHDRAW_MODEL_FROM_SERVICE_V0"), q("CC_WITHDRAW_MODEL_FROM_SERVICE_V0"), "NOT_FOUND", "S0 operation_refusals #4"),
    ("Submit a user prompt", "The model is not registered.", SW, "RECORD_REFUSED_NOT_REGISTERED", "SUCCESS", "S0 operation_refusals #5"),
    ("Submit a user prompt", "The model is not in service.", SW, "RECORD_REFUSED_NOT_IN_SERVICE", "SUCCESS", "S0 operation_refusals #6"),
    ("Submit a user prompt", "The user prompt contains a more sensitive kind of information than the model may read.", SW, "RECORD_REFUSED_ABOVE_CEILING", "SUCCESS", "S0 operation_refusals #7"),
    ("Submit a user prompt", "What the model would read is longer than the model can read at once.", SW, "RECORD_REFUSED_TOO_LONG_TO_READ", "SUCCESS", "S0 operation_refusals #8"),
    ("Submit a user prompt", "The requester is not permitted to act for the customer.", SW, "RECORD_REFUSED_NOT_PERMITTED", "SUCCESS", "S0 operation_refusals #9"),
    ("Submit a user prompt", "The model cannot finish a response without breaking a response rule.", SW, "RECORD_REFUSED_BY_RULE", "SUCCESS", "S0 operation_refusals #10"),
    ("Submit a user prompt", "The response reaches the longest response before it is finished.", SW, "RECORD_REFUSED_UNFINISHED", "SUCCESS", "S0 operation_refusals #11"),
] + [("Register a model, place in service, withdraw, retrieve a record", "The staff member is not authorized model staff.", q(wf), STAFF, "VIOLATION", "S0 operation_refusals #12")
     for wf in ("WF_REGISTER_MODEL_V0", "WF_PLACE_MODEL_IN_SERVICE_V0", "WF_WITHDRAW_MODEL_FROM_SERVICE_V0", "WF_RETRIEVE_USER_PROMPT_RECORD_V0")]
w("""
---

## 18. Refusal Discharge

A submission's refusal is discharged at the place that records it: that place's success ends the act
at `EXIT_REFUSED`, which refuses. The check that found the refusal routes there and nowhere else.

""")
w(table("refusal_discharge", ["Operation", "Refused When", "Act", "Step", "Outcome", "Source Finding"], DIS))

w("""
---

## 19. Refusal Deferrals

""")
w(table("refusal_deferrals", ["Operation", "Refused When", "Deferred To", "Until", "Source Finding"], []))
w("""
---

## 20. Refusal — Governance-Surface Discharge

""")
w(table("refusal_governance_discharge", ["Operation", "Refused When", "Phase", "Governing Rule", "Source Finding"], []))

PASS, WRESP = q("CT_WRITE_NEXT_WORD_V0"), q("CT_WRITE_RESPONSE_V0")
w("""
---

## 21. Molecule Steps

""")
w(table("molecule_steps", ["CT Code", "Step", "Kind (atom, molecule, loop)", "Target", "Over", "Iterator", "Emits", "Source Finding"], [
    (PASS, "offered", "atom", q("CT_IMPURE_OFFER_NEXT_WORDS_V0"), "—", "—", "—", "S4 design_decisions #2"),
    (PASS, "chosen", "atom", q("CT_PURE_CHOOSE_PERMITTED_WORD_V0"), "—", "—", "result", "S4 design_decisions #3"),
    (WRESP, "written", "loop", PASS, "inputs.positions", "position", "result", "S4 design_decisions #2"),
]))
MSB = [
    (PASS, "offered", "INPUT", "reading", "inputs.reading"),
    (PASS, "offered", "INPUT", "text", "inputs.text"),
    (PASS, "offered", "INPUT", "finished", "inputs.finished"),
    (PASS, "offered", "INPUT", "stopped_by", "inputs.stopped_by"),
    (PASS, "chosen", "INPUT", "candidates", "results.offered.candidates"),
    (PASS, "chosen", "INPUT", "rules_in_force", "inputs.rules_in_force"),
    (PASS, "chosen", "INPUT", "position", "inputs.position"),
    (PASS, "chosen", "INPUT", "text", "inputs.text"),
    (PASS, "chosen", "INPUT", "finished", "inputs.finished"),
    (PASS, "chosen", "INPUT", "stopped_by", "inputs.stopped_by"),
    (PASS, "chosen", "INPUT", "stopped", "inputs.stopped"),
    (WRESP, "written", "CARRY", "text", '""'),
    (WRESP, "written", "CARRY", "finished", "false"),
    (WRESP, "written", "CARRY", "stopped_by", "none"),
    (WRESP, "written", "CARRY", "stopped", "[]"),
    (WRESP, "written", "INPUT", "position", "iterator"),
    (WRESP, "written", "INPUT", "reading", "inputs.reading"),
    (WRESP, "written", "INPUT", "rules_in_force", "inputs.rules_in_force"),
    (WRESP, "written", "INPUT", "text", "accumulator.text"),
    (WRESP, "written", "INPUT", "finished", "accumulator.finished"),
    (WRESP, "written", "INPUT", "stopped_by", "accumulator.stopped_by"),
    (WRESP, "written", "INPUT", "stopped", "accumulator.stopped"),
    (WRESP, "written", "UPDATE", "text", "results.text"),
    (WRESP, "written", "UPDATE", "finished", "results.finished"),
    (WRESP, "written", "UPDATE", "stopped_by", "results.stopped_by"),
    (WRESP, "written", "UPDATE", "stopped", "results.stopped"),
]
w("""
---

## 22. Molecule Step Bindings

""")
w(table("molecule_step_bindings", ["CT Code", "Step", "Role (INPUT, CARRY, UPDATE)", "Field", "Bound To", "Source Finding"],
        [(*r, "S4 design_decisions #2") for r in MSB]))

# ---------------------------------------------------------------- vectors
TC, TV = [], []
ACCT = "'[0-9](?:[ -]?[0-9]){7}'"
FORBID = f"[{{rule: no_guarantees, pattern: '\\bguaranteed\\b'}}, {{rule: another_customers_account_number, pattern: {ACCT}, except: ['12345678']}}]"
RIF = f"{{forbidden: {FORBID}, freedom: 0, seed: 7}}"
RIF1 = f"{{forbidden: {FORBID}, freedom: 1, seed: 7}}"
READING = "{system_prompt: 'Answer briefly.', question: 'What is my balance?', supporting_material: 'Account 12345678 balance 40.'}"
STOP1 = "{position: 1, word: '87654321', rule: another_customers_account_number}"
NOTHING = [("INPUT", "finished", "false"), ("INPUT", "stopped_by", "none")]


def case(ct, name, outcome, values):
    TC.append((q(ct), name, outcome, "human decision"))
    for role, field, value in values:
        TV.append((q(ct), name, role, field, value, "human decision"))


def choose(name, candidates, rules, position, text, expected_text, finished, stopped_by, stopped):
    case("CT_PURE_CHOOSE_PERMITTED_WORD_V0", name, "SUCCESS", [
        ("INPUT", "candidates", candidates), ("INPUT", "rules_in_force", rules), ("INPUT", "position", str(position)),
        ("INPUT", "text", text), ("INPUT", "finished", "false"), ("INPUT", "stopped_by", "none"), ("INPUT", "stopped", "[]"),
        ("EXPECTED", "text", expected_text), ("EXPECTED", "finished", finished),
        ("EXPECTED", "stopped_by", stopped_by), ("EXPECTED", "stopped", stopped)])


case("CT_PURE_FORM_MODEL_IDENTITY_KEY_V0", "forms_key_from_description_and_fingerprint", "SUCCESS", [
    ("INPUT", "description", "{reading_capacity: 64, layers: 2}"),
    ("INPUT", "fingerprint", "sha256:ab12"),
    ("EXPECTED", "identity_key", "'{\"layers\":2,\"reading_capacity\":64}\\|sha256:ab12'"),
])
case("CT_PURE_FORM_MODEL_IDENTITY_KEY_V0", "refuses_blank_fingerprint", "VIOLATION", [
    ("INPUT", "description", "{reading_capacity: 64, layers: 2}"),
    ("INPUT", "fingerprint", "\" \""),
])
case("CT_PURE_COMPARE_SENSITIVITY_V0", "admits_kind_within_ceiling", "SUCCESS", [
    ("INPUT", "kind", "internal"), ("INPUT", "ceiling", "confidential"),
    ("INPUT", "kinds", "[public, internal, confidential, restricted]"),
    ("EXPECTED", "within_ceiling", "true"),
])
case("CT_PURE_COMPARE_SENSITIVITY_V0", "refuses_kind_above_ceiling", "VIOLATION", [
    ("INPUT", "kind", "restricted"), ("INPUT", "ceiling", "internal"),
    ("INPUT", "kinds", "[public, internal, confidential, restricted]"),
])
case("CT_PURE_ASSEMBLE_MODEL_READING_V0", "assembles_what_fits", "SUCCESS", [
    ("INPUT", "system_prompt", "Answer briefly."), ("INPUT", "question", "What is my balance?"),
    ("INPUT", "supporting_material", "Account 12345678 balance 40."), ("INPUT", "reading_capacity", "20"),
    ("EXPECTED", "reading", READING), ("EXPECTED", "reading_length", "10"),
])
case("CT_PURE_ASSEMBLE_MODEL_READING_V0", "refuses_reading_too_long", "VIOLATION", [
    ("INPUT", "system_prompt", "Answer briefly."), ("INPUT", "question", "What is my balance?"),
    ("INPUT", "supporting_material", "Account 12345678 balance 40."), ("INPUT", "reading_capacity", "5"),
])
case("CT_PURE_FORM_RESPONSE_RULES_V0", "adds_the_account_rule_and_positions", "SUCCESS", [
    ("INPUT", "response_rules", f"{{forbidden: [{{rule: no_guarantees, pattern: '\\bguaranteed\\b'}}], account_number_pattern: {ACCT}, freedom: 0, longest_response: 3}}"),
    ("INPUT", "account_numbers", "['12345678']"), ("INPUT", "seed", "7"),
    ("EXPECTED", "rules_in_force", RIF), ("EXPECTED", "positions", "[1, 2, 3]"),
])
case("CT_IMPURE_OFFER_NEXT_WORDS_V0", "offers_candidates", "SUCCESS", [
    ("INPUT", "reading", READING), ("INPUT", "text", "\"\""), *NOTHING,
    ("ASSERT", "candidates", "{mode: property, type: non_zero}"),
])
choose("stops_another_customers_account_and_continues",
       "[{word: '87654321', likelihood: 0.6}, {word: Your, likelihood: 0.3}]", RIF, 1, "\"\"",
       "Your", "false", "none", f"[{STOP1}]")
choose("stops_an_account_number_written_across_two_words",
       "[{word: '4321', likelihood: 0.7}, {word: is, likelihood: 0.2}]", RIF, 3, "Account 8765",
       "Account 8765 is", "false", "none", "[{position: 3, word: '4321', rule: another_customers_account_number}]")
choose("writes_the_customers_own_account_across_two_words",
       "[{word: '5678', likelihood: 0.8}]", RIF, 3, "Account 1234",
       "Account 1234 5678", "false", "none", "[]")
choose("names_the_rule_when_no_permitted_word_remains",
       "[{word: '87654321', likelihood: 0.9}]", RIF, 1, "\"\"",
       "\"\"", "false", "another_customers_account_number", f"[{STOP1}]")
choose("draws_an_adventurous_word_from_the_seed",
       "[{word: balance, likelihood: 0.6}, {word: savings, likelihood: 0.3}, {word: loan, likelihood: 0.1}]", RIF1, 2, "Your",
       "Your savings", "false", "none", "[]")
choose("finishes_on_the_end_of_the_response",
       "[{word: <end>, likelihood: 0.9}]", RIF, 3, "Your balance",
       "Your balance", "true", "none", "[]")
case("CT_WRITE_NEXT_WORD_V0", "writes_one_permitted_word_from_a_recorded_offer", "SUCCESS", [
    ("INPUT", "reading", READING), ("INPUT", "rules_in_force", RIF), ("INPUT", "position", "1"), ("INPUT", "text", "\"\""),
    *NOTHING, ("INPUT", "stopped", "[]"),
    ("RECORDED", "offered", "{candidates: [{word: '87654321', likelihood: 0.6}, {word: Your, likelihood: 0.3}]}"),
    ("EXPECTED", "result", f"{{text: Your, finished: false, stopped_by: none, stopped: [{STOP1}]}}"),
])
case("CT_WRITE_RESPONSE_V0", "writes_a_finished_response_and_offers_nothing_after", "SUCCESS", [
    ("INPUT", "reading", READING), ("INPUT", "rules_in_force", RIF), ("INPUT", "positions", "[1, 2, 3, 4]"),
    ("RECORDED", "written[0]/offered", "{candidates: [{word: '87654321', likelihood: 0.6}, {word: Your, likelihood: 0.3}]}"),
    ("RECORDED", "written[1]/offered", "{candidates: [{word: balance, likelihood: 0.9}]}"),
    ("RECORDED", "written[2]/offered", "{candidates: [{word: <end>, likelihood: 0.9}]}"),
    ("RECORDED", "written[3]/offered", "{candidates: []}"),
    ("EXPECTED", "result", f"{{text: Your balance, finished: true, stopped_by: none, stopped: [{STOP1}]}}"),
])
case("CT_WRITE_RESPONSE_V0", "stops_unfinished_at_the_longest_response", "SUCCESS", [
    ("INPUT", "reading", READING), ("INPUT", "rules_in_force", RIF), ("INPUT", "positions", "[1]"),
    ("RECORDED", "written[0]/offered", "{candidates: [{word: Your, likelihood: 0.9}]}"),
    ("EXPECTED", "result", "{text: Your, finished: false, stopped_by: none, stopped: []}"),
])
w("""
---

## 23. Test Cases

""")
w(table("test_cases", ["CT Code", "Case", "Expected Outcome (SUCCESS, VIOLATION)", "Source Finding"], TC))
w("""
---

## 24. Test Case Values

""")
w(table("test_case_values", ["CT Code", "Case", "Role (INPUT, EXPECTED, ASSERT, RECORDED)", "Field", "Value", "Source Finding"], TV))

w("""
---

## gov_projection — Governed Handoff to Stage 8

| Direction | Fields |
|-----------|--------|
| **Consumes** ← Stage 6 | ownership · storage_governance · cross_subdomain_deps · pps_artifacts_requiring_action · boundary_rules · governance_outcome |
| **Emits** → Stage 8 | design_resolution · existing_inventory · new_artifacts · rb_declarations · execution_topology · cc_composition · step_bindings · interface_fields · implementation_bindings · vocabulary_extensions · runtime_policies · artifact_properties · structure_stores · artifact_summary · generation_provenance |
""")

OUT.write_text("\n".join(out) if False else "".join(x if x.endswith("\n") else x + "\n" for x in out))
print(OUT, len(NEW), "new;", len(TOPO), "topology rows;", len(BIND), "bindings;", len(F), "fields;", len(TC), "cases")
