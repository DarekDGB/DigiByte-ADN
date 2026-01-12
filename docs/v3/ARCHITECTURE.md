# 🛡️ Active Defence Network (ADN) — Architecture v3
### Shield Contract v3 • Deterministic • Fail-Closed • Coverage-Gated

ADN is the **local defence engine** in the DigiByte Quantum Shield stack.

It sits **above Sentinel AI and DQSN**, consuming their signals and converting them into a
**deterministic, fail-closed contract response**.

---

## 1. What “ADN v3” means

**ADN v3 is a contract gate + deterministic envelope**.

- `adn_v3` is the **authoritative v3 contract package**
- The v3 contract **calls the existing v2 engine** for behavior (for now)
- This preserves **no-behavior-drift** while adding:
  - strict parsing
  - deny-by-default schema
  - explicit reason codes
  - deterministic context hashing
  - CI coverage gate on v3 surface

**Public import (authoritative):**
```python
from adn_v3 import ADNv3
```

**Legacy import (deprecated compatibility only):**
```python
from adn_v2.v3 import ADNv3  # deprecated, re-exports adn_v3.ADNv3
```

---

## 2. Role in the Shield

ADN is a **local decision layer**.

It:
- consumes signal-like events (e.g. from DQSN / Sentinel AI)
- evaluates local risk and lockdown state
- emits deterministic contract responses

It does **not**:
- hold keys
- sign transactions
- change chain consensus
- perform network calls inside the contract response

---

## 3. v3 Data Flow (conceptual)

```
[ Sentinel AI signals ]      [ DQSN aggregation ]
         ↓                           ↓
   (events normalized into v3 request envelope)
                      ↓
               [ ADN v3 Contract ]
                      ↓
              deterministic response:
     decision + reason_codes + context_hash + actions
```

---

## 4. Determinism + Fail-Closed invariants

**Determinism**
- `context_hash` is computed from a canonical payload (`canonical_sha256`)
- No timestamps / runtime timing in hash inputs
- Stable JSON canonicalization (sorted keys, stable separators)

**Fail-Closed**
- unknown keys rejected
- NaN / Infinity rejected anywhere in request
- oversize event lists rejected
- oversize metadata rejected
- invalid schema → `decision="ERROR"` with explicit `reason_codes`

---

## 5. Contract boundaries (what v3 controls)

ADN v3 is responsible for:
- parsing `ADNv3Request` (strict)
- mapping v3 events into internal `DefenseEvent`
- calling `evaluate_defense(...)` (legacy behavior engine)
- converting engine state into:
  - `decision` (ALLOW/WARN/BLOCK or ERROR)
  - `reason_codes`
  - deterministic `context_hash`

ADN v3 intentionally keeps evidence minimal:
- `active_events_count` only (no internal leakage)

---

## 6. Repo layout (authoritative)

### v3 contract package (authoritative)
```
src/adn_v3/
├── __init__.py              # exports ADNv3
├── core.py                  # ADNv3 contract gate (authoritative)
└── contracts/
    ├── v3_types.py          # strict request parsing + NaN/Inf rejection
    ├── v3_reason_codes.py   # explicit reason codes
    └── v3_hash.py           # canonical_sha256 (deterministic)
```

### v2 legacy package (still used by v3 for behavior)
```
src/adn_v2/
├── engine.py                # evaluate_defense(...) behavior engine
├── models.py                # DefenseEvent, NodeDefenseState, enums
├── config.py                # NodeDefenseConfig defaults
├── policy.py / actions.py   # policy + action helpers (legacy)
├── telemetry.py             # adapter (legacy, deterministic defaults)
└── v3.py                    # DEPRECATED shim -> re-exports adn_v3.ADNv3
```


---

## 7. License

MIT License  
© 2026 DarekDGB
