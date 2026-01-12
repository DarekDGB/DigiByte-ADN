# 🔐 ADN — Shield Contract v3
**Component:** ADN (Active Defence Network)  
**Contract Version:** 3  
**Authoritative Package:** `adn_v3`

This document is **normative** for ADN v3 contract behavior.

---

## Public API

```python
from adn_v3 import ADNv3
v3 = ADNv3()
response = v3.evaluate(request_dict)
```

---

## Request schema

Allowed top-level keys:
- contract_version (must be 3)
- component ("adn")
- request_id
- events

Unknown keys fail closed.

---

## Fail-closed guarantees

Any invalid request returns:
- decision = ERROR
- meta.fail_closed = True
- explicit reason_codes

---
**Author:** DarekDGB
