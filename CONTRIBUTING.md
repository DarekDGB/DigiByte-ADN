# Contributing to ADN v2 (Active Defence Network)

**ADN v2** is the **Active Defence Network** layer in the DigiByte Quantum Shield.

It consumes signals from **DQSN v2** and **Sentinel AI v2**, then coordinates
defensive *recommendations* and *tactical responses* for higher layers such as:

- Quantum Wallet Guard (QWG)
- Guardian Wallet
- Node operators and tooling

ADN is **advisory and orchestration only**.  
It does **not** change DigiByte consensus, rules, or block validity.

This repository is a **reference architecture & implementation skeleton** for
DigiByte Core developers and security researchers.

---

## ✅ What Contributions Are Welcome

### ✔️ Extensions & Improvements

- New defence playbooks and strategies (e.g. how to react to certain threats)
- Improved risk aggregation and prioritisation logic
- Better routing of signals to different consumer types (nodes, wallets, services)
- Performance, reliability, and robustness improvements
- Additional simulation scenarios and test harnesses
- Documentation clarifications and diagrams

### ✔️ Security & Reliability Fixes

- Hardening of decision logic
- More deterministic behaviour
- Better error handling and fallback strategies
- Improved logging and audit traces

---

## ❌ What Will Not Be Accepted

### 🚫 Removing or weakening core architecture

ADN v2 has clearly defined responsibilities:

- Consume signals from **DQSN v2** and **Sentinel AI v2**
- Fuse and prioritise risk
- Select appropriate defensive playbooks
- Emit *recommendations* and *signals* to higher layers

Any PR that:

- removes core modules or planes
- attempts to collapse ADN into another layer
- downgrades it to a trivial “if/else” wrapper
- strips out key functionality (e.g. playbook engine, signal router)

…will be rejected.

### 🚫 Consensus or Governance Changes

ADN v2 **must not**:

- modify DigiByte’s consensus rules
- enforce or veto blocks
- participate in fork choice
- become a voting or governance layer

ADN is **advisory**. It recommends; it does not rule.

### 🚫 Black-Box Behaviour

Avoid:

- opaque ML models with no explainability
- behaviour that cannot be traced, logged, or audited
- hidden thresholds that operators cannot reason about

All actions and decisions must remain understandable to humans.

---

## 🧱 Design Principles

All contributions should respect these principles:

1. **Advisory, Not Authoritarian**  
   ADN recommends tactics; it never forces network behaviour.

2. **Explainability**  
   For any decision, there should be a clear “why” available in logs or traces.

3. **Composability**  
   New playbooks and strategies should plug into existing dispatch and routing logic cleanly.

4. **Determinism Where Possible**  
   Given the same inputs, ADN should behave predictably.

5. **Auditability**  
   Security teams and operators must be able to reconstruct how a decision was made.

6. **Interoperability**  
   Outputs must remain useful to QWG, Guardian Wallet, node tooling, and external dashboards.

---

## 🔄 Pull Request Expectations

A PR should include:

- A clear description of *what* is being added or changed
- Motivation: *why* this improves ADN
- Tests where appropriate (unit / simulation / integration)
- No breaking folder structure without strong justification
- No removal of core architectural components

The original architect (@DarekDGB) reviews **direction and architectural fit**.  
DigiByte developers and contributors review **technical implementation details**.

If you are unsure whether a change fits the vision, open an issue first and
discuss the concept before submitting a PR.

---

## 📝 License

By contributing, you agree that your contributions are licensed under the
MIT License, the same as the rest of the project.

© 2025 **DarekDGB**
