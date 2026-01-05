# Risk Validator – DigiByte ADN v2

## Overview

The **RiskValidator** module is responsible for transforming raw telemetry
metrics into normalized **RiskSignal** objects.  
These signals are then passed into the Policy Engine to determine the
appropriate security posture for the node.

This validator acts as the *bridge* between real‑world node activity and
the internal decision logic of ADN v2.

---

## Responsibilities

### 1. Convert TelemetryPacket → List[RiskSignal]
The validator examines fields inside the telemetry packet:

- **peer_count**
- **mempool_size**
- **height**
- **timestamp**
- **extra metadata**

and transforms them into structured risk assessments.

---

## v2 Reference Heuristics

The ADN v2 reference implementation includes simple rules:

### 🟡 Low Peer Count
```
peer_count < 2  →  RiskLevel.ELEVATED
```
Reason:  
Low peers may indicate isolation, network issues, eclipse attempts, or
poor connectivity.

---

### 🔴 Mempool Spike
```
mempool_size > 20000  →  RiskLevel.HIGH
```
Reason:  
Large mempool surges may indicate congestion, spam attacks, or sudden
network instability.

---

### 🟢 Normal Baseline
If no risk patterns are detected:
```
RiskLevel.NORMAL (score=0.1)
```
This ensures the Policy Engine always receives at least one signal for
every telemetry packet.

---

## Data Model (for reference)

### RiskSignal
```python
@dataclass
class RiskSignal:
    source: str
    level: RiskLevel
    score: float
    details: Dict[str, Any]
```

### RiskLevel Enum
```
NORMAL
ELEVATED
HIGH
CRITICAL
```

---

## Example Output

### Example 1 — Healthy Node
```
Telemetry:
  peer_count: 8
  mempool_size: 300

RiskSignal:
  source: "telemetry"
  level: NORMAL
  score: 0.1
```

### Example 2 — Low Peers
```
Telemetry:
  peer_count: 1
  mempool_size: 500

RiskSignals:
  - source: "telemetry"
    level: ELEVATED
    score: 0.6
    details: {reason: "low_peer_count"}
```

### Example 3 — Large Mempool Spike
```
Telemetry:
  peer_count: 5
  mempool_size: 35000

RiskSignals:
  - source: "telemetry"
    level: HIGH
    score: 0.8
    details: {reason: "mempool_spike"}
```

---

## Extending the Validator (v3+)

Node operators or other blockchains adopting ADN can implement more
advanced validators:

- entropy monitoring  
- nonce‑reuse detection  
- orphan‑rate patterns  
- time‑warp anomalies  
- Sentinel AI score fusion  
- DQSN global‑network scores  
- wallet‑guard withdrawal anomalies  
- quantum signature irregularities  

These systems can plug‑in **without modifying** the core engine.

---

## File Location

```
src/adn_v2/validator.py
```

This module is automatically imported by ADNEngine during the pipeline:
```
telemetry → validator → policy → actions
```

---

## Author  
**DarekDGB**

