# Matters Left Unresolved

Each entry uses the required provenance shape. These matters were looked for in the named sources and were not determined sufficiently to support a stronger claim. They are findings against the standard, not silent profile decisions.

## Finding F-1

**Matter:** Canonical machine-readable representation of a profile, including how a checker obtains the exact profile document named by identity.

**Source basis:** Normative Platform Profile §§9, 11; Conformance Model §2; commission §6.

**Claim type:** unresolved.

**Reasoning:** The profile standard requires an identity and says the form of a profile is unspecified. The named sources do not define a canonical encoding, publication mechanism, or identity-to-document resolution rule. NPP-D can name its identity in prose but cannot claim interoperable profile retrieval from the family alone.

**Confidence:** high

## Finding F-2

**Matter:** The exact trust-root verification mechanism for the profile document.

**Source basis:** Evidence, Attestation & Provenance §§6.2, 10, 12; Normative Platform Profile §7; commission §7.

**Claim type:** unresolved.

**Reasoning:** The family requires a nameable trust root and delegates its selection, but does not specify how a checker verifies the integrity or authenticity of the root document. NPP-D chose the externally authored profile document as the accepted root, but cannot specify a signature, digest, key, or transport mechanism without introducing a reference-shaped assumption. This limits NPP-D-E to the stated trust-root condition rather than a concrete cryptographic demonstration.

**Confidence:** high

## Finding F-3

**Matter:** The semantic contracts of the profile-selected artifact kinds.

**Source basis:** Kind Vocabulary §§3, 5-6, 9; Machine Block §§6, 9-10; commission §5.6.

**Claim type:** unresolved.

**Reasoning:** The family requires every admitted kind to have a kind contract and registry binding, but it does not provide a universal payload grammar for profile-defined kinds. NPP-D names four kinds and their high-level declarations, but a complete interoperable contract for their payloads cannot be derived from the family alone. A claim requiring those payloads to be interoperable is therefore not supported.

**Confidence:** high

## Finding F-4

**Matter:** The semantic interpretation and interoperability of profile-selected outcome names.

**Source basis:** Capability §§3, 3.2; Normative Platform Profile §7; commission §6.

**Claim type:** unresolved.

**Reasoning:** The family requires outcomes to be closed and enumerated and delegates which outcomes contracts may declare, but it does not define a family-wide vocabulary or semantics for names such as `success`, `failure`, and `refusal`. NPP-D fixes the admissible labels, but cannot claim that independent systems assign identical domain meaning to them without further contract text or profile machinery.

**Confidence:** medium

## Finding F-5

**Matter:** Whether direct access to a sealed representation is a sufficient and uniformly realizable means of reaching an inspection surface across independent realizations.

**Source basis:** Governed Inspection §§2.1, 10; Normative Platform Profile §7; commission §2.

**Claim type:** unresolved.

**Reasoning:** The family requires the profile to state how the read surface is reached but explicitly leaves the means outside the family. It names direct access as an example, but does not specify the authority, identity, or evidence mechanism by which an evaluator obtains that access. NPP-D records direct access as its profile choice, while the concrete access mechanism remains outside the standard.

**Confidence:** medium

## Finding F-6

**Matter:** The exact boundary between a system's one tenant and a separate authority or concern.

**Source basis:** Conceptual Model §§5-6; Governance Closure & Authority §§3-9; Domain Profiles §§2, 4-5; commission §2.

**Claim type:** unresolved.

**Reasoning:** The family supplies tests for authority and defines domains and concerns, but does not define a universal `tenant` concept or a mechanical criterion for proving that a system has one tenant. NPP-D excludes multiple tenant arrangements by scope, but a concrete claim about tenant count needs a realization-specific declaration and determination.

**Confidence:** high

## Finding F-7

**Matter:** A complete, independently fail-capable demonstration set for every possible NPP-D system-instance subject class.

**Source basis:** Conformance Model §§3.1, 7-8; Conformance Test Specification §§2-9; commission §7.

**Claim type:** unresolved.

**Reasoning:** Part VII supplies discharge classes and demonstration requirements but no universal fixture grammar, fixture identity scheme, or realization-independent method for constructing every structural search space. NPP-D therefore states the required classes and failure conditions but does not invent a harness or claim that this prose alone discharges a particular implementation.

**Confidence:** high

## Finding F-8

**Matter:** Whether the profile-selected `npp-d-governance-root` is a valid artifact kind rather than a profile-level declaration that should not be admitted as an artifact.

**Source basis:** Machine Block §6; Governance Semantic Ontology §8; Kind Vocabulary §§2-3, 9; Governed Transformation §5.

**Claim type:** unresolved.

**Reasoning:** The family separates governance assertions, declaration elements, semantic categories, and artifact kinds, and does not enumerate which governance-root representations may be artifacts. NPP-D selected the kind to make the profile's governance-root disposition explicit, but the family alone does not settle whether that representation belongs in the artifact vocabulary. This is a blocking finding for any claim that relies on that kind as interoperable.

**Confidence:** medium

## Findings consequence

NPP-D supports profile-level claims and narrowly stated system claims whose demonstrations supply the missing realization-specific material. It does not claim that the standard alone supplies a machine-readable profile format, cryptographic trust-root mechanism, complete kind contracts, universal tenant test, or universal fixture construction method.
