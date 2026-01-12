# 🔐 Security Policy — DigiByte ADN (Active Defence Network)

**Repository:** DigiByte-ADN  
**Component:** ADN v3 (Active Defence Network)  
**Maintainer:** DarekDGB  
**License:** MIT

This document defines the **security policy and disclosure process** for the
DigiByte Active Defence Network (ADN), with a focus on the **v3 Shield Contract**.

---

## 🛡️ Security Model Overview

ADN v3 is a **deterministic, fail-closed local defence decision engine**.

Security is enforced through:
- strict input validation
- explicit contract boundaries
- deterministic outputs
- deny-by-default semantics
- CI-enforced test coverage on the v3 surface

ADN v3 is **consensus-neutral**:
- it does not alter DigiByte consensus rules
- it does not sign transactions
- it does not broadcast transactions

All decisions affect **local behaviour only** (wallet, node wrapper, RPC layer).

---

## 🔒 Design Invariants (Non-Negotiable)

The following invariants must never be violated:

1. **Fail-Closed by Default**  
   Any invalid, ambiguous, or malformed input must result in:
   - `decision = ERROR`
   - `meta.fail_closed = true`
   - explicit `reason_codes`

2. **Determinism**  
   - Same inputs → same outputs
   - No timestamps, randomness, or runtime-dependent data in contract decisions
   - `context_hash` must be canonical and reproducible

3. **Explicit Authority Boundaries**  
   ADN:
   - consumes signals
   - produces decisions  
   It must **never**:
   - execute cryptographic signing
   - modify consensus
   - perform network I/O inside the contract surface

4. **No Silent Fallbacks**  
   All error paths must be explicit and test-covered.

5. **Coverage-Gated Contract Surface**  
   - `adn_v3` is coverage-gated (≥90%)
   - legacy `adn_v2` is not coverage-gated

---

## 📦 Supported Versions

| Component | Status |
|---------|--------|
| ADN v3 (`adn_v3`) | ✅ Supported |
| ADN v2 (`adn_v2`) | ⚠️ Legacy (behavior engine only) |

Only **ADN v3** is considered security-relevant for new changes.

---

## 🧪 Security Testing

Security guarantees are enforced via:

- Unit tests for:
  - schema validation
  - fail-closed behaviour
  - deterministic hashing
  - oversize / malformed input handling
- CI enforcement of coverage on `adn_v3`
- Regression tests preventing behavior drift

Security-sensitive changes **must include tests**.

---

## 🐛 Reporting a Vulnerability

If you believe you have found a security issue:

### ✅ Preferred method
- Open a **private security advisory** via GitHub (if available)

### 📧 Alternative
- Contact the maintainer directly via GitHub profile:
  **@DarekDGB**

Please include:
- a clear description of the issue
- steps to reproduce
- expected vs actual behavior
- potential impact assessment

Do **not** disclose vulnerabilities publicly before coordination.

---

## 🚫 Out of Scope

The following are **out of scope** for this repository:
- DigiByte consensus vulnerabilities
- Mining or network-layer attacks
- Wallet UI issues not related to ADN decisions
- Third-party integrations

---

## 🔁 Security Updates

Security fixes:
- are released as normal commits
- may include additional tests and documentation updates
- may tighten validation or fail-closed behavior

Breaking changes to security semantics require:
- documentation updates
- explicit version notes

---

## 📜 Disclaimer

This software is provided **as-is**, without warranty of any kind.
Use at your own risk.

---

© 2026 DarekDGB
