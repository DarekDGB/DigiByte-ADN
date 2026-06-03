# ⚔️ DigiByte ADN v3.2.0 — Active Defense Network

![ADN Tests](https://github.com/DarekDGB/DigiByte-ADN/actions/workflows/tests.yml/badge.svg)
![Coverage 100%](https://img.shields.io/badge/coverage-100%25-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-ORCHESTRATOR--BOUNDARY--LOCKED-critical)

**Deterministic Local Defence Engine • Risk → Policy → Decision Evidence**  
**Architecture & Implementation by @DarekDGB — MIT Licensed**

---

## Purpose

**ADN v3.2.0 — Active Defense Network** is the deterministic local defense decision engine of the **DigiByte Quantum Shield**.

ADN converts validated defensive context into deterministic local policy decisions and provides structured decision evidence to the Shield stack.

Where:

- **Sentinel AI v3** detects anomalies and emits structured threat signals.
- **DQSN v3** validates, deduplicates, and aggregates those signals deterministically.
- **ADN v3** evaluates local defense posture and produces deterministic decision evidence.
- **Shield Orchestrator v3** is the only final Shield receipt boundary for AdamantineOS handoff.

ADN operates using a strict, testable, fail-closed contract.

ADN does **not**:

- modify DigiByte consensus rules
- sign transactions
- broadcast transactions
- hold, derive, or access private keys
- approve AdamantineOS execution directly
- override the Shield Orchestrator

ADN governs **local defensive behavior only**.

---

## Position in the DigiByte Quantum Shield

```text
┌───────────────────────────────────────────────┐
│              AdamantineOS                     │
│   Consumes only Shield Orchestrator receipt   │
└───────────────────────────────────────────────┘
                       ▲
                       │ deterministic receipt only
┌───────────────────────────────────────────────┐
│          Shield Orchestrator v3               │
│   Final Shield aggregation + receipt boundary │
└───────────────────────────────────────────────┘
                       ▲
                       │ component verdict evidence
┌───────────────────────────────────────────────┐
│                 ADN v3                        │
│   Deterministic local defence decision engine │
│   Risk → Policy → Decision Evidence           │
└───────────────────────────────────────────────┘
                       ▲
                       │ aggregated signals
┌───────────────────────────────────────────────┐
│               DQSN v3                         │
│   Deterministic signal aggregation            │
└───────────────────────────────────────────────┘
                       ▲
                       │ raw threat signals
┌───────────────────────────────────────────────┐
│            Sentinel AI v3                     │
│   Anomaly and threat detection                │
└───────────────────────────────────────────────┘
```

ADN is an **evidence-producing defense component**.

It is **not** the final AdamantineOS execution authority.

---

## Core Mission

### Deterministic Risk → Decision

ADN converts validated defensive context into deterministic policy decisions.

Same valid input must always produce the same output.

### Fail-Closed by Default

ADN rejects unsafe input conditions, including:

- unknown keys
- invalid schema
- NaN / Infinity values
- oversized inputs
- unserialisable payloads
- unsupported contract versions
- ambiguous authority claims

Errors must always be explicit and test-covered.

### Local Enforcement Intent

ADN may map decisions into local defense states, warnings, lockdown intent, or allow intent.

This remains local defense behavior only.

It does not create signing authority, consensus authority, or final execution authority.

### Orchestrator-First Handoff

For v3.2.0 integration, ADN verdict data is evidence only.

AdamantineOS must consume Shield decisions only through the deterministic **Shield Orchestrator receipt**.

Raw ADN outputs are not final execution authority.

---

## What v3 Means

**ADN v3 separates contract from legacy behavior.**

- `adn_v3` is the authoritative v3 contract layer.
- `adn_v2` is the legacy behavior engine and compatibility layer.

This preserves:

- deterministic contract safety
- stable v3 imports
- zero unintended behavior drift
- future-safe Shield upgrades

Public import:

```python
from adn_v3 import ADNv3
```

---

## Repository Layout

```text
DigiByte-ADN/
├─ README.md
├─ LICENSE
├─ CONTRIBUTING.md
├─ CHANGELOG.md
├─ SECURITY.md
├─ docs/
│  ├─ v2/                         # legacy reference docs
│  └─ v3/                         # authoritative v3 docs
│     ├─ ARCHITECTURE.md
│     ├─ CONTRACT.md
│     ├─ EVIDENCE_FAMILIES.md
│     ├─ INDEX.md
│     ├─ MANIFEST.md
│     ├─ PROOF_PACK.md
│     ├─ REASON_IDS.md
│     └─ TEST_MATRIX.md
├─ tests/
│  ├─ test_v3_full_coverage_lock.py
│  └─ test_v3_2_manifest_verdict_lock.py
└─ src/
   ├─ adn_v3/                     # v3 contract boundary — authoritative
   │  ├─ core.py
   │  ├─ py.typed
   │  └─ contracts/
   │     ├─ v3_hash.py
   │     ├─ v3_reason_codes.py
   │     ├─ v3_types.py
   │     └─ v3_2_lock.py
   └─ adn_v2/                     # legacy behavior engine
      ├─ engine.py
      ├─ models.py
      ├─ config.py
      ├─ py.typed
      └─ v3.py                    # deprecated shim → adn_v3
```

---

## v3.2.0 Manifest / Verdict Lock

ADN v3.2.0 includes the Shield manifest / registry / canonical verdict lock required before AdamantineOS integration.

The v3.2.0 lock enforces:

- component identity discipline
- contract version discipline
- stable reason ID registration
- stable evidence-family registration
- deterministic canonical verdict data
- fail-closed rejection of malformed verdict inputs
- Orchestrator-first handoff assumptions

ADN remains evidence-only.

It cannot:

- sign
- broadcast
- hold keys
- expand authority
- override the Shield Orchestrator
- approve AdamantineOS execution directly

See:

- `docs/v3/MANIFEST.md`
- `docs/v3/REASON_IDS.md`
- `docs/v3/EVIDENCE_FAMILIES.md`
- `docs/v3/TEST_MATRIX.md`
- `docs/v3/PROOF_PACK.md`

---

## Tests & Security Guarantees

CI enforces **100% coverage on `adn_v3`**.

Security and regression tests enforce:

- strict schema validation
- fail-closed behavior
- deterministic hashing
- oversized input rejection
- malformed input rejection
- unsupported contract version rejection
- reason-code stability
- evidence-family stability
- manifest/verdict alignment
- no hidden authority
- no silent fallback
- v3.2.0 contract lock behavior

Legacy `adn_v2` remains packaged but is not the authoritative v3 coverage boundary.

Tests define truth.

No release is locked unless CI proves the contract surface.

---

## v3.2.0 Status

ADN is aligned with the Shield v3.2.0 integration-boundary track:

- package metadata set to `3.2.0`
- `adn_v3` remains the authoritative v3 contract boundary
- `v3_2_lock.py` lives under `src/adn_v3/contracts/`
- manifest / reason ID / evidence-family docs are present
- v3.2.0 verdict lock tests are present
- deterministic contract behavior is preserved
- no consensus authority is added
- no signing, broadcasting, key custody, or hidden execution authority is added
- AdamantineOS must consume Shield through the Orchestrator receipt only

Do **not** tag v3.2.0 until the final roadmap checklist, fresh ZIP audit, CI proof, and Red Team report are complete.

---

## Shield v3 Invariants

ADN v3 follows the Shield v3 baseline invariants:

- **Deny-by-default** — anything not explicitly allowed is rejected.
- **Fail-closed** — invalid, ambiguous, partial, or unsafe input is rejected.
- **Deterministic execution** — same valid input must produce the same output.
- **No silent fallback** — failures must surface as explicit reasoned rejections.
- **Contract-first behavior** — the v3 interface is the authoritative safety boundary.
- **Local-only enforcement** — ADN never modifies consensus and never signs transactions.
- **Orchestrator-first handoff** — AdamantineOS receives Shield state only through the deterministic Orchestrator receipt.

Any violation of these invariants is a security defect.

---

## Documentation

- Start here: `docs/v3/INDEX.md`
- Architecture: `docs/v3/ARCHITECTURE.md`
- Contract: `docs/v3/CONTRACT.md`
- Manifest: `docs/v3/MANIFEST.md`
- Reason IDs: `docs/v3/REASON_IDS.md`
- Evidence Families: `docs/v3/EVIDENCE_FAMILIES.md`
- Test Matrix: `docs/v3/TEST_MATRIX.md`
- Proof Pack: `docs/v3/PROOF_PACK.md`
- Legacy reference: `docs/v2/`

---

## Contribution Policy

See `CONTRIBUTING.md`.

Rules:

- No consensus-touching behavior.
- No signing or broadcasting behavior.
- No private-key custody behavior.
- No AdamantineOS direct execution approval.
- Deterministic decisions only.
- Explicit enforcement outputs only.
- Tests required for contract changes.
- No reduction of the `adn_v3` 100% coverage gate.
- No bypass of the Shield Orchestrator receipt boundary.

---

## License

MIT License  
© 2025 **DarekDGB**
