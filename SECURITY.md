# Security Policy - DigiByte ADN

**Repository:** DigiByte-ADN
**Component:** ADN - Shield v4 candidate and retained v3 compatibility
**Maintainer:** DarekDGB
**License:** MIT

This document defines the security policy and disclosure process for the
DigiByte Active Defense Network's **Shield v4 evidence boundary and retained
ADN v3 contract**.

---

## Supported Versions

Distribution 4.0.0 is a controlled pre-release candidate. New v4 evidence work
uses `adn_v3.v4`; the existing v3 contract remains a separate compatibility surface.

| Component | Status |
|---|---|
| ADN v4 (`adn_v3.v4`) | Current controlled candidate evidence surface; not released |
| ADN v3 (`adn_v3`) | Retained deterministic contract; frozen 3.2.0 manifest |
| ADN v2 (`adn_v2`) | Legacy behavior engine and compatibility code |
| Older versions | Unsupported |

Legacy documentation may remain in the repository for historical reference, but it is **non-authoritative** for current v4 security claims.

---

## Security Model

ADN's retained v3 engine provides deterministic, fail-closed local defense
contracts. The parallel v4 surface produces and verifies component evidence.
Canonical payloads are deterministic for explicit inputs; native key generation
and signature bytes need not be deterministic.

Security is enforced through:

- strict input validation
- explicit contract boundaries
- deterministic outputs
- deny-by-default semantics
- stable reason codes
- canonical context hashing
- CI-enforced 100% coverage on the `adn_v3` surface

ADN remains **consensus-neutral**.

It does not:

- alter DigiByte consensus rules
- sign transactions
- broadcast transactions
- hold, derive, or access wallet private keys
- perform final wallet execution approval

All ADN decisions affect **local defensive behavior only**, such as wallet wrappers, node wrappers, RPC-layer wrappers, policy gates, or Shield orchestration evidence.

---

## Non-Negotiable Design Invariants

The following invariants must never be violated.

### 1. Fail-Closed by Default

Any invalid, ambiguous, incomplete, unsafe, or malformed input must produce an explicit rejection path.

Expected fail-closed behavior includes:

- deterministic error or deny decision
- explicit reason code
- no silent fallback
- no implicit allow
- no authority escalation

### 2. Determinism

The same explicit contract inputs must produce the same canonical decision
and payload. Native signature bytes are not subject to that determinism claim.
V4 freshness fields are supplied explicitly and bound by signatures. Verifiers
must apply their time, policy, and replay state; the payload alone is not an
independent replay store.

Contract decisions must not implicitly depend on:

- ambient wall-clock reads
- randomness
- environment state
- network state
- file-system state
- dictionary iteration order
- runtime-dependent side effects

`context_hash` must be canonical and reproducible.

### 3. Explicit Authority Boundaries

ADN may:

- consume defensive signals
- evaluate local risk context
- produce deterministic decision evidence
- provide evidence to the Shield Orchestrator
- sign v4 component evidence using separately supplied evidence keys

ADN must never:

- sign transactions
- modify consensus behavior
- perform network I/O inside the contract surface
- approve AdamantineOS execution directly
- override the Shield Orchestrator
- create hidden authority through fallback behavior

### 4. No Silent Fallbacks

All error paths must be explicit, deterministic, and test-covered.

A fallback that changes authority, weakens validation, or allows execution is a security defect.

### 5. Coverage-Gated Contract Surface

The `adn_v3` contract surface must remain coverage-gated at **100%**.

Legacy `adn_v2` is not the authoritative v3 security surface.

---

## Orchestrator-First Security Boundary

The retained v3.2.0 manifest and parallel v4 evidence path both preserve the
Shield component / Orchestrator receipt / AdamantineOS boundary.

ADN component verdicts are **evidence only**.

ADN must not be treated as final execution authority.

AdamantineOS must consume Shield decisions only through the deterministic **Shield Orchestrator receipt**.

Raw ADN outputs must not be consumed directly by AdamantineOS as final signing, execution, or approval authority.

A Shield `ALLOW` result only permits AdamantineOS to continue its own checks.

It is **not** final signing or execution approval.

---

## V4 Cryptographic Policy and Limits

The required `classical-ed25519` and `ml-dsa` paths use strict AND semantics.
The optional `fn-dsa` path stays last in canonical order, cannot replace or
rescue required evidence, and is fatal when present but invalid. Profile, role,
domain, key, and signed-payload bindings remain mandatory.

OQS adapters provide ML-DSA-65 and draft Falcon-1024 backend paths for evidence.
This repository does not supply a production classical Ed25519 backend, an
HSM integration proof, or a FIPS-validated deployment. A production deployment
must satisfy every required policy path. No real-to-TEST-ONLY fallback is allowed.
The profile `fips206-draft-falcon1024-v1` is not a final FIPS 206 claim.

## Fail-Closed Requirements

The following conditions must reject deterministically:

- missing required verdict data
- malformed verdict data
- unknown fields in strict contract paths
- duplicated authority claims
- unknown reason IDs
- unknown evidence families
- mismatched component identity
- mismatched contract version
- mismatched context hash
- unsafe or unserialisable input
- non-canonical verdict data
- ambiguity affecting authority, determinism, or auditability

---

## Security Testing

The suite checks contract behavior through tests covering:

- schema validation
- fail-closed behavior
- deterministic hashing
- oversize input handling
- malformed input handling
- unsupported contract versions
- reason-code stability
- evidence-family validation
- manifest/verdict alignment
- Orchestrator-first boundary assumptions
- regression protection against behavior drift

Security-sensitive changes must include tests.

Tests define truth.

Documentation must never claim behavior that tests do not enforce.

---

## Release Requirements

The `v4.0.0` candidate is not released or tagged. Current status is recorded in
[the v4 release-status document](docs/v4/RELEASE_STATUS_v4.0.0.md).
A release decision requires all of the following:

- roadmap checklist is complete
- standard CI passes on the exact release-candidate commit
- dedicated native-OQS proof runs both locked nodes with zero skips, failures, or errors on that same commit
- CI coverage gate remains at 100%
- manifest files are present and aligned
- reason IDs are documented and tested
- evidence families are documented and tested
- verdict boundary tests pass
- Orchestrator receipt boundary is respected
- final fresh ZIP audit is complete
- Red Team report is complete
- no docs-vs-tests mismatch remains

---

## Reporting a Vulnerability

If you believe you have found a security issue:

1. Do **not** disclose it publicly first.
2. Open a private security advisory through GitHub if available.
3. Alternatively, contact the maintainer through the GitHub profile: **@DarekDGB**.

Please include:

- clear description of the issue
- steps to reproduce, if applicable
- expected behavior
- actual behavior
- affected commit hash or tag
- potential security impact

Coordinated disclosure is strongly encouraged.

---

## In Scope

Security issues in scope include:

- ADN v4 evidence and retained v3 contract behavior
- determinism violations
- fail-closed bypasses
- reason ID ambiguity
- evidence-family ambiguity
- manifest/verdict mismatch
- context hash mismatch
- Orchestrator boundary bypass risk
- AdamantineOS raw-output bypass risk
- CI or test coverage gaps affecting security

---

## Out of Scope

The following are out of scope unless they create a direct security defect:

- DigiByte consensus vulnerabilities
- mining-layer issues
- network-layer attacks outside ADN contract behavior
- wallet UI preferences
- performance tuning
- cosmetic documentation changes
- non-security refactors
- unsupported archived behavior

---

## Security Updates

Security fixes may:

- tighten validation
- improve fail-closed behavior
- add negative tests
- update documentation
- clarify reason IDs or evidence families

Breaking changes to security semantics require:

- documentation updates
- explicit version notes
- regression tests
- coverage proof

---

## Disclaimer

This software is provided **as-is**, without warranty of any kind.

Use at your own risk.

---

## Final Security Rule

Any change that weakens determinism, fail-closed behavior, explicit authority boundaries, or the Orchestrator-first receipt model must be rejected.

Copyright (c) 2025 DarekDGB
