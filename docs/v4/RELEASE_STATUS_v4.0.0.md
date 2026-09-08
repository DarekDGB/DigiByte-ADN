# DigiByte ADN - Shield v4.0.0 Candidate Release Status

Author attribution: DarekDGB
Status: CONTROLLED PRE-RELEASE
Release decision: NOT YET AUTHORIZED
Distribution version: 4.0.0
Candidate tag: v4.0.0
Tag created: no

## Scope

V4.10-E5 aligns ADN package metadata and release documentation with its existing
parallel v4 evidence implementation. It adds a proof pack and release lock.
Runtime, workflow, protocol, schema, trust-profile, and fixture bytes remain
unchanged. No new runtime version attribute or signed v4 endpoint is added.

The retained v3 manifest remains package_version 3.2.0 and contract_version 3.
The legacy adn_v2 package remains compatibility behavior, not the current v4
evidence contract. Coverage remains 100% for adn_v3, including its v4 subpackage.

## Remaining Gates

- External review of the prepared copy-only E5 package.
- DarekDGB commits the complete package to DigiByte-ADN.
- Standard Python 3.11 CI passes on the exact E5 commit at 100% coverage.
- Dedicated native-OQS proof passes on that same commit with exactly the two
  locked nodes, zero skips, zero failures, zero errors, and the JUnit guard green.
- A fresh post-commit ZIP matches the approved candidate and required evidence.
- Later ecosystem release gates and an explicit release decision are complete.

Package preparation and local tests do not close the post-commit gate. The two
ordinary native-module skips are not native proof. Exact commands, node names,
frozen fixture hashes, and claim limits are in [PROOF_PACK.md](PROOF_PACK.md).

## Authority and Cryptographic Limits

ADN evidence reaches AdamantineOS through the Shield Orchestrator receipt.
ADN cannot sign or broadcast transactions, change consensus, hold wallet keys,
or grant final execution approval. Evidence keys remain separate.

Classical Ed25519 and ML-DSA are required; optional FN-DSA cannot replace or
rescue either path. Present-invalid optional evidence is fatal. Falcon-1024
uses the frozen draft profile and is not final FIPS 206 proof. A production
classical Ed25519 backend, HSM integration proof, and a FIPS-validated deployment
are not supplied by this repository.

Do not create or move `v4.0.0` without DarekDGB's explicit release authorization.
This record does not authorize tags in any other repository.
