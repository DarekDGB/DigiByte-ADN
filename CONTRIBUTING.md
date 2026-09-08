# Contributing to DigiByte ADN - Active Defense Network

Author attribution: DarekDGB

Distribution 4.0.0 is a controlled pre-release candidate. Current Shield v4
evidence primitives live in `adn_v3.v4`; the retained v3 contract remains in
`adn_v3`, with legacy behavior and compatibility under `adn_v2`.

## Welcome Contributions

- Contract and documentation corrections grounded in executable behavior.
- Deterministic defensive decision logic and explicit fail-closed errors.
- Negative tests for malformed evidence, policy failures, and authority bypasses.
- Reviewed improvements to backend adapters, performance, and integration examples.
- Clear descriptions of limitations and reproducible proof commands.

ADN provides local defensive evidence. Cross-repository deployment wiring,
transaction execution, and broader protection claims require their own
implementation and proof; documentation must not imply they already exist.

## Required Boundaries

- Do not change DigiByte consensus, block validity, or fork choice.
- Do not sign or broadcast transactions, take wallet-key custody, or grant
  direct AdamantineOS execution approval.
- V4 signatures prove component evidence only, with separate evidence keys.
- Preserve Orchestrator-first receipt handoff. AdamantineOS remains the final
  fail-closed policy and execution boundary.
- Keep required classical Ed25519 and ML-DSA paths under strict AND semantics.
- Optional draft Falcon-1024 evidence stays last and cannot replace or rescue
  a failed or missing required signature. Present-invalid evidence is fatal.
- Do not reinterpret draft Falcon signatures as final FIPS 206 signatures.
- Do not fall back from real backend mode to deterministic TEST-ONLY signatures.

## Compatibility and Determinism

Preserve the frozen v3 manifest at package_version 3.2.0 and contract_version 3.
The distribution version is a separate surface. Do not rename legacy imports
or change frozen v4 schema, domain, policy, profile, role, or KAT bytes as part
of a release-document alignment.

Canonical payloads and contract decisions must be reproducible for explicit
inputs. Native key generation and signature bytes are not required to be
deterministic. Keep environmental behavior outside the deterministic contract.

## Pull Request Expectations

Explain the problem, the resulting behavior, the exact file scope, and the
evidence for each security claim. Read existing documents before editing,
preserve relevant history, and update tests when contract behavior changes.

Run the standard Python 3.11 gate:

```sh
python -m pip install -e ".[test]"
python -m pytest --cov=adn_v3 --cov-report=term-missing --cov-fail-under=100 -q
```

The 100% coverage boundary is `adn_v3`, including the v4 subpackage.
Legacy `adn_v2` is packaged but is not included in that coverage claim.

For release proof, also require the dedicated native-OQS workflow's two exact
nodes with zero skips, failures, or errors on the same commit. Ordinary
native-module skips are expected without liboqs and are not native proof.
See [the proof pack](docs/v4/PROOF_PACK.md) for the exact gate.

Use ASCII-safe release-pack files, strict UTF-8/NFC/LF repository text, and
escaped Unicode in new test probes. Do not include generated caches, bytecode,
coverage databases, build metadata, or native library checkouts in copy packages.
First-party author attribution is DarekDGB only; preserve third-party notices.

DarekDGB reviews architecture and release scope. A prepared package or green
local run does not authorize a release tag. The controlled roadmap requires
same-commit CI, native proof, fresh ZIP verification, and a release decision.

## License

Contributions use the repository's MIT License.
Copyright (c) 2025 DarekDGB.
