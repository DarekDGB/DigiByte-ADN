# DigiByte Autonomous Defense Node v2 (ADN v2)

**ADN v2** is the upgraded Layer‑3 autonomous protection engine of DigiByte’s 5‑Layer Quantum Shield.  
It operates between Sentinel AI v2 (detection) and Wallet Guardian (local wallet defence), executing **real‑time actions**, enforcing **policy rules**, and communicating with **DQSN** to maintain chain integrity.

---

## 🚀 Mission  
To provide DigiByte with a **fully automated defence layer** capable of responding instantly to:
- quantum‑related key extraction attempts  
- deep reorganisations  
- timestamp manipulation  
- sudden spikes in mempool entropy  
- coordinated multi‑node attacks  
- hostile or suspicious node behaviour  
- abnormal propagation patterns  

---

## 🧩 Layers Working Together  
ADN v2 is part of the 5‑Layer Quantum Shield:

```
DGB Core
   ▲
Wallet Guardian (Layer 5)
   ▲
ADN v2 – Autonomous Defense Node (Layer 4)
   ▲
DQSN – Quantum Shield Network (Layer 3)
   ▲
Sentinel AI v2 – Detection Engine (Layer 2)
   ▲
Node / Chain Observability (Layer 1)
```

---

## 📁 Repository Structure

```
DigiByte-ADN-v2/
│
├── README.md
├── LICENSE
│
├── src/
│   └── adn_v2/
│       ├── __init__.py
│       ├── actions.py
│       ├── cli.py
│       ├── client.py
│       ├── config.py
│       ├── engine.py
│       ├── main.py
│       ├── models.py
│       ├── policy.py
│       ├── server.py
│       └── telemetry.py
│
└── docs/
    ├── technical-spec.md
    └── whitepaper-adn-v2.md
```

---

## 🔥 Core Components (What Each File Does)

### **`engine.py`**
Central brain of ADN v2.  
It merges:
- live telemetry  
- validator results  
- risk states  
- actions  
- configuration  

### **`policy.py`**
Defines all enforcement behaviour:
- thresholds  
- cooldown rules  
- escalation rules  
- hardened‑mode logic  

### **`actions.py`**
Executes automated responses:
- slow down block processing  
- lock RPC  
- isolate node  
- broadcast anomaly packets  
- notify DQSN  

### **`telemetry.py`**
Ingests real‑time metrics from:
- mempool  
- block templates  
- peer list  
- difficulty  
- network entropy  

### **`validator.py`**
Runs checks:
- reorg depth  
- timestamp drift  
- quantum signature anomalies  
- entropy collapses  

### **`client.py`**
Outbound messaging:
- ADN → Sentinel AI  
- ADN → DQSN  

### **`server.py`**
Inbound server:
- receives signals from other ADN nodes  
- receives warnings from DQSN  

### **`cli.py`**
Local command‑line interface for:
- checking risk  
- forcing hardened mode  
- exporting logs  

---

## 🛡️ ADN v2 Modes

### **Normal**
Everything behaves normally  
→ monitoring active

### **Elevated**
Minor anomalies  
→ warnings, additional validation

### **High**
Confirmed suspicious behaviour  
→ multi‑step confirmation, optional RPC lockdown

### **Critical**
High confidence of attack  
→  
- hard‑lock wallet  
- freeze block signing  
- isolate node  
- notify DQSN  
- force hardened mode

---

## 📜 Early Milestone v0.1 (Completed)
- ✔ baseline policy engine  
- ✔ risk state tracking  
- ✔ hardened mode  
- ✔ basic anomaly validators  
- ✔ telemetry ingestion  
- ✔ ADN CLI  
- ✔ inter-node signalling  
- ✔ full repo structure  

---

## 🗺️ Roadmap (Vision)
### **v0.2 – Full Network Behaviour Model**
- predictive risk scoring  
- behaviour fingerprinting  
- node reputation map  

### **v0.3 – Clustered ADN Mesh**
- multiple ADN nodes forming a mesh  
- shared risk packets  
- distributed validation  

### **v1.0 – Production‑Ready ADN**
- plug‑and‑play deployment  
- GUI dashboard  
- integration with Wallet Guardian  
- integration with Sentinel AI v2 & DQSN  

---

## 🤝 Open‑Source & Community  
This project is open-source under the MIT license.  
It is built for DigiByte, its community, and future generations.

If you want to contribute, open an issue or PR.  
Your help strengthens the network.

---

## ✨ Vision  
ADN v2 is part of something bigger:  
a **self‑protecting blockchain** where nodes cooperate using machine intelligence to keep DigiByte secure against future threats—including quantum computing.

This is only the beginning.
