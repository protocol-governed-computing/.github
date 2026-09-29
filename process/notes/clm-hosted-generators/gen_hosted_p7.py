"""Generate CLM cr_02_hosted_model P7 design intent. Writes the dossier file.

Kept as evidence under ruling C1: the dossier's P7 was written by this script. The phase checks admit
the document on what it says. Do not run it after P7 is approved; it writes over the dossier in place.
"""
from pathlib import Path

D = "causal_language_model"
OUT = Path("/Users/bp/protocol-governed-computing/business_domains/causal_language_model/cr_dossiers/"
           "cr_02_hosted_model/p7_design_intent_clm_hosted_model_v0.md")
BASELINE = "b8dd7145232e48f29575a00a5f056ba68930e1a34a7cf8aae5e3e6b23a02f1ef"


def q(code): return f"{D}::{code}"


MUT, REG, APP = ("capability_side_effects::CS_MUTABLE_JSON_V0", "capability_side_effects::CS_REGISTRY_V0",
                 "capability_side_effects::CS_APPENDONLY_JSONL_V0")
ASSEMBLE, RULES, MEMBER = ("capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0",
                           "capability_transforms::CT_PURE_VALIDATE_PARAMETER_RULES_V0",
                           "capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0")
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
**CR:** cr_02_hosted_model
**Status:** DRAFT
**Feeds:** Stage 8 — Authoring Mandate

Every binding names a field the capability declares, read from the pinned baseline
`{BASELINE}`.

The hosted way is three acts beside the test model's, which is not touched. The host drives them: it
begins a request on the requester's behalf, offers the model's candidates one step at a time, and asks
for release. The business chooses, records and releases. A hosted request's record trail is its state:
an opening entry at admission, a step entry per offer, and a closing entry on release or refusal.

---

## 1. Design Decisions Resolution

""")
w(table("design_resolution", ["Decision", "Business Fact", "Resolution", "Source Finding"], [
    ("One act per step, driven by the host", "The host proposes; the business chooses",
     "Three workflows: begin, offer, release. The host calls them; nothing in them calls the host", "S4 design_decisions #1"),
    ("Admission is the test model's", "A hosted request is admitted under the same conditions",
     "The begin act runs the four admission contracts and the reading check of the test model's way, unchanged and in the same order", "S4 design_decisions #2"),
    ("The reported size is checked with each offer", "The host counts what the model reads once it has it",
     "The offer act compares the size the host reports with the capacity recorded at admission before anything is chosen, and records the report with the step", "S4 design_decisions #3"),
    ("The trail is the state", "One truth for a hosted request; an abandoned one stays visible",
     "The opening entry holds what the model reads, the rules in force, the limits and the admitted fingerprint; each offer reads the trail and reduces it to the response as built; the existing record closes it", "S4 design_decisions #4"),
    ("Tokens are joined as they are", "A pattern split across tokens is not written",
     "A new choice transform applies the test model's stopping and choosing to the text as built, with the permitted length", "S4 design_decisions #5"),
    ("The permitted length is the smaller limit", "The registered maximum and the rules' longest response both bind",
     "The opening entry keeps both; the reduced state carries the smaller, and a token chosen at it that does not end the response refuses the request as unfinished", "S4 design_decisions #6"),
    ("The fingerprint is compared at every step", "An offer for another model is refused; the host is not authenticated",
     "The offer act confirms the offered fingerprint is the admitted model's before choosing", "S4 design_decisions #7"),
    ("Release closes the record with the business's text", "The host never supplies what is released",
     "The release act reads the trail, confirms the response complete, and records it with the text the trail holds", "S4 design_decisions #8"),
    ("Grounding is a rule of the time in service", "A time in service may require every number to be one the model read",
     "The opening entry carries the stored rules' grounding beside the rules in force; the choice stops a number no number in the reading begins, or ends one that is not in it", "S4 design_decisions #9"),
    ("A number's beginning is judged, and its lookalikes", "A pattern judged only when complete lets its beginning through",
     "The choice judges the compatibility form of the text, and stops the first digit of a forbidden number the model read unless it could still be a permitted one", "S4 design_decisions #10"),
]))

# ---------------------------------------------------------------- existing
REUSED_CC = ["CC_CLAIM_USER_PROMPT_IDENTITY_V0", "CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0", "CC_ADMIT_USER_PROMPT_V0",
             "CC_CONFIRM_WITHIN_CEILING_V0", "CC_CONFIRM_READING_FITS_V0", "CC_CONFIRM_RESPONSE_RELEASABLE_V0",
             "CC_RECORD_USER_PROMPT_V0"]
w("""
---

## 2. Artifact Inventory — Existing Artifacts

""")
w(table("existing_inventory", ["FQDN", "Action (REPLACE, REUSE, EXTEND, REVIEW)", "Summary", "Reason", "Source Finding"], [
    (APP, "REUSE", "", "Appends every entry of a hosted request's trail and reads the trail back.", "S6 pps_artifacts_requiring_action causal_language_model::STRUCTURE_MODEL_RESPONSE_STORAGE_V0"),
    (ASSEMBLE, "REUSE", "", "Assembles the opening and step entries of a hosted request's trail.", "S6 pps_artifacts_requiring_action causal_language_model::CC_RECORD_USER_PROMPT_V0"),
    (RULES, "REUSE", "", "Confirms the reported reading size against the capacity.", "S6 pps_artifacts_requiring_action causal_language_model::CC_CONFIRM_RESPONSE_RELEASABLE_V0"),
    (MEMBER, "REUSE", "", "Confirms an offer names the admitted model's fingerprint.", "S6 pps_artifacts_requiring_action causal_language_model::CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0"),
    *[(q(c), "REUSE", "", "Reused unchanged by the hosted acts.", f"S6 pps_artifacts_requiring_action {q(c)}") for c in REUSED_CC],
    (q("CT_PURE_FORM_RESPONSE_RULES_V0"), "REUSE", "", "Forms the rules in force when a hosted request's record opens.", f"S6 pps_artifacts_requiring_action {q('CT_PURE_FORM_RESPONSE_RULES_V0')}"),
    (RB, "REUSE", "", "Binds the hosted acts to the subdomain's stores, as it binds the test model's.", f"S6 pps_artifacts_requiring_action {RB}"),
    (STRUCTURE, "REUSE", "", "Declares the user prompt records the trail is kept in.", f"S6 pps_artifacts_requiring_action {STRUCTURE}"),
    (q("AC_REQUESTER_V0"), "REUSE", "", "The requester a hosted request is begun for.", f"S6 pps_artifacts_requiring_action {q('AC_REQUESTER_V0')}"),
    (q("EV_USER_PROMPT_RESPONDED_V0"), "REUSE", "", "Announced when a hosted response is released.", f"S6 pps_artifacts_requiring_action {q('EV_USER_PROMPT_RESPONDED_V0')}"),
    (q("EV_USER_PROMPT_REFUSED_V0"), "REUSE", "", "Announced when a hosted request is refused.", f"S6 pps_artifacts_requiring_action {q('EV_USER_PROMPT_REFUSED_V0')}"),
], flags=""))

# ---------------------------------------------------------------- new
NEW = [  # capability, family, code, summary, source
    ("The host of a model in service, which proposes and holds no authority", "AC", "AC_MODEL_HOST_V0", "The host of a model in service, which proposes and holds no authority", "S5 provisional_codes AC_MODEL_HOST_V0"),
    ("A request to a hosted model on behalf of a customer", "IN", "IN_BEGIN_HOSTED_RESPONSE_V0", "A request to a hosted model on behalf of a customer", "S5 provisional_codes IN_BEGIN_HOSTED_RESPONSE_V0"),
    ("The candidates a hosted model could write next, naming its fingerprint", "IN", "IN_OFFER_NEXT_TOKENS_V0", "The candidates a hosted model could write next, naming its fingerprint and the size of what it reads", "S5 provisional_codes IN_OFFER_NEXT_TOKENS_V0"),
    ("A request to release a completed hosted response", "IN", "IN_RELEASE_HOSTED_RESPONSE_V0", "A request to release a completed hosted response", "S5 provisional_codes IN_RELEASE_HOSTED_RESPONSE_V0"),
    ("Admitting a hosted request and opening its record, or refusing it", "WF", "WF_BEGIN_HOSTED_RESPONSE_V0", "Admitting a hosted request and opening its record, or refusing it", "S5 provisional_codes WF_BEGIN_HOSTED_RESPONSE_V0"),
    ("Choosing a permitted token from an offer and recording the step, or refusing the request", "WF", "WF_OFFER_NEXT_TOKENS_V0", "Choosing a permitted token from an offer and recording the step, or refusing the request", "S5 provisional_codes WF_OFFER_NEXT_TOKENS_V0"),
    ("Releasing a completed hosted response from the record", "WF", "WF_RELEASE_HOSTED_RESPONSE_V0", "Releasing a completed hosted response from the record", "S5 provisional_codes WF_RELEASE_HOSTED_RESPONSE_V0"),
    ("Refuse an offer whose reported reading size exceeds the model's capacity", "CC", "CC_CONFIRM_HOSTED_READING_FITS_V0", "Refuse an offer whose reported reading size exceeds the model's capacity", "S5 provisional_codes CC_CONFIRM_HOSTED_READING_FITS_V0"),
    ("Form the rules in force and open the record of a hosted request", "CC", "CC_OPEN_HOSTED_RECORD_V0", "Form the rules in force and open the record of a hosted request", "S5 provisional_codes CC_OPEN_HOSTED_RECORD_V0"),
    ("Read a hosted request's trail and reduce it to the response as built", "CC", "CC_READ_HOSTED_STATE_V0", "Read a hosted request's trail and reduce it to the response as built", "S5 provisional_codes CC_READ_HOSTED_STATE_V0"),
    ("Refuse an offer naming another model's fingerprint", "CC", "CC_CONFIRM_OFFER_FOR_MODEL_V0", "Refuse an offer naming another model's fingerprint", "S5 provisional_codes CC_CONFIRM_OFFER_FOR_MODEL_V0"),
    ("Choose a permitted token from an offer under the rules in force", "CC", "CC_CHOOSE_PERMITTED_TOKEN_V0", "Choose a permitted token from an offer under the rules in force", "S5 provisional_codes CC_CHOOSE_PERMITTED_TOKEN_V0"),
    ("Record an offer and the choice made from it in the request's trail", "CC", "CC_RECORD_HOSTED_STEP_V0", "Record an offer and the choice made from it in the request's trail", "S5 provisional_codes CC_RECORD_HOSTED_STEP_V0"),
    ("Reduce a hosted request's trail to its state", "CT", "CT_PURE_READ_HOSTED_STATE_V0", "Reduces a hosted request's trail to the response as built, its position, whether it is complete, and its permitted length", "S5 provisional_codes CT_PURE_READ_HOSTED_STATE_V0"),
    ("Stop forbidden tokens and choose a permitted one", "CT", "CT_PURE_CHOOSE_PERMITTED_TOKEN_V0", "Stops forbidden tokens among those offered and chooses one permitted token, joined as it is, within the permitted length", "S5 provisional_codes CT_PURE_CHOOSE_PERMITTED_TOKEN_V0"),
]
w("""
---

## 3. Artifact Family Mapping — New Artifacts

""")
w(table("new_artifacts", ["Capability", "Family (AC, IN, WF, RB, CC, CT, EV, VOCAB, STRUCTURE, TI, TE)", "Code", "Summary",
                          "Owner Subdomain", "Status", "Source Finding"],
        [(c, f, q(code), s, SUB, "NEW", src) for c, f, code, s, src in NEW], flags="business_language=capability"))

WFS = ["WF_BEGIN_HOSTED_RESPONSE_V0", "WF_OFFER_NEXT_TOKENS_V0", "WF_RELEASE_HOSTED_RESPONSE_V0"]
w("""
---

## 4. Runtime Binding (RB) Declarations

""")
w(table("rb_declarations", ["RB Code", "Binds WF", "CS Bindings", "Storage Structure", "Source Finding"],
        [(RB, q(wf), f"{MUT}, {REG}, {APP}", STRUCTURE, f"S6 pps_artifacts_requiring_action {RB}") for wf in WFS], flags=""))

# ---------------------------------------------------------------- topology
TOPO = []
STORE_OUT = "VIOLATION -> EXIT_REJECTED; BACKEND_ERROR -> EXIT_REJECTED"
RECORD, RELEASE = q("CC_RECORD_USER_PROMPT_V0"), q("CC_CONFIRM_RESPONSE_RELEASABLE_V0")
STEPREC = q("CC_RECORD_HOSTED_STEP_V0")


def node(wf, n, typ, routing, runs=""):
    short = (runs or n).split("::")[-1]
    src = f"S7 new_artifacts {short}" if typ in ("IN", "CC") else f"S7 execution_topology {wf}"
    TOPO.append((q(wf), n, runs, typ, routing, src))


CLAIM, REQ, ADMIT, CEIL, FITS = (q("CC_CLAIM_USER_PROMPT_IDENTITY_V0"), q("CC_CONFIRM_REQUESTER_ACTS_FOR_CUSTOMER_V0"),
                                 q("CC_ADMIT_USER_PROMPT_V0"), q("CC_CONFIRM_WITHIN_CEILING_V0"), q("CC_CONFIRM_READING_FITS_V0"))
OPEN, READST, HFITS, SAME, CHOOSE = (q("CC_OPEN_HOSTED_RECORD_V0"), q("CC_READ_HOSTED_STATE_V0"),
                                     q("CC_CONFIRM_HOSTED_READING_FITS_V0"), q("CC_CONFIRM_OFFER_FOR_MODEL_V0"),
                                     q("CC_CHOOSE_PERMITTED_TOKEN_V0"))

wf = "WF_BEGIN_HOSTED_RESPONSE_V0"
node(wf, q("IN_BEGIN_HOSTED_RESPONSE_V0"), "IN", f"ACK -> {CLAIM}; NACK -> EXIT_REJECTED")
node(wf, CLAIM, "CC", f"SUCCESS -> {REQ}; ALREADY_EXISTS -> EXIT_REJECTED; {STORE_OUT}")
node(wf, REQ, "CC", f"SUCCESS -> {ADMIT}; VIOLATION -> RECORD_REFUSED_NOT_PERMITTED")
node(wf, ADMIT, "CC", f"SUCCESS -> {CEIL}; NOT_FOUND -> RECORD_REFUSED_NOT_REGISTERED; VIOLATION -> RECORD_REFUSED_NOT_IN_SERVICE; BACKEND_ERROR -> EXIT_REJECTED")
node(wf, CEIL, "CC", f"SUCCESS -> {FITS}; NOT_FOUND -> RECORD_REFUSED_NOT_IN_SERVICE; VIOLATION -> RECORD_REFUSED_ABOVE_CEILING; BACKEND_ERROR -> EXIT_REJECTED")
node(wf, FITS, "CC", f"SUCCESS -> {OPEN}; VIOLATION -> RECORD_REFUSED_TOO_LONG_TO_READ")
node(wf, OPEN, "CC", f"SUCCESS -> EXIT_WRITING; {STORE_OUT}")
BEGIN_REFUSALS = ["NOT_PERMITTED", "NOT_REGISTERED", "NOT_IN_SERVICE", "ABOVE_CEILING", "TOO_LONG_TO_READ"]
for r in BEGIN_REFUSALS:
    node(wf, f"RECORD_REFUSED_{r}", "CC", f"SUCCESS -> EXIT_REFUSED; {STORE_OUT}", runs=RECORD)
node(wf, "EXIT_WRITING", "EXIT_SUCCESS", "—")
node(wf, "EXIT_REFUSED", "EXIT", "—")
node(wf, "EXIT_REJECTED", "EXIT", "—")

wf = "WF_OFFER_NEXT_TOKENS_V0"
node(wf, q("IN_OFFER_NEXT_TOKENS_V0"), "IN", f"ACK -> {READST}; NACK -> EXIT_REJECTED")
node(wf, READST, "CC", f"SUCCESS -> {SAME}; {STORE_OUT}")
node(wf, SAME, "CC", f"SUCCESS -> {HFITS}; VIOLATION -> RECORD_REFUSED_OTHER_MODEL")
node(wf, HFITS, "CC", f"SUCCESS -> {CHOOSE}; VIOLATION -> RECORD_REFUSED_TOO_LONG_TO_READ")
node(wf, CHOOSE, "CC", "SUCCESS -> CONFIRM_NO_RULE_STOPPED; VIOLATION -> EXIT_REJECTED")
node(wf, "CONFIRM_NO_RULE_STOPPED", "CC", "SUCCESS -> CONFIRM_WITHIN_LENGTH; VIOLATION -> RECORD_STOPPED_STEP", runs=RELEASE)
node(wf, "CONFIRM_WITHIN_LENGTH", "CC", "SUCCESS -> RECORD_STEP; VIOLATION -> RECORD_UNFINISHED_STEP", runs=RELEASE)
node(wf, "RECORD_STEP", "CC", f"SUCCESS -> EXIT_CHOSEN; {STORE_OUT}", runs=STEPREC)
node(wf, "RECORD_STOPPED_STEP", "CC", f"SUCCESS -> RECORD_REFUSED_BY_RULE; {STORE_OUT}", runs=STEPREC)
node(wf, "RECORD_UNFINISHED_STEP", "CC", f"SUCCESS -> RECORD_REFUSED_UNFINISHED; {STORE_OUT}", runs=STEPREC)
OFFER_REFUSALS = ["OTHER_MODEL", "TOO_LONG_TO_READ", "BY_RULE", "UNFINISHED"]
for r in OFFER_REFUSALS:
    node(wf, f"RECORD_REFUSED_{r}", "CC", f"SUCCESS -> EXIT_REFUSED; {STORE_OUT}", runs=RECORD)
node(wf, "EXIT_CHOSEN", "EXIT_SUCCESS", "—")
node(wf, "EXIT_REFUSED", "EXIT", "—")
node(wf, "EXIT_REJECTED", "EXIT", "—")

wf = "WF_RELEASE_HOSTED_RESPONSE_V0"
node(wf, q("IN_RELEASE_HOSTED_RESPONSE_V0"), "IN", f"ACK -> {READST}; NACK -> EXIT_REJECTED")
node(wf, READST, "CC", f"SUCCESS -> CONFIRM_FINISHED; {STORE_OUT}")
node(wf, "CONFIRM_FINISHED", "CC", "SUCCESS -> RECORD_RESPONDED; VIOLATION -> EXIT_REJECTED", runs=RELEASE)
node(wf, "RECORD_RESPONDED", "CC", f"SUCCESS -> EXIT_RESPONDED; {STORE_OUT}", runs=RECORD)
node(wf, "EXIT_RESPONDED", "EXIT_SUCCESS", "—")
node(wf, "EXIT_REJECTED", "EXIT", "—")

w("""
---

## 5. Execution Topology

Every refusal is recorded before the act ends: the existing recording contract runs at one place per
refusal, each handed its outcome and reason. In the offer act, a step the rules or the length stopped
is recorded first, so the trail keeps the offer that ended the request; the step recording contract
runs at three places for that. The releasability contract runs at two places in the offer act and one
in the release act, each with its own condition.

""")
w(table("execution_topology", ["Workflow", "Node", "Runs", "Node Type (IN, CC, EXIT, EXIT_SUCCESS)", "Routing", "Source Finding"],
        TOPO, flags="optional_columns=runs"))

# ---------------------------------------------------------------- composition
COMP, BIND = [], []


def step(cc, n, name, cap, kind, op, store, consumes, produces, routing, status, iface="—", interp="—"):
    COMP.append((q(cc), n, name, cap, kind, op, store, consumes, produces, routing, interp, status, iface))


def cb(cc, st, direction, field, bound):
    BIND.append((q(cc), st, direction, field, bound, f"S7 cc_composition {st}"))


cc = "CC_CONFIRM_HOSTED_READING_FITS_V0"
step(cc, 1, "confirm_reported_reading_fits", RULES, "CT", "VALIDATE_PARAMETER_RULES", "—", "reported_reading_size, reading_capacity",
     "reading_fits", "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: parameters=reported_reading_size, rules=reading_capacity; out: valid=reading_fits")
cb(cc, "confirm_reported_reading_fits", "INPUT", "parameters", "{'reported_reading_size': '$.inputs.reported_reading_size'}")
cb(cc, "confirm_reported_reading_fits", "INPUT", "rules", "[{'field': 'reported_reading_size', 'op': 'lte', 'value': '$.inputs.reading_capacity'}]")
cb(cc, "confirm_reported_reading_fits", "OUTPUT", "reading_fits", "capability_result.valid")

OPEN_FIELDS = ["user_prompt_id", "requester_id", "customer_id", "identity_key", "kind", "question", "supporting_material",
               "time_in_service_id", "reading", "fingerprint", "reading_capacity", "maximum_response_length"]
cc = "CC_OPEN_HOSTED_RECORD_V0"
step(cc, 1, "form_rules_in_force", q("CT_PURE_FORM_RESPONSE_RULES_V0"), "CT", "FORM_RESPONSE_RULES", "—",
     "response_rules, account_numbers, seed", "rules_in_force, positions", "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS",
     "in: response_rules=response_rules, account_numbers=account_numbers, seed=seed; out: rules_in_force=rules_in_force, positions=positions")
step(cc, 2, "assemble_opening_record", ASSEMBLE, "CT", "ASSEMBLE_RECORD", "—", ", ".join(OPEN_FIELDS + ["response_rules"]),
     "opening_record", "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: fields=opening_fields; out: record=opening_record")
step(cc, 3, "append_opening_record", APP, "CS", "APPEND", "USER_PROMPT_RECORDS", "record, stream_id, actor_id",
     "record_id, sequence_number", "SUCCESS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
cb(cc, "form_rules_in_force", "INPUT", "response_rules", "inputs.response_rules")
cb(cc, "form_rules_in_force", "INPUT", "account_numbers", "inputs.account_numbers")
cb(cc, "form_rules_in_force", "INPUT", "seed", "inputs.seed")
cb(cc, "form_rules_in_force", "OUTPUT", "rules_in_force", "capability_result.rules_in_force")
cb(cc, "form_rules_in_force", "OUTPUT", "positions", "capability_result.positions")
fields = ", ".join(f"'{f}': '$.inputs.{f}'" for f in OPEN_FIELDS)
cb(cc, "assemble_opening_record", "INPUT", "fields",
   "{" + fields + ", 'rules_in_force': '$.results.form_rules_in_force.rules_in_force', "
   "'ground_numbers': '$.inputs.response_rules.ground_numbers', "
   "'longest_response': '$.inputs.response_rules.longest_response', 'outcome': 'WRITING'}")
cb(cc, "assemble_opening_record", "OUTPUT", "opening_record", "capability_result.record")
cb(cc, "append_opening_record", "INPUT", "record", "results.assemble_opening_record.opening_record")
cb(cc, "append_opening_record", "INPUT", "stream_id", "inputs.user_prompt_id")
cb(cc, "append_opening_record", "INPUT", "actor_id", "inputs.requester_id")
cb(cc, "append_opening_record", "OUTPUT", "record_id", "capability_result.record_id")
cb(cc, "append_opening_record", "OUTPUT", "sequence_number", "capability_result.sequence_number")

cc = "CC_READ_HOSTED_STATE_V0"
step(cc, 1, "read_trail", APP, "CS", "GET_ALL", "USER_PROMPT_RECORDS", "stream_id", "entries",
     "SUCCESS -> continue; BACKEND_ERROR -> exit", "SUCCESS")
step(cc, 2, "reduce_trail", q("CT_PURE_READ_HOSTED_STATE_V0"), "CT", "READ_HOSTED_STATE", "—", "entries", "state",
     "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: entries=entries; out: state=state")
cb(cc, "read_trail", "INPUT", "stream_id", "inputs.user_prompt_id")
cb(cc, "read_trail", "OUTPUT", "entries", "capability_result.entries")
cb(cc, "read_trail", "OUTPUT", "result_status", "result_status")
cb(cc, "reduce_trail", "INPUT", "entries", "results.read_trail.entries")
cb(cc, "reduce_trail", "OUTPUT", "state", "capability_result.state")

cc = "CC_CONFIRM_OFFER_FOR_MODEL_V0"
step(cc, 1, "confirm_same_model", MEMBER, "CT", "VALIDATE_SET_MEMBERSHIP", "—", "offered_fingerprint, admitted_fingerprint",
     "offer_for_model", "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS", "in: value=offered_fingerprint, allowed_set=admitted_fingerprint; out: is_member=offer_for_model")
cb(cc, "confirm_same_model", "INPUT", "value", "inputs.offered_fingerprint")
cb(cc, "confirm_same_model", "INPUT", "allowed_set", "['$.inputs.admitted_fingerprint']")
cb(cc, "confirm_same_model", "OUTPUT", "offer_for_model", "capability_result.is_member")

cc = "CC_CHOOSE_PERMITTED_TOKEN_V0"
step(cc, 1, "choose_token", q("CT_PURE_CHOOSE_PERMITTED_TOKEN_V0"), "CT", "CHOOSE_PERMITTED_TOKEN", "—", "state, candidates",
     "step, text, finished, stopped_by, within_length", "SUCCESS -> exit; VIOLATION -> exit", "SUCCESS",
     "in: state=state, candidates=candidates; out: step=step, text=text, finished=finished, stopped_by=stopped_by, within_length=within_length")
cb(cc, "choose_token", "INPUT", "state", "inputs.state")
cb(cc, "choose_token", "INPUT", "candidates", "inputs.candidates")
for o in ("step", "text", "finished", "stopped_by", "within_length"):
    cb(cc, "choose_token", "OUTPUT", o, f"capability_result.{o}")

STEP_FIELDS = ["position", "candidates", "chosen", "stopped", "stopped_by", "finished", "within_length"]
cc = "CC_RECORD_HOSTED_STEP_V0"
step(cc, 1, "assemble_step_record", ASSEMBLE, "CT", "ASSEMBLE_RECORD", "—", "user_prompt_id, host_id, fingerprint, reported_reading_size, step",
     "step_record", "SUCCESS -> continue; VIOLATION -> exit", "SUCCESS", "in: fields=step_fields; out: record=step_record")
step(cc, 2, "append_step_record", APP, "CS", "APPEND", "USER_PROMPT_RECORDS", "record, stream_id, actor_id",
     "record_id, sequence_number", "SUCCESS -> exit; VIOLATION -> exit; BACKEND_ERROR -> exit", "SUCCESS")
cb(cc, "assemble_step_record", "INPUT", "fields",
   "{'user_prompt_id': '$.inputs.user_prompt_id', 'outcome': 'STEP', 'host_id': '$.inputs.host_id', "
   "'fingerprint': '$.inputs.fingerprint', 'reported_reading_size': '$.inputs.reported_reading_size', "
   + ", ".join(f"'{f}': '$.inputs.step.{f}'" for f in STEP_FIELDS) + "}")
cb(cc, "assemble_step_record", "OUTPUT", "step_record", "capability_result.record")
cb(cc, "append_step_record", "INPUT", "record", "results.assemble_step_record.step_record")
cb(cc, "append_step_record", "INPUT", "stream_id", "inputs.user_prompt_id")
cb(cc, "append_step_record", "INPUT", "actor_id", "inputs.host_id")
cb(cc, "append_step_record", "OUTPUT", "record_id", "capability_result.record_id")
cb(cc, "append_step_record", "OUTPUT", "sequence_number", "capability_result.sequence_number")


# ---------------------------------------------------------------- workflow node bindings
def wb(wf, st, field, bound):
    BIND.append((q(wf), st, "INPUT", field, bound, f"S7 execution_topology {st.split('::')[-1]}"))


wf = "WF_BEGIN_HOSTED_RESPONSE_V0"
ADM = "results.CC_ADMIT_USER_PROMPT_V0.model_record"
wb(wf, CLAIM, "user_prompt_id", "payload.user_prompt_id")
wb(wf, REQ, "customer_id", "payload.customer_id")
wb(wf, REQ, "permitted_customers", "payload.permitted_customers")
wb(wf, ADMIT, "identity_key", "payload.identity_key")
wb(wf, CEIL, "time_in_service_id", f"{ADM}.time_in_service_id")
wb(wf, CEIL, "kind", "payload.kind")
wb(wf, FITS, "system_prompt", "results.CC_CONFIRM_WITHIN_CEILING_V0.time_in_service.system_prompt")
wb(wf, FITS, "question", "payload.question")
wb(wf, FITS, "supporting_material", "payload.supporting_material")
wb(wf, FITS, "reading_capacity", f"{ADM}.description.reading_capacity")
for fl in ("user_prompt_id", "requester_id", "customer_id", "identity_key", "kind", "question", "supporting_material",
           "account_numbers", "seed"):
    wb(wf, OPEN, fl, f"payload.{fl}")
wb(wf, OPEN, "time_in_service_id", f"{ADM}.time_in_service_id")
wb(wf, OPEN, "reading", "results.CC_CONFIRM_READING_FITS_V0.reading")
wb(wf, OPEN, "response_rules", "results.CC_CONFIRM_WITHIN_CEILING_V0.time_in_service.response_rules")
wb(wf, OPEN, "fingerprint", f"{ADM}.fingerprint")
wb(wf, OPEN, "reading_capacity", f"{ADM}.description.reading_capacity")
wb(wf, OPEN, "maximum_response_length", f"{ADM}.description.maximum_response_length")
ALWAYS = [(f, f"payload.{f}") for f in ("user_prompt_id", "requester_id", "customer_id", "identity_key", "kind", "question",
                                         "supporting_material")]
TIS = [("time_in_service_id", f"{ADM}.time_in_service_id")]
BEGIN_PLACES = {
    "NOT_PERMITTED": ("requester_not_permitted_for_customer", []),
    "NOT_REGISTERED": ("model_not_registered", []),
    "NOT_IN_SERVICE": ("model_not_in_service", []),
    "ABOVE_CEILING": ("kind_above_sensitivity_ceiling", TIS),
    "TOO_LONG_TO_READ": ("reading_longer_than_model_can_read", TIS),
}
for r, (reason, known) in BEGIN_PLACES.items():
    for fl, src in ALWAYS + known:
        wb(wf, f"RECORD_REFUSED_{r}", fl, src)
    wb(wf, f"RECORD_REFUSED_{r}", "outcome", "REFUSED")
    wb(wf, f"RECORD_REFUSED_{r}", "reason", reason)

wf = "WF_OFFER_NEXT_TOKENS_V0"
ST = "results.CC_READ_HOSTED_STATE_V0.state"
wb(wf, READST, "user_prompt_id", "payload.user_prompt_id")
wb(wf, SAME, "offered_fingerprint", "payload.fingerprint")
wb(wf, SAME, "admitted_fingerprint", f"{ST}.opening.fingerprint")
wb(wf, HFITS, "reported_reading_size", "payload.reported_reading_size")
wb(wf, HFITS, "reading_capacity", f"{ST}.opening.reading_capacity")
wb(wf, CHOOSE, "state", ST)
wb(wf, CHOOSE, "candidates", "payload.candidates")
wb(wf, "CONFIRM_NO_RULE_STOPPED", "release_facts", "{'stopped_by': '$.results.CC_CHOOSE_PERMITTED_TOKEN_V0.stopped_by'}")
wb(wf, "CONFIRM_NO_RULE_STOPPED", "release_rules", "[{'field': 'stopped_by', 'op': 'eq', 'value': 'none'}]")
wb(wf, "CONFIRM_WITHIN_LENGTH", "release_facts", "{'within_length': '$.results.CC_CHOOSE_PERMITTED_TOKEN_V0.within_length'}")
wb(wf, "CONFIRM_WITHIN_LENGTH", "release_rules", "[{'field': 'within_length', 'op': 'eq', 'value': True}]")
for place in ("RECORD_STEP", "RECORD_STOPPED_STEP", "RECORD_UNFINISHED_STEP"):
    wb(wf, place, "user_prompt_id", "payload.user_prompt_id")
    wb(wf, place, "host_id", "payload.host_id")
    wb(wf, place, "fingerprint", "payload.fingerprint")
    wb(wf, place, "reported_reading_size", "payload.reported_reading_size")
    wb(wf, place, "step", "results.CC_CHOOSE_PERMITTED_TOKEN_V0.step")
OPENED = [("user_prompt_id", "payload.user_prompt_id")] + [
    (f, f"{ST}.opening.{f}") for f in ("requester_id", "customer_id", "identity_key", "kind", "question",
                                       "supporting_material", "time_in_service_id")]
READ_RULED = [("reading", f"{ST}.opening.reading"), ("rules_in_force", f"{ST}.opening.rules_in_force")]
OFFER_PLACES = {
    "OTHER_MODEL": ("offer_for_another_model", READ_RULED),
    "TOO_LONG_TO_READ": ("reading_longer_than_model_can_read", READ_RULED),
    "BY_RULE": ("results.CC_CHOOSE_PERMITTED_TOKEN_V0.stopped_by", READ_RULED),
    "UNFINISHED": ("longest_response_reached", READ_RULED),
}
for r, (reason, known) in OFFER_PLACES.items():
    for fl, src in OPENED + known:
        wb(wf, f"RECORD_REFUSED_{r}", fl, src)
    wb(wf, f"RECORD_REFUSED_{r}", "outcome", "REFUSED")
    wb(wf, f"RECORD_REFUSED_{r}", "reason", reason)

wf = "WF_RELEASE_HOSTED_RESPONSE_V0"
wb(wf, READST, "user_prompt_id", "payload.user_prompt_id")
wb(wf, "CONFIRM_FINISHED", "release_facts", "{'finished': '$.results.CC_READ_HOSTED_STATE_V0.state.finished'}")
wb(wf, "CONFIRM_FINISHED", "release_rules", "[{'field': 'finished', 'op': 'eq', 'value': True}]")
for fl, src in OPENED + READ_RULED:
    wb(wf, "RECORD_RESPONDED", fl, src)
wb(wf, "RECORD_RESPONDED", "outcome", "RESPONDED")
wb(wf, "RECORD_RESPONDED", "response", f"{ST}.text")

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
    "user_prompt_id": ("string", "The request's identity, named by the requester and claimed once"),
    "requester_id": ("string", "The requester who submits the request"),
    "permitted_customers": ("array", "The customers the requester may act for, as the business's existing arrangements state"),
    "customer_id": ("string", "The customer the request is for"),
    "account_numbers": ("array", "The customer's own account numbers, from the business's existing records"),
    "identity_key": ("string", "The key of the hosted model the request is for"),
    "kind": ("string", "The most sensitive kind of information the question and its material contain"),
    "question": ("string", "What the requester asks on the customer's behalf"),
    "supporting_material": ("string", "Material carried with the question for the model to read"),
    "seed": ("integer", "The seed each adventurous choice is drawn from"),
    "host_id": ("string", "The host offering, as it names itself; recorded, not authenticated"),
    "fingerprint": ("string", "The fingerprint of the model the offer is claimed to come from"),
    "reported_reading_size": ("integer", "How many tokens the host reports the model reads for this request"),
    "candidates": ("array", "The tokens the model could write next, each with its likelihood"),
    "time_in_service_id": ("string", "The model's open time in service"),
    "reading": ("object", "Exactly what the model reads"),
    "response_rules": ("object", "The time in service's forbidden words and patterns, account-number shape, freedom and longest response"),
    "reading_capacity": ("integer", "How many tokens the model can read in one request"),
    "maximum_response_length": ("integer", "The most tokens a response of the model may have"),
    "state": ("object", "The hosted request's response as built, its position, whether it is complete, and its permitted length"),
    "offered_fingerprint": ("string", "The fingerprint an offer names"),
    "admitted_fingerprint": ("string", "The fingerprint of the model the request was admitted for"),
    "step": ("object", "One offer and the choice made from it"),
}
INTENTS = {
    "IN_BEGIN_HOSTED_RESPONSE_V0": ["user_prompt_id", "requester_id", "permitted_customers", "customer_id", "account_numbers",
                                    "identity_key", "kind", "question", "supporting_material", "seed"],
    "IN_OFFER_NEXT_TOKENS_V0": ["user_prompt_id", "host_id", "fingerprint", "reported_reading_size", "candidates"],
    "IN_RELEASE_HOSTED_RESPONSE_V0": ["user_prompt_id", "host_id"],
}
for art, fields in INTENTS.items():
    for fl in fields:
        f(art, "INPUT", fl, *M[fl])

CCF = {
    "CC_CONFIRM_HOSTED_READING_FITS_V0": (["reported_reading_size", "reading_capacity"],
                                          [("reading_fits", "boolean", "Whether the reported size is within the capacity")]),
    "CC_OPEN_HOSTED_RECORD_V0": (["user_prompt_id", "requester_id", "customer_id", "identity_key", "kind", "question", "supporting_material",
                                  "time_in_service_id", "reading", "response_rules", "account_numbers", "seed", "fingerprint",
                                  "reading_capacity", "maximum_response_length"],
                                 [("rules_in_force", "object", "The response rules in force for this request, with its seed"),
                                  ("positions", "array", "One position per token up to the rules' longest response"),
                                  ("opening_record", "object", "The opening entry of the request's trail, with what the model reads"),
                                  ("record_id", "string", "The identity of the opening entry"),
                                  ("sequence_number", "integer", "The opening entry's position in the user prompt records")]),
    "CC_READ_HOSTED_STATE_V0": (["user_prompt_id"], [("entries", "array", "The request's trail as recorded"),
                                                     ("state", "object", M["state"][1])]),
    "CC_CONFIRM_OFFER_FOR_MODEL_V0": (["offered_fingerprint", "admitted_fingerprint"],
                                      [("offer_for_model", "boolean", "Whether the offer names the admitted model's fingerprint")]),
    "CC_CHOOSE_PERMITTED_TOKEN_V0": (["state", "candidates"],
                                     [("step", "object", M["step"][1]), ("text", "string", "The response with the chosen token"),
                                      ("finished", "boolean", "Whether the chosen token ends the response"),
                                      ("stopped_by", "string", "The rule that left no permitted token, or none"),
                                      ("within_length", "boolean", "Whether the response is still within its permitted length")]),
    "CC_RECORD_HOSTED_STEP_V0": (["user_prompt_id", "host_id", "fingerprint", "reported_reading_size", "step"],
                                 [("step_record", "object", "The step entry appended to the request's trail"),
                                  ("record_id", "string", "The identity of the step entry"),
                                  ("sequence_number", "integer", "The step entry's position in the user prompt records")]),
}
for cc, (ins, outs) in CCF.items():
    for fl in ins:
        f(cc, "INPUT", fl, *M[fl])
    for name, typ, meaning in outs:
        f(cc, "OUTPUT", name, typ, meaning)

CTF = {
    "CT_PURE_READ_HOSTED_STATE_V0": ([("entries", "array", "The request's trail as recorded")], [("state", "object", M["state"][1])]),
    "CT_PURE_CHOOSE_PERMITTED_TOKEN_V0": ([("state", "object", M["state"][1]), ("candidates", "array", M["candidates"][1])],
                                          [("step", "object", M["step"][1]), ("text", "string", "The response with the chosen token"),
                                           ("finished", "boolean", "Whether the chosen token ends the response"),
                                           ("stopped_by", "string", "The rule that left no permitted token, or none"),
                                           ("within_length", "boolean", "Whether the response is still within its permitted length")]),
}
for ct, (ins, outs) in CTF.items():
    for name, typ, meaning in ins:
        f(ct, "INPUT", name, typ, meaning)
    for name, typ, meaning in outs:
        f(ct, "OUTPUT", name, typ, meaning)
f("AC_MODEL_HOST_V0", "ATTRIBUTE", "host_id", "string", "The host's name for itself; recorded against every offer, not authenticated")

w("""
---

## 8. Interface Fields

""")
w(table("interface_fields", ["Artifact", "Direction (INPUT, OUTPUT, ATTRIBUTE)", "Field", "Type", "Required (YES, NO)", "Default", "Meaning"], F))

MOD = "causal_language_model.implementation.capability_transforms.atoms"
IMPL = [("CT_PURE_READ_HOSTED_STATE_V0", "READ_HOSTED_STATE", "raises"),
        ("CT_PURE_CHOOSE_PERMITTED_TOKEN_V0", "CHOOSE_PERMITTED_TOKEN", "raises")]
w("""
---

## 9. Implementation Bindings

The state is read from the trail and nowhere else: the opening entry, then the steps in the order they
were appended. A trail with no opening entry, or with a closing one, is refused. The chosen tokens are
joined as they are into the response so far; the end marker `<end>` ends it.

The choice stops a candidate when a forbidden rule's pattern matches the response so far joined to the
candidate, at a match that reaches into the candidate, unless the matched characters with spaces and
dashes removed are among the rule's exceptions. Text is judged in its compatibility form, so a
lookalike digit is the digit it looks like. A number is judged on its digits, spaces, commas, dots and
dashes between them being separators. A number the model read is not begun unless it could be a
permitted one: a candidate is stopped when it writes digits that begin a number a rule forbids in what
the model read, and begin no other number the model read. Where the opening sets grounding, a number
may not be begun unless a number the model read begins with its digits, nor ended unless it is one, and
a candidate that would do either is stopped by `numbers_from_the_reading`. It chooses among the
permitted candidates, most likely first and ties in offered order: of the first freedom-plus-one, the
one at position (seed plus the token's position) modulo their count. A response may have at most its
permitted length in tokens, the end marker not counted; a token that would take it past that leaves it
outside its length. An offer for a complete response is refused.

""")
w(table("implementation_bindings", ["CT Code", "Module", "Callable", "Operation", "Kind (atom, molecule)", "Purity (ct_pure, ct_impure)",
                                    "Refusal (raises, returns, never)", "Source Finding"],
        [(q(c), f"{MOD}.{c.lower()}", "execute", op, "atom", "ct_pure", r, f"S7 new_artifacts {c}") for c, op, r in IMPL]))

w("""
---

## 10. Vocabulary Extensions

""")
w(table("vocabulary_extensions", ["Vocabulary Code", "Extends", "Group", "Casing", "Value", "Meaning", "Source Finding"], []))
w("""
---

## 11. Runtime Policies

""")
w(table("runtime_policies", ["RB Code", "Capability", "Key", "Value", "Source Finding"], []))

PROPS = [(q("AC_MODEL_HOST_V0"), "type", "ENDUSER", "S5 provisional_codes AC_MODEL_HOST_V0"),
         (q("WF_BEGIN_HOSTED_RESPONSE_V0"), "emit.EXIT_REFUSED", q("EV_USER_PROMPT_REFUSED_V0"), "S1 business_events #2"),
         (q("WF_OFFER_NEXT_TOKENS_V0"), "emit.EXIT_REFUSED", q("EV_USER_PROMPT_REFUSED_V0"), "S1 business_events #2"),
         (q("WF_RELEASE_HOSTED_RESPONSE_V0"), "emit.EXIT_RESPONDED", q("EV_USER_PROMPT_RESPONDED_V0"), "S1 business_events #1"),
         (q("EV_USER_PROMPT_REFUSED_V0"), "moment", "refusal", "S1 business_events #2")]
w("""
---

## 12. Artifact Properties

""")
w(table("artifact_properties", ["Artifact", "Property", "Value", "Source Finding"], PROPS))
w("""
---

## 13. STRUCTURE Stores

The trail is kept in the user prompt records the subdomain already declares; no store is added.

""")
w(table("structure_stores", ["Store Name", "Storage Type (CS_APPENDONLY_JSONL_V0, CS_MUTABLE_JSON_V0, CS_REGISTRY_V0)", "Proposed Path", "Used By", "Source Finding"], []))
w("""
---

## 14. Transport Bindings

""")
w(table("transport_bindings", ["Artifact", "Direction (INGRESS, EGRESS)", "Operation", "Handler Kind (WF_INVOCATION, SNAPSHOT_READ)", "Handler Target", "Field", "Bound To", "Source Finding"], []))

counts = {}
for _, fam, *_ in NEW:
    counts[fam] = counts.get(fam, 0) + 1
w("""
## 15. Artifact Summary

""")
w(table("artifact_summary", ["Action (REPLACE, EXTEND, NEW)", "Subdomain", "Count", "Artifacts"],
        [("NEW", SUB, len(NEW), ", ".join(f"{counts[k]} {k}" for k in ["AC", "IN", "WF", "CC", "CT"]))], flags=""))
w("""
---

## 16. Generation Provenance

""")
w(table("generation_provenance", ["Artifact", "Generator", "Generator Sources", "Source Finding"], []))
w("""
---

## 17. Declared Reach

Every act reads only what model_response owns.

""")
w(table("declared_reach", ["Act", "Consults", "Source Finding"], []))

OW, RW = q("WF_OFFER_NEXT_TOKENS_V0"), q("WF_RELEASE_HOSTED_RESPONSE_V0")
DIS = [
    ("Offer candidates", "The reported reading size exceeds the model's reading capacity.", OW, "RECORD_REFUSED_TOO_LONG_TO_READ", "SUCCESS", "S0 operation_refusals #1"),
    ("Offer candidates", "The offer names a fingerprint other than the model's the request was admitted for.", OW, "RECORD_REFUSED_OTHER_MODEL", "SUCCESS", "S0 operation_refusals #2"),
    ("Offer candidates", "The request is not being written.", OW, READST, "VIOLATION", "S0 operation_refusals #3"),
    ("Offer candidates", "Every candidate is forbidden.", OW, "RECORD_REFUSED_BY_RULE", "SUCCESS", "S0 operation_refusals #4"),
    ("Offer candidates", "The response reaches its permitted length before it is complete.", OW, "RECORD_REFUSED_UNFINISHED", "SUCCESS", "S0 operation_refusals #5"),
    ("Release a response", "The response is not complete.", RW, "CONFIRM_FINISHED", "VIOLATION", "S0 operation_refusals #6"),
]
w("""
---

## 18. Refusal Discharge

A refusal that closes the request is discharged at the place that records it, whose success ends the
act at `EXIT_REFUSED`. An offer for a request not being written, and a release of an incomplete
response, change nothing and end at `EXIT_REJECTED`.

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
w("""
---

## 21. Molecule Steps

""")
w(table("molecule_steps", ["CT Code", "Step", "Kind (atom, molecule, loop)", "Target", "Over", "Iterator", "Emits", "Source Finding"], []))
w("""
---

## 22. Molecule Step Bindings

""")
w(table("molecule_step_bindings", ["CT Code", "Step", "Role (INPUT, CARRY, UPDATE)", "Field", "Bound To", "Source Finding"], []))

# ---------------------------------------------------------------- vectors
TC, TV = [], []
ACCT = "'[0-9](?:[ -]?[0-9]){7}'"
FORBID = f"[{{rule: no_guarantees, pattern: '\\bguaranteed\\b'}}, {{rule: another_customers_account_number, pattern: {ACCT}, except: ['12345678']}}]"
RIF = f"{{forbidden: {FORBID}, freedom: 0, seed: 7}}"
READING = "{system_prompt: 'Answer only from the supporting material.', question: 'What is my balance?', supporting_material: 'Account 12345678 balance 40. Spouse account 87654321.'}"
def opening(grounded="false"):
    return (f"{{outcome: WRITING, fingerprint: fp-host, reading: {READING}, rules_in_force: {RIF}, "
            f"ground_numbers: {grounded}, maximum_response_length: 3, longest_response: 5}}")


OPENING = opening()


def case(ct, name, outcome, values):
    TC.append((q(ct), name, outcome, "human decision"))
    for role, field, value in values:
        TV.append((q(ct), name, role, field, value, "human decision"))


def state(position, text, finished="false", limit=3, grounded="false"):
    return f"{{opening: {opening(grounded)}, position: {position}, text: '{text}', finished: {finished}, limit: {limit}}}"


READ = "CT_PURE_READ_HOSTED_STATE_V0"
case(READ, "reduces_the_trail_to_the_response_as_built", "SUCCESS", [
    ("INPUT", "entries", f"[{{sequence_number: 1, record: {OPENING}}}, {{sequence_number: 2, record: {{outcome: STEP, chosen: 'Your'}}}}, "
                         "{sequence_number: 3, record: {outcome: STEP, chosen: ' balance'}}]"),
    ("EXPECTED", "state", state(2, "Your balance")),
])
case(READ, "refuses_a_request_never_admitted", "VIOLATION", [
    ("INPUT", "entries", "[{sequence_number: 1, record: {outcome: REFUSED, reason: model_not_registered}}]"),
])
case(READ, "refuses_a_closed_request", "VIOLATION", [
    ("INPUT", "entries", f"[{{sequence_number: 1, record: {OPENING}}}, {{sequence_number: 2, record: {{outcome: RESPONDED}}}}]"),
])
CH = "CT_PURE_CHOOSE_PERMITTED_TOKEN_V0"
case(CH, "stops_an_account_number_split_across_tokens", "SUCCESS", [
    ("INPUT", "state", state(1, "Account 8765")),
    ("INPUT", "candidates", "[{token: '4321', likelihood: 0.7}, {token: ' is', likelihood: 0.2}]"),
    ("EXPECTED", "text", "Account 8765 is"), ("EXPECTED", "finished", "false"), ("EXPECTED", "stopped_by", "none"),
    ("EXPECTED", "within_length", "true"),
])
case(CH, "writes_the_customers_own_account_across_tokens", "SUCCESS", [
    ("INPUT", "state", state(1, "Account 1234")),
    ("INPUT", "candidates", "[{token: '5678', likelihood: 0.8}]"),
    ("EXPECTED", "text", "Account 12345678"), ("EXPECTED", "stopped_by", "none"),
])
case(CH, "names_the_rule_when_no_permitted_token_remains", "SUCCESS", [
    ("INPUT", "state", state(0, "")),
    ("INPUT", "candidates", "[{token: '87654321', likelihood: 0.9}]"),
    ("EXPECTED", "text", "\"\""), ("EXPECTED", "stopped_by", "another_customers_account_number"), ("EXPECTED", "finished", "false"),
])
case(CH, "passes_the_permitted_length_unfinished", "SUCCESS", [
    ("INPUT", "state", state(3, "Your balance is")),
    ("INPUT", "candidates", "[{token: ' today', likelihood: 0.9}]"),
    ("EXPECTED", "text", "Your balance is today"), ("EXPECTED", "within_length", "false"), ("EXPECTED", "finished", "false"),
])
case(CH, "finishes_on_the_end_of_the_response", "SUCCESS", [
    ("INPUT", "state", state(2, "Your balance")),
    ("INPUT", "candidates", "[{token: <end>, likelihood: 0.9}]"),
    ("EXPECTED", "text", "Your balance"), ("EXPECTED", "finished", "true"), ("EXPECTED", "within_length", "true"),
])
case(CH, "judges_a_lookalike_digit_as_the_digit", "SUCCESS", [
    ("INPUT", "state", state(2, "Spouse account 8765432")),
    ("INPUT", "candidates", "[{token: '₁', likelihood: 0.8}, {token: '.', likelihood: 0.1}]"),
    ("EXPECTED", "text", "Spouse account 8765432."), ("EXPECTED", "stopped_by", "none"),
])
case(CH, "does_not_begin_a_forbidden_number_the_model_read", "SUCCESS", [
    ("INPUT", "state", state(2, "Spouse account ")),
    ("INPUT", "candidates", "[{token: '8', likelihood: 0.8}, {token: withheld, likelihood: 0.1}]"),
    ("EXPECTED", "text", "Spouse account withheld"), ("EXPECTED", "stopped_by", "none"),
])
case(CH, "begins_a_number_the_model_read_that_is_permitted", "SUCCESS", [
    ("INPUT", "state", state(2, "Balance ")),
    ("INPUT", "candidates", "[{token: '4', likelihood: 0.8}]"),
    ("EXPECTED", "text", "Balance 4"), ("EXPECTED", "stopped_by", "none"),
])
case(CH, "grounded_writes_a_number_it_read", "SUCCESS", [
    ("INPUT", "state", state(2, "Balance 4", grounded="true")),
    ("INPUT", "candidates", "[{token: '9', likelihood: 0.8}, {token: '0', likelihood: 0.1}]"),
    ("EXPECTED", "text", "Balance 40"), ("EXPECTED", "stopped_by", "none"),
])
case(CH, "grounded_does_not_change_a_value_it_read", "SUCCESS", [
    ("INPUT", "state", state(2, "Balance 4", grounded="true")),
    ("INPUT", "candidates", "[{token: ' dollars', likelihood: 0.8}, {token: <end>, likelihood: 0.1}]"),
    ("EXPECTED", "text", "Balance 4"), ("EXPECTED", "stopped_by", "numbers_from_the_reading"),
])
case(CH, "ungrounded_writes_a_number_it_did_not_read", "SUCCESS", [
    ("INPUT", "state", state(2, "Balance ")),
    ("INPUT", "candidates", "[{token: '9', likelihood: 0.8}]"),
    ("EXPECTED", "text", "Balance 9"), ("EXPECTED", "stopped_by", "none"),
])
case(CH, "refuses_an_offer_for_a_complete_response", "VIOLATION", [
    ("INPUT", "state", state(2, "Your balance", finished="true")),
    ("INPUT", "candidates", "[{token: ' more', likelihood: 0.9}]"),
])

import sys, yaml
sys.path.insert(0, "/Users/bp/protocol-governed-computing/business_domains")
from causal_language_model.implementation.capability_transforms.atoms import ct_pure_choose_permitted_token_v0 as _ch


def _flow(v):
    return yaml.safe_dump(v, default_flow_style=True, width=10**6, sort_keys=False).removesuffix("...\n").strip()


for _ct, _name, _outcome, _ in list(TC):
    if _ct != q(CH) or _outcome != "SUCCESS":
        continue
    _given = {r[3]: yaml.safe_load(r[4]) for r in TV if r[0] == _ct and r[1] == _name and r[2] == "INPUT"}
    _stated = {r[3]: r for r in TV if r[0] == _ct and r[1] == _name and r[2] == "EXPECTED"}
    _out = _ch.execute(inputs=_given)
    for _field, _value in _out.items():
        if _field in _stated:
            assert yaml.safe_load(_stated[_field][4]) == _value or (_stated[_field][4] == '""' and _value == ""), (_name, _field, _value)
        else:
            TV.append((_ct, _name, "EXPECTED", _field, _flow(_value), "human decision"))

_order = [(c[0], c[1]) for c in TC]
TV.sort(key=lambda r: _order.index((r[0], r[1])))

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

## 25. Withdrawn Facts

""")
w(table("withdrawn_facts", ["Artifact", "Fact", "Reason", "Source Finding"], []))
w("""
---

## gov_projection — Governed Handoff to Stage 8

| Direction | Fields |
|-----------|--------|
| **Consumes** ← Stage 6 | ownership · storage_governance · cross_subdomain_deps · pps_artifacts_requiring_action · boundary_rules · governance_outcome |
| **Emits** → Stage 8 | design_resolution · existing_inventory · new_artifacts · rb_declarations · execution_topology · cc_composition · step_bindings · interface_fields · implementation_bindings · vocabulary_extensions · runtime_policies · artifact_properties · structure_stores · artifact_summary · generation_provenance |
""")

OUT.write_text("".join(x if x.endswith("\n") else x + "\n" for x in out))
print(OUT.name, len(NEW), "new;", len(TOPO), "topology rows;", len(BIND), "bindings;", len(F), "fields;", len(TC), "cases")
