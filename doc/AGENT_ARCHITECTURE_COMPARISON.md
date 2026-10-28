# PGC for AI Agents: Comparison with Current Agent Architectures

## 1. The question

Should PGC be used to build AI agents? In such an agent, the sealed snapshot states the behavior,
and the model, the prompts and the tool code only realize it.

This document compares that approach with how agents are built today. It then states the case
for pursuing it, where the case is weak, and how to test it.

---

## 2. How agents are built today

### 2.1 Orchestration frameworks
- LangGraph, the OpenAI Agents SDK, the Claude Agent SDK, CrewAI, AG2 and Microsoft Agent
  Framework all fall here.
- Control flow lives in code, in a graph that code builds, or in the model's own choices.
- Governance is the least-documented area of these frameworks.
  - One comparison rates Microsoft Agent Framework and CrewAI Enterprise as the most mature,
    with LangGraph plus LangSmith close behind.
  - Teams using the other frameworks build the governance layer themselves [1].

### 2.2 Enforcement at the tool boundary
The field is moving away from prompt instructions and model-judged guardrails. It is moving
toward deterministic checks outside the model.

- **Cloud gateways.**
  - AWS Bedrock AgentCore Policy evaluates Cedar rules at a gateway before each tool call,
    with default deny [2].
  - Alibaba's Agent Identity does the same for outbound MCP calls [2].
- **Out-of-Band Policy Enforcement (OBPE)** [3].
  - A trusted proxy narrows each query and filters each response.
  - Agent policy can only narrow the data owner's grant.
  - Results: across 3,621 trials, trace failures fell from 57.6% to 0.2%. Task fulfillment fell
    from 79.1% to 60.9%.
  - Not covered: write controls, durable approval, and temporal or aggregate policies.
- **CaMeL** [4].
  - It takes the control flow from the trusted user query, so untrusted data cannot change it.
  - Capability tags on values restrict where data may flow.
  - It solves 77% of AgentDojo tasks with provable security, against 84% for an undefended agent.
  - Its guarantees do not compose across several agents [5].
- **Practice guidance.** Practitioners now separate policy from reasoning and enforce critical
  actions with fixed rules. A second model watching the first is treated as a weak primary
  control [6].

### 2.3 Whole-execution policy
- The Compositional Policy Violations paper shows that every step can pass its own check while
  the full execution breaks the policy [7].
- It names four types: authority creep, threshold laundering, cumulative-sum violation and
  context collapse.
- Its proposed fix checks the complete trace and recomputes guarded values from raw provenance.

### 2.4 Configuration as a governed object
- Agentic Configuration Management (ACM) [8]:
  - versions agents, prompts, tools, models, policies and workflows as typed items with immutable
    baselines;
  - separates configuration from runtime;
  - has adapters for LangGraph, CrewAI and the OpenAI Agents SDK.
- Its abstract does not describe build-time verification of the composition.

### 2.5 Durable execution and replay
- Temporal splits an agent into deterministic workflow code and non-deterministic activities.
  Model calls are activities.
- After a crash, it replays the recorded model results rather than calling the model again [9].
- Integrations exist for the OpenAI Agents SDK and Google ADK [9].

### 2.6 Risk catalog and regulation
- **OWASP Top 10 for Agentic Applications.** The first three entries are:
  - goal hijack;
  - tool misuse;
  - identity and privilege abuse [10].
- **EU AI Act, Article 12.**
  - High-risk systems must log events automatically over their lifetime. Logs must support risk
    identification, post-market monitoring and operational monitoring [11].
  - Under Article 25, an integrator that deploys a general-purpose model in a high-risk use takes
    on provider obligations [11].
  - The Act does not require tamper-proof logs. Commentators argue that logs that can be altered
    have little value as evidence [11].
  - Annex III obligations were due on 2 August 2026, and a pending proposal may defer them.
    Verify the current date before citing it.

---

## 3. Side-by-side

| Concern | Current practice | PGC agent |
|---|---|---|
| Where behavior is stated | Code, prompts, the model's choices | Sealed snapshot; code realizes it |
| When the boundary is checked | At each call (gateway, proxy, interpreter) | At build time over the whole composition, and at each call by the blind runtime |
| Whole-execution policy | A research problem [7]; trace checking after the fact | Workflow graph is sealed, so path-level rules are compile-time invariants |
| Change control | Code or prompt redeploy; ACM-style versioning emerging [8] | New snapshot hash; every behavior change is an artifact diff |
| Who authorized an act | Gateway decision log | Trace links each act to the sealed rule that admitted it (with decision accounting) |
| Replay | Temporal-style activity replay [9] | `ct_impure` outputs recorded and replayed |
| Model substitution | Often changes behavior silently | Same sealed behavior; the model is one realization |
| Caller identity and authority | Mature (IAM, Cedar, gateways) [2] | **Missing**: actor is attribution only (B5) |
| Open-ended planning | Native | Restricted to sealed options |
| Ecosystem and speed | Large; fast iteration | None; compile and seal per change |

---

## 4. The case for pursuing it

### 4.1 The field is converging on PGC's premise in pieces
Each current trend is one part of what PGC already does:
- deterministic enforcement outside the model (§2.2);
- control flow fixed before untrusted data arrives (CaMeL);
- configuration as a versioned, governed object (ACM);
- recorded model outputs for replay (Temporal);
- evidence that holds up to scrutiny (Article 12).

No surveyed system joins them. None seals the whole composition, checks it before deployment,
and runs it under a runtime that cannot add behavior. That union is the gap PGC can occupy.

### 4.2 PGC answers the problem the field has named but not solved
- Compositional violations arise because policy is checked one step at a time [7].
- In PGC the workflow graph is sealed. A rule over a whole path, such as "no route reaches the
  refund tool without passing the approval step", is a build-time invariant. No run-time monitor
  has to reconstruct it.
- PGC still needs run-time checks for rules over data, such as a cumulative sum across steps. But
  the compiler can require each such rule to be declared and bound to a sealed check. Today that
  is a matter of convention.

### 4.3 The control flow is fixed before the model runs
- CaMeL fixes control flow per query by having a privileged model write a plan [4].
- PGC fixes it per release, by a compiler. The model can choose only among sealed routes.
- This is a stronger and more auditable form of the same defense against goal hijack and tool
  misuse (OWASP ASI01–02). The guarantee does not depend on a planner model behaving well.

### 4.4 The evidence is what regulators will ask for
- Article 12 asks for automatic, lifetime logs that support risk identification and monitoring.
- A PGC trace records:
  - what happened;
  - the snapshot hash it ran under;
  - with decision accounting, which sealed rule or recorded observation each decision came from.
- An integrator under Article 25 needs to show that the deployed behavior is the approved
  behavior. A hash-attested snapshot is direct evidence of that.

### 4.5 Building an agent domain repairs PGC itself
An agent domain exercises the open gaps in `BEHAVIOR_OUTSIDE_SNAPSHOT.md` and
`DOMAIN_BEHAVIOR_OUTSIDE_SNAPSHOT.md`:
- **B5, authority.** An agent needs a verified principal, not attribution.
- **A1/A2, caller-supplied policy.** An agent must never supply its own limits.
- **B3, prompt rendering.** The text the model reads must be recorded or declared.
- **Decision accounting.** Model output is an `observed` source that the admissibility table must
  bar from acting as `policy`.

The work is useful even if the agent case fails.

---

## 5. Where the case is weak

- **Authority is the field's strength and PGC's gap.**
  - Gateways with Cedar and IAM already enforce who may call what [2].
  - PGC records an actor but enforces nothing.
  - Until B5 is closed, a PGC agent is less safe on identity than a stock AgentCore agent.
- **Usefulness costs.**
  - OBPE lost 18 points of task fulfillment [3], and CaMeL lost 7 [4].
  - Sealed routes are stricter than either, so PGC should expect a larger loss on open-ended
    tasks.
- **The model's reasoning stays ungoverned.** This is the C1 limit. PGC bounds what the model may
  do, not how it reasons. Data-to-text leaks, as in OBPE's reconstruction failures, are outside
  any routing guarantee.
- **Overlap.**
  - A buyer could approximate PGC with LangGraph, Cedar at a gateway, Temporal and signed logs.
  - PGC's argument must be the union and the build-time check (§4.1–4.2), not any single feature.
- **No ecosystem.** No adapters, no MCP integration, no users.

---

## 6. How to test it

Pursue it as an experiment with criteria for stopping, not as a pivot.

1. **Build one agent domain** on `causal_language_model`:
   - 3–4 tools, at least one of which writes or spends;
   - one approval step;
   - one cumulative limit.
2. **Close B5 first**, so that the comparison on authority is fair.
3. **Run a red-team suite** modelled on AgentDojo and the OBPE tasks against two agents:
   - the PGC agent;
   - an equivalent LangGraph agent with a Cedar gateway.
4. **Measure:**
   - policy violations in the trace;
   - compositional violations by the four types in [7];
   - task fulfillment;
   - time from a policy change to a verified deployment.
5. **Proceed only if** PGC:
   - catches compositional violations the gateway agent misses, at build time;
   - keeps task fulfillment within the range OBPE and CaMeL report.
   Otherwise publish the result and stop.

The compelling reason, stated plainly: agent safety is moving from "ask the model" to "enforce
outside the model". The next step is to verify the whole composition before it runs. PGC already
does that for ordinary software. The open question is whether it holds when one step is a model.
Section 6 answers that question cheaply.

---

## Sources

1. [AI Agent Frameworks (2026 Update): 8 SDKs Compared](https://www.morphllm.com/ai-agent-framework); [2026 AI Agent Framework Showdown](https://qubittool.com/blog/ai-agent-framework-comparison-2026)
2. [Amazon Bedrock AgentCore Policy Implementation Guide](https://hidekazu-konishi.com/entry/amazon_bedrock_agentcore_policy_implementation_guide.html); [Alibaba Cloud Agent Identity policy](https://help.aliyun.com/en/agentidentity/policy-description)
3. Millstone et al., [Out-of-Band Policy Enforcement at a Trusted Tool Boundary](https://arxiv.org/abs/2608.27646), arXiv:2608.27646
4. Debenedetti et al., [Defeating Prompt Injections by Design (CaMeL)](https://arxiv.org/abs/2503.18813), arXiv:2503.18813
5. [CaMeL summary, including the multi-agent composition result](https://signals.aktagon.com/articles/2026/07/camel-defeating-prompt-injection-attacks-in-llm-agents-through-capability-based-security/)
6. [AI agent governance now demands deterministic guardrails](https://nhimg.org/articles/ai-agent-governance-now-demands-deterministic-guardrails-and-identity-controls/); [Agents Are Doers: Why AI Guardrails Aren't Enough](https://www.rubrik.com/blog/ai/26/4/agents-are-doers-why-ai-guardrails-are-not-enough)
7. Kurady et al., [Compositional Policy Violations](https://arxiv.org/abs/2609.18820), arXiv:2609.18820
8. Quessada-Vial, [Agentic Configuration Management](https://arxiv.org/abs/2608.11166), arXiv:2608.11166
9. [Temporal: dynamic AI agents](https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal); [Temporal Google ADK integration](https://docs.temporal.io/develop/go/integrations/google-adk)
10. [OWASP Agentic Top 10, explained](https://www.speakeasy.com/blog/owasp-agentic-top-10-explained); [promptfoo OWASP agentic mapping](https://www.promptfoo.dev/docs/red-team/owasp-agentic-ai/)
11. [What the EU AI Act requires for AI agent logging](https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/)
