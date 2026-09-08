# DigiByte ADN v4.0.0 - Active Defense Network

![ADN Tests](https://github.com/DarekDGB/DigiByte-ADN/actions/workflows/tests.yml/badge.svg)
![Coverage 100%](https://img.shields.io/badge/coverage-100%25-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

Author attribution: DarekDGB

Status: controlled pre-release; not released and not tagged.

## Purpose

DigiByte Active Defense Network (ADN) produces local defense decision evidence
for the DigiByte Quantum Shield. Distribution version 4.0.0 includes the
parallel Shield v4 evidence contract and the retained deterministic v3 contract.

The v4 primitives build and verify component verdict evidence. They do not
automatically turn a legacy telemetry handler into a signed v4 endpoint or
establish a deployed cross-repository integration.

## Position in the DigiByte Quantum Shield

| Component | Responsibility in the Shield evidence path |
|---|---|
| Sentinel AI | Threat-signal evidence |
| DQSN | Network-signal evidence and deterministic aggregation |
| ADN | Local defense decision evidence |
| Shield Orchestrator | Verifies component evidence and produces the Shield receipt |
| AdamantineOS | Independently verifies the receipt and applies final fail-closed policy and execution checks |

Raw ADN output is not final execution authority. AdamantineOS consumes Shield
through the Orchestrator receipt. A Shield ALLOW permits further AdamantineOS
checks; it does not approve signing or execution.

ADN cannot sign or broadcast transactions, change DigiByte consensus, hold
wallet keys, override the Orchestrator, or approve AdamantineOS execution.
V4 component-evidence signatures use separately supplied evidence keys;
they do not grant transaction-signing or custody authority.

## Core Mission

ADN evaluates validated local defensive context and produces decision evidence.
The retained v3 contract rejects unknown fields, unsupported versions,
malformed or oversized requests, and invalid numeric values with explicit
fail-closed results. V4 signed payloads bind context, request, decision,
freshness fields, policy, and registry version.

Canonical payloads and contract decisions are deterministic for explicit
inputs. Native key generation and signature bytes need not be deterministic.
Freshness and replay enforcement require the verifier's policy, time, and
replay state; signed fields alone do not provide a global replay store.

Local defense states and recommendations remain evidence or local intent.
They do not become network-wide enforcement or final execution authority.

## Shield v4 Contract and Policy

The parallel implementation is `adn_v3.v4`.

| Identity | Frozen value |
|---|---|
| Component | `adn` |
| Role | `shield_component_adn` |
| Contract | `4` |
| Verdict schema | `shield.verdict.v2` |
| Canonicalization | `shield-v4-canon.v1` |
| Signature policy | `policy.v1` |

Required signatures are `classical-ed25519` and `ml-dsa`, with strict AND
semantics. Optional `fn-dsa` evidence must be last. A verifier rejects
noncanonical order before trust lookup or cryptographic verification.
Present-invalid optional evidence is fatal; valid optional evidence cannot
replace or rescue either required signature.

ML-DSA is formerly CRYSTALS-Dilithium. The OQS adapter uses ML-DSA-65.
FN-DSA is based on Falcon; this repository's Falcon-1024 evidence uses
`fips206-draft-falcon1024-v1`, not a final FIPS 206 profile.

The deterministic TEST-ONLY signature path is a contract fixture mechanism.
The deployment-controlled OQS adapters provide real ML-DSA and Falcon-1024
backend paths. This repository does not supply a production classical Ed25519
backend, HSM integration proof, or FIPS-validated deployment. All required
policy paths must still be satisfied by any real deployment.

## Retained v3 Compatibility

`adn_v3` remains the authoritative implementation of the retained v3 contract.
`adn_v2` remains the legacy behavior and compatibility package. Their runtime
bytes are unchanged by this release-pack alignment.

Public v3 import remains:

```python
from adn_v3 import ADNv3

engine = ADNv3()
# engine.evaluate(request_dict) accepts the retained contract_version 3 schema.
```

The frozen v3 manifest continues to declare `package_version: 3.2.0`,
`contract_version: 3`, and `shield.verdict.v1`. These compatibility identities
do not track the current distribution version. No runtime `__version__`
attribute or server-version surface is introduced by E5.

The retained v3 rules include explicit rejection, stable reason IDs and
evidence families, deterministic context hashing, and Orchestrator-first
handoff. V3 history is not a pending instruction to create or move a v3 tag.

## Repository Layout

| Path | Purpose |
|---|---|
| `src/adn_v3/v4/` | Parallel v4 component evidence, trust, and crypto adapter primitives |
| `src/adn_v3/contracts/` | Retained v3 contracts and frozen manifest |
| `src/adn_v3/core.py` | Retained v3 request boundary |
| `src/adn_v2/` | Legacy behavior and compatibility code |
| `docs/v4/` | Current v4 contract, proof, and candidate release documents |
| `docs/v3/` | Retained v3 normative and historical documents |
| `docs/v2/` | Legacy reference documents |
| `tests/` | Contract, regression, release, and gated native-proof tests |

## Tests and Release Gates

Install and run the standard gate on Python 3.11:

```sh
python -m pip install -e ".[test]"
python -m pytest --cov=adn_v3 --cov-report=term-missing --cov-fail-under=100 -q
```

Coverage is enforced at 100% for `adn_v3`, including `adn_v3.v4`.
It is not a claim of 100% coverage for the legacy `adn_v2` package.

Ordinary tests use deterministic contract fixtures and fake crypto backends.
The two native-OQS modules skip unless their explicit gates are enabled.
Those ordinary skips do not count as native proof.

The dedicated `Shield v4 Real OQS ML-DSA and Falcon-1024 Proof` workflow must
run the exact two locked tests with zero skips, failures, or errors.
Standard CI and dedicated native proof must be green on the final E5 commit,
followed by fresh ZIP verification. Package preparation alone does not close E5
or authorize `v4.0.0`. See the release-status record for remaining gates.

## Documentation

- [V4 contract](docs/v4/CONTRACT.md)
- [V4 manifest](docs/v4/MANIFEST.md)
- [V4 real crypto backend](docs/v4/REAL_CRYPTO_BACKEND.md)
- [V4 test matrix](docs/v4/TEST_MATRIX.md)
- [V4 proof pack](docs/v4/PROOF_PACK.md)
- [V4.0.0 candidate release status](docs/v4/RELEASE_STATUS_v4.0.0.md)
- [Retained v3 index](docs/v3/INDEX.md)
- [Retained v3 manifest](docs/v3/MANIFEST.md)
- [V3 reason IDs](docs/v3/REASON_IDS.md)
- [V3 evidence families](docs/v3/EVIDENCE_FAMILIES.md)
- [V3 test matrix](docs/v3/TEST_MATRIX.md)
- [Historical v3 proof pack](docs/v3/PROOF_PACK.md)
- [Security policy](SECURITY.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## Contribution Policy

See [CONTRIBUTING.md](CONTRIBUTING.md). Preserve deterministic contracts,
fail-closed behavior, frozen compatibility identities, and the 100% coverage
gate. Evidence signing must remain distinct from transaction signing.
First-party author attribution is DarekDGB only.

## License

MIT License. Copyright (c) 2025 DarekDGB.
