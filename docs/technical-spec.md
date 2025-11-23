# ADN v2 – Technical Specification

## 1. Overview
Autonomous Defense Node v2 is the execution layer of DigiByte’s 3‑layer + wallet security stack:
DQSN → Sentinel AI v2 → ADN v2 → Wallet Guardian.

ADN v2 receives risk states from Sentinel v2 and enforces real-time defensive actions.

## 2. Responsibilities
- Apply hardened network modes.
- Enforce PQC signing policies.
- Filter malicious peers.
- Slow/stop suspicious transaction propagation.
- Activate emergency consensus safeguards (non-forking).
- Integrate with Wallet Guardian signals.

## 3. Architecture
ADN v2 consists of:
- `rules_engine/` — deterministic defense triggers.
- `pqc_manager/` — post‑quantum activation logic.
- `network_filter/` — peer + region filtering.
- `transaction_guard/` — mempool hardening.
- `orchestration/` — main controller.
- `api/` — interface for wallets, nodes, UIs.

## 4. Risk Levels
Sentinel AI v2 supplies:
NORMAL  
ELEVATED  
HIGH  
CRITICAL  

ADN v2 maps these to escalating defense actions.

## 5. State Machine
- NORMAL → regular operation  
- ELEVATED → warnings + light filtering  
- HIGH → PQC lock-in + peer restrictions  
- CRITICAL → hardened mode + freeze unsafe tx paths  

## 6. PQC Layer
Implements:
- Kyber-based key upgrade triggers  
- Shor/Grover threat mitigation  
- Legacy ECDSA freeze options  

## 7. Network Defense
- Sybil cluster detection  
- Eclipse prevention  
- Region anomaly throttling  

## 8. Transaction Defense
- mempool flood throttling  
- RBF abuse protection  
- suspicious-fee freeze  

## 9. API
Provides:
- `/state`  
- `/harden`  
- `/pqc/upgrade`  
- `/filters/update`  

## 10. Telemetry Inputs
- peers, reorg, entropy, mempool, wallet signals  

## 11. Outputs
- defensive state  
- PQC mode status  
- network filter table  
- transaction policies  

## 12. Security Notes
ADN v2 DOES NOT:
- modify consensus rules  
- fork the network  
- sign transactions  
- manage wallet keys  

It is a “shield layer,” not a validator.

## 13. Future Extensions
- region-level anomaly maps  
- predictive peer isolation  
- encrypted sentinel‑ADN channel  
