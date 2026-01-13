# ⚔️ ADN v3 — Active Defence Network

![ADN Tests](https://github.com/DarekDGB/DigiByte-ADN/actions/workflows/tests.yml/badge.svg)
![Coverage ≥90%](https://img.shields.io/badge/coverage-%E2%89%A590%25-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

### *Deterministic Local Defence Engine • Risk → Policy → Decision*
**Architecture & Implementation by @DarekDGB — MIT Licensed**

---

## 🚀 Purpose

**ADN v3 (Active Defence Network)** is the **deterministic local defence decision engine**
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

```
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

```
DigiByte-ADN/
├─ README.md
├─ LICENSE
├─ CONTRIBUTING.md
├─ docs/
│  ├─ v2/                  # legacy reference docs
│  └─ v3/                  # authoritative v3 docs
└─ src/
   ├─ adn_v3/               # v3 contract (authoritative)
   │  ├─ core.py
   │  └─ contracts/
   │     ├─ v3_types.py
   │     ├─ v3_reason_codes.py
   │     └─ v3_hash.py
   └─ adn_v2/               # legacy behaviour engine
      ├─ engine.py
      ├─ models.py
      ├─ config.py
      └─ v3.py              # deprecated shim → adn_v3
```

---

## 🧪 Tests & Security Guarantees

- CI enforces **≥90% coverage on `adn_v3`**
- Determinism tested explicitly
- Fail-closed behaviour tested on invalid inputs
- Legacy code is *not* coverage-gated

This ensures **contract safety without fake tests**.

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

---

## 📜 License

MIT License  
© 2025 **DarekDGB**
