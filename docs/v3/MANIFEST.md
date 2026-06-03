# DigiByte Active Defense Network — Shield v3.2.0 Manifest

Author attribution: DarekDGB

## Component Identity

- `component_id`: `adn`
- `contract_version`: `3`
- `package_version`: `3.2.0`
- `output_schema_version`: `shield.verdict.v1`

## Supported Decisions

- `ALLOW`
- `ESCALATE`
- `DENY`
- `ERROR`
- `SKIPPED`

## Reason ID Registry

- `ADN_OK_COORDINATION_ALLOW`
- `ADN_ESCALATE_POLICY_REVIEW`
- `ADN_DENY_DEFENSE_TRIGGERED`
- `ADN_ERROR_INVALID_VERDICT`
- `ADN_ERROR_CONTEXT_HASH_MISMATCH`

## Evidence Family Registry

- `defense_signal`
- `policy_context`
- `coordination_state`

## Authority Boundary

This component is evidence-only. It does not sign, broadcast, hold keys, expand authority, override the Orchestrator, or approve AdamantineOS execution directly.

## Orchestrator Role

The component verdict is input evidence only. Final Shield outcome must be produced by the Shield Orchestrator deterministic receipt.

## AdamantineOS Visibility

AdamantineOS must not consume this component directly. AdamantineOS consumes Shield only through one deterministic Orchestrator receipt.
