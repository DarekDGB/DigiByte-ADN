# Changelog

## v3.2.0 — Manifest / Verdict / Receipt Lock

- Added Shield v3.2.0 manifest documentation under `docs/v3/`.
- Added reason ID and evidence family registries.
- Added canonical component verdict lock and validation code with negative-first fail-closed tests.
- Preserved 100% coverage gate.
- Locked AdamantineOS boundary language: Shield is consumed only through the deterministic Orchestrator receipt.

## v3.1.0

Shield v3.1.0 hardening release for DigiByte ADN / Active Defense Network.

- Corrects ADN naming to **Active Defense Network**.
- Updates package metadata to `3.1.0`.
- Preserves the stable Shield Contract v3 surface.
- Confirms `adn_v3` remains fully regression-locked at 100% coverage.
- Confirms 39 tests passing with 172 statements covered and 0 missed statements.
- Maintains deterministic, fail-closed, local-only defense decision behavior.
- Adds no consensus authority, signing authority, transaction broadcast authority, or hidden execution authority.

## v3.0.0

- Stabilises ADN v3 package metadata and CI.
- Locks ADN v3 contract coverage at 100%.
- Adds v3 full coverage lock tests for defensive fail-closed branches.
- Adds packaged typing markers for ADN packages.
