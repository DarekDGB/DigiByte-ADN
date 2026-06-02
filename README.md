# ⚔️ ADN v3.1.0 — Active Defense Network

![ADN Tests](https://github.com/DarekDGB/DigiByte-ADN/actions/workflows/tests.yml/badge.svg)
![Coverage 100%](https://img.shields.io/badge/coverage-100%25-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

### *Deterministic Local Defence Engine • Risk → Policy → Decision*
**Architecture & Implementation by @DarekDGB — MIT Licensed**

---

## 🚀 Purpose

**ADN v3.1.0 (Active Defense Network)** is the **deterministic local defense decision engine**
of the **DigiByte Quantum Shield**.

Where:
- **Sentinel AI v3** detects anomalies and emits structured threat signals
- **DQSN v3** validates, deduplicates, and aggregates those signals deterministically

**ADN v3** is responsible for deciding **what a local environment is allowed to do**:
node wrapper, RPC gateway, or wallet runtime.

It operates using a **strict, testable, fail-closed contract**.

ADN:
- does **not** modify DigiByte consensus rules
- does **not** sign transactions
- governs **local behaviour only**

---

## 🛡️ Position in the DigiByte Quantum Shield (v3)

```text
 ┌───────────────────────────────────────────────┐
 │            Guardian Wallet                    │
 │   User-side defence rules & policies          │
 └───────────────────────────────────────────────┘
                     ▲
                     │   (policy recommendations)
 ┌───────────────────────────────────────────────┐
 │        Quantum Wallet Guard (QWG)             │
 │   Runtime tx / key safety enforcement         │
 └───────────────────────────────────────────────┘
                     ▲
                     │   (execution authority)
 ┌───────────────────────────────────────────────┐
 │                 ADN v3                        │
 │   Deterministic defence decision engine       │
 │   Risk → Policy → Enforcement intent          │
 └───────────────────────────────────────────────┘
                     ▲
                     │   (aggregated signals)
 ┌───────────────────────────────────────────────┐
 │               DQSN v3                         │
 │   Deterministic signal aggregation            │
 └───────────────────────────────────────────────┘
                     ▲
                     │   (raw threat signals)
 ┌───────────────────────────────────────────────┐
 │            Sentinel AI v3                     │
 │   Anomaly & threat detection                  │
 └───────────────────────────────────────────────┘
```

ADN is the **decision authority** for local defence actions.

---

## 🎯 Core Mission (v3)

### ✓ Deterministic risk → decision
- Convert aggregated signals into structured requests
- Produce deterministic policy decisions
  *(same inputs → same outputs)*

### ✓ Fail-closed by default
- Unknown keys rejected
- Invalid schema rejected
- NaN / Infinity rejected anywhere
- Oversized inputs rejected
- Errors always explicit

### ✓ Local enforcement intent
- Map decisions into `NodeDefenseState`
- Emit lockdown / warning / allow decisions
- Provide structured evidence without leaking internals

---

## 🧠 What “v3” means (important)

**ADN v3 separates contract from behaviour.**

- `adn_v3` → **authoritative contract layer**
- `adn_v2` → **legacy behaviour engine (still used)**

This ensures:
- zero behaviour drift
- deterministic contract surface
- future-safe upgrades

Public import:

```python
from adn_v3 import ADNv3
```

---

## 🧩 Repository Layout (authoritative)

```text
DigiByte-ADN/
├─ README.md
├─ LICENSE
├─ CONTRIBUTING.md
├─ CHANGELOG.md
├─ docs/
│  ├─ v2/                  # legacy reference docs
│  └─ v3/                  # authoritative v3 docs
├─ tests/
│  └─ test_v3_full_coverage_lock.py
└─ src/
   ├─ adn_v3/               # v3 contract (authoritative)
   │  ├─ core.py
   │  ├─ py.typed
   │  └─ contracts/
   │     ├─ v3_types.py
   │     ├─ v3_reason_codes.py
   │     └─ v3_hash.py
   └─ adn_v2/               # legacy behaviour engine
      ├─ engine.py
      ├─ models.py
      ├─ config.py
      ├─ py.typed
      └─ v3.py              # deprecated shim → adn_v3
```

---

## 🧪 Tests & Security Guarantees

- CI enforces **100% coverage on `adn_v3`**
- Determinism tested explicitly
- Fail-closed behaviour tested on invalid inputs
- Legacy `adn_v2` remains packaged but is not the v3 coverage boundary
- The authoritative v3 contract layer must remain fully covered

This ensures **contract safety without fake tests or uncovered v3 branches**.

### v3.1.0 hardening status

ADN is aligned with the Shield v3.1.0 hardening track:

- package metadata set to `3.1.0`
- Active Defense Network naming corrected
- `adn_v3` remains coverage-gated at 100%
- deterministic contract behavior preserved
- no consensus authority added
- no signing, broadcasting, or hidden execution authority added

### v3.1.0 CI Proof

```text
39 passed
172 statements
0 missed
100% coverage
Required test coverage of 100% reached.
```

---

## 🔒 Shield v3 Invariants

ADN v3 follows the Shield v3 baseline invariants:

- **Deny-by-default** — anything not explicitly allowed is rejected
- **Fail-closed** — invalid, ambiguous, partial, or unsafe input is rejected
- **Deterministic execution** — same valid input must produce the same output
- **No silent fallback** — failures must surface as explicit reasoned rejections
- **Contract-first behaviour** — the v3 interface is the authoritative safety boundary
- **Local-only enforcement** — ADN never modifies consensus and never signs transactions

Any violation of these invariants is a security defect.

---

## 📚 Documentation

- **Start here:** `docs/v3/INDEX.md`
- **Architecture:** `docs/v3/ARCHITECTURE.md`
- **Contract:** `docs/v3/CONTRACT.md`
- **Legacy reference:** `docs/v2/`

---

## 🤝 Contribution Policy

See `CONTRIBUTING.md`.

Rules:
- No consensus-touching behaviour
- Deterministic decisions only
- Explicit enforcement outputs
- Tests required for contract changes
- No reduction of the `adn_v3` 100% coverage gate

---

## 📜 License

MIT License
© 2025 **DarekDGB**
