# DigiByte ADN - Shield v4.0.0 Candidate Proof Pack

Author attribution: DarekDGB

## Status and Scope

Distribution version: 4.0.0. This is a controlled pre-release candidate,
not a released or tagged artifact. V4.10-E5 aligns release documentation and
metadata; every runtime, workflow, schema, trust-profile, and fixture byte is
preserved. [Release status](RELEASE_STATUS_v4.0.0.md) records the remaining gates.

ADN's parallel v4 evidence surface is `adn_v3.v4`. The retained `adn_v3` request
contract remains version 3; its manifest package_version remains 3.2.0.
Legacy `adn_v2` behavior and imports remain unchanged. No runtime __version__
attribute or server-version surface is introduced. Existing v3/legacy handlers
do not become signed v4 endpoints through a distribution-version change.

## Frozen Identity and Policy

| Item | Value |
|---|---|
| Component ID | `adn` |
| Component role | `shield_component_adn` |
| Contract version | `4` |
| Verdict schema | `shield.verdict.v2` |
| Canonicalization profile | `shield-v4-canon.v1` |
| Signature policy | `policy.v1` |
| Signature-bundle schema | `shield.signature_bundle.v1` |
| Key-registry schema | `shield.key_registry.v1` |

Required order is classical-ed25519, then ml-dsa, then fn-dsa only if present.
Both required algorithms must verify. Optional FN-DSA cannot replace or rescue
either required signature; present-invalid optional evidence is fatal.
Verifier structural preflight and canonical-order validation occur before any
trust lookup or cryptographic verification. Received bundles are not sorted
or repaired by the verifier.

| Algorithm | Profile | Backend evidence |
|---|---|---|
| `classical-ed25519` | `rfc8032-ed25519-v1` | Required policy path; deterministic contract tests |
| `ml-dsa` | `fips204-ml-dsa-65-v1` | OQS ML-DSA-65 adapter and gated native proof |
| `fn-dsa` | `fips206-draft-falcon1024-v1` | Optional draft Falcon-1024 adapter and gated native proof |

ML-DSA is formerly CRYSTALS-Dilithium. FN-DSA is based on Falcon.
The draft Falcon profile is not final FIPS 206 proof.

## Test Mapping

| Claim | Existing evidence |
|---|---|
| V3 manifest and registries remain frozen | `tests/test_v3_2_manifest_verdict_lock.py` |
| V3 fail-closed request boundary and legacy parity | `tests/test_contract_v3_fail_closed.py`, `tests/test_v2_v3_no_drift.py` |
| V4 payload schema, authority metadata, and deterministic hash | `tests/test_v4_crypto_verdict_contract.py` |
| Missing required evidence and tampering reject | `tests/test_v4_missing_signature_fail_closed.py`, `tests/test_v4_signature_tamper_fail_closed.py` |
| Context binding | `tests/test_v4_context_hash_signature_binding.py` |
| Frozen component KAT | `tests/test_v4_component_kat_vectors.py` |
| Authenticated draft FN-DSA message KAT | `tests/test_v48h_fn_dsa_signed_message_kat.py` |
| Optional evidence, canonical order, no rescue, preflight | `tests/test_v48h_fn_dsa_optional_evidence.py` |
| Real-adapter parsing, policy, errors, and no TEST-ONLY fallback | `tests/test_v4_real_crypto_backend_contract.py` |
| ML-DSA fake-backend boundary | `tests/test_v4_oqs_mldsa_backend.py` |
| Falcon-1024 fake-backend boundary | `tests/test_v48h_e_oqs_falcon_backend.py` |
| Exact native JUnit guard behavior | `tests/test_v48h_e_real_oqs_junit_guard.py` |
| Candidate release truth, identity, links, and transfer hygiene | `tests/test_v410e5_release_pack_lock.py` |

## Frozen Fixture Hashes

The following are complete-file SHA-256 values:

```text
176d9d8f7d16be456f2bf783c3031b65c46fd5f9efed1aba89d216b98406b0ff  tests/fixtures/v4/component_verdict_policy_v1_kat.json
b799b963cb46ccf579a0380cffeecd81f99fa616267e6d69fec4f2bf06e9f6ef  tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json
```

The shared component KAT's signed_payload_hash is separately:

```text
a3881f27444ce73de875a15c8b413785a4fec4f4c03baaa6f8ee2fbf839736ae
```

These fixtures are TEST-ONLY canonicalization and message-binding evidence,
not production keys or native cryptographic execution evidence.

## Standard and Native Gates

Standard workflow: `tests`, Python 3.11, full suite and 100% `adn_v3` coverage:

```sh
python -m pip install -e ".[test]"
python -m pytest --cov=adn_v3 --cov-report=term-missing --cov-fail-under=100 -q
```

Coverage includes `adn_v3.v4`; it does not claim complete legacy `adn_v2` coverage.
Ordinary runs skip the two gated native modules when their environment flags
are absent. Those skips are not native proof.

Dedicated workflow: `Shield v4 Real OQS ML-DSA and Falcon-1024 Proof`.
The exact two required testcase identities are:

```text
tests/test_v48g_real_oqs_mldsa_backend.py::test_v48g_real_oqs_mldsa65_adn_backend_round_trip_and_negatives
tests/test_v48h_e_real_oqs_falcon_backend.py::test_v48h_e_real_oqs_falcon1024_backend_round_trip_and_negatives
```

The workflow must enable both SHIELD_V4_REAL_OQS=1 and
SHIELD_V4_REAL_OQS_FALCON=1. The existing guard requires --min-tests 2 and both
--require-testcase identities; release evidence must show tests=2, skipped=0,
failures=0, errors=0, required=2. See [the test matrix](TEST_MATRIX.md) for commands.
These tests exercise real adapter round trips, signature tampering and cross-key
rejection; ML-DSA also checks wrong-length key rejection. They do not prove an
end-to-end production classical-plus-PQC deployment or HSM integration.

Preparation results are recorded in the controlled roadmap. Both workflows
must pass on the actual post-upload E5 commit, followed by fresh ZIP verification.
Historical native runs and local skipped tests cannot close that future gate.

## Authority and Remaining Limits

ADN cannot sign or broadcast transactions, change DigiByte consensus, hold
wallet keys, or approve AdamantineOS execution. V4 cryptography signs component
evidence with separately supplied evidence keys. Orchestrator-first handoff
remains mandatory. AdamantineOS remains the final fail-closed policy and execution
boundary and independently applies its own receipt policy and replay checks.

Canonical decisions and payloads are deterministic for explicit inputs; native
key generation and signature bytes need not be deterministic. Freshness fields
are signed evidence, not an independently implemented global replay store.

This repository does not supply a production classical Ed25519 backend,
HSM integration proof, or a FIPS-validated deployment. The neutral interface
and example resolver references do not establish those capabilities. Real
deployments must supply all required policy paths without fallback to TEST-ONLY
material. The FN-DSA profile remains draft Falcon-1024 evidence.

E5 creates no release tag and does not grant release authorization. The current
roadmap controls the later ecosystem proof and final release decision.
