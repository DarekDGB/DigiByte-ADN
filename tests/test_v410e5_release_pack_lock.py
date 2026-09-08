from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import tomllib
import unicodedata
from pathlib import Path

import pytest

import adn_v2
import adn_v3
from adn_v3.contracts import v3_2_lock
from adn_v3.v4 import (
    CANONICALIZATION_PROFILE, COMPONENT_ID, COMPONENT_ROLE, CONTRACT_VERSION,
    KEY_REGISTRY_SCHEMA_VERSION, POLICY_VERSION, SIGNATURE_BUNDLE_SCHEMA_VERSION,
    VERDICT_SCHEMA_VERSION,
)
from adn_v3.v4.trust_profile import (
    ALGORITHM_STANDARD_PROFILES, OPTIONAL_ALGORITHMS, REQUIRED_ALGORITHMS,
    SUPPORTED_ALGORITHMS,
)

ROOT = Path(__file__).resolve().parents[1]
V4_DOCS = tuple('docs/v4/' + name for name in (
    'CONTRACT.md', 'MANIFEST.md', 'REAL_CRYPTO_BACKEND.md', 'TEST_MATRIX.md',
    'PROOF_PACK.md', 'RELEASE_STATUS_v4.0.0.md',
))
PACK_FILES = (
    'pyproject.toml', 'README.md', 'CHANGELOG.md', 'SECURITY.md', 'CONTRIBUTING.md',
    'docs/v3/PROOF_PACK.md', 'docs/v3/REASON_IDS.md', 'docs/v3/RELEASE_STATUS_v3.2.0.md',
    'tests/test_v410e5_release_pack_lock.py',
) + V4_DOCS
KATS = {
    'tests/fixtures/v4/component_verdict_policy_v1_kat.json':
        '176d9d8f7d16be456f2bf783c3031b65c46fd5f9efed1aba89d216b98406b0ff',
    'tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json':
        'b799b963cb46ccf579a0380cffeecd81f99fa616267e6d69fec4f2bf06e9f6ef',
}
REAL_NODES = (
    'tests/test_v48g_real_oqs_mldsa_backend.py::'
    'test_v48g_real_oqs_mldsa65_adn_backend_round_trip_and_negatives',
    'tests/test_v48h_e_real_oqs_falcon_backend.py::'
    'test_v48h_e_real_oqs_falcon1024_backend_round_trip_and_negatives',
)
GENERATED_DIRS = frozenset({
    '.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    '.tox', '.venv', 'venv', 'build', 'dist', 'htmlcov',
})


def _text(name: str) -> str:
    return (ROOT / name).read_text(encoding='utf-8', errors='strict')


def _generated(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return (
        any(part in GENERATED_DIRS or part.endswith(('.egg-info', '.dist-info'))
            for part in relative.parts)
        or path.suffix in {'.pyc', '.pyo'}
        or path.name in {'.coverage', 'coverage.xml', 'shield-v4-real-oqs-results.xml'}
        or path.name.startswith('.coverage.')
    )


def _source_files(root: Path) -> list[Path]:
    if (root / '.git').exists():
        output = subprocess.run(
            ['git', '-C', str(root), 'ls-files', '-z'], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.decode('utf-8', errors='strict')
        paths = [root / name for name in output.split('\0') if name]
        assert all(path.is_file() and not path.is_symlink() for path in paths)
        assert not any(_generated(path, root) for path in paths), 'tracked generated artifact'
        return sorted(paths)
    return sorted(path for path in root.rglob('*')
                  if path.is_file() and not _generated(path, root))


def _check_text(raw: bytes) -> str:
    assert not raw or raw.endswith(b'\n'), 'missing terminal LF'
    assert b'\r' not in raw and b'\x00' not in raw, 'CR or NUL'
    assert not raw.startswith(bytes((0xEF, 0xBB, 0xBF))), 'UTF-8 BOM'
    text = raw.decode('utf-8', errors='strict')
    assert unicodedata.normalize('NFC', text) == text, 'non-NFC text'
    assert '\ufffd' not in text, 'replacement character'
    assert not any(0x80 <= ord(c) <= 0x9F for c in text), 'C1 control'
    markers = ('\u00c2', '\u00c3', '\u00e2\u20ac', '\u00e2\u0153',
               '\u00ef\u00bb\u00bf', '\u00f0\u0178')
    assert not any(marker in text for marker in markers), 'mojibake'
    return text


def _check_attribution(text: str) -> None:
    lines = [re.sub(r'[*`#]', '', line).strip() for line in text.splitlines()]
    for index, line in enumerate(lines):
        match = re.match(
            r'(?i)^(?:author(?:s| attribution)?|maintainer|created by|written by):\s*(.+)$', line
        )
        if match:
            assert match.group(1).lstrip('@') == 'DarekDGB', 'non-canonical attribution'
        if line.lower() in {'author', 'author attribution', 'maintainer'}:
            following = next((value for value in lines[index + 1:] if value), '')
            assert following.lstrip('@') == 'DarekDGB', 'non-canonical attribution'


def _scan(root: Path) -> list[Path]:
    paths = _source_files(root)
    for path in paths:
        try:
            _check_attribution(_check_text(path.read_bytes()))
        except (AssertionError, UnicodeError) as exc:
            raise AssertionError(f'{path.relative_to(root)}: {exc}') from exc
    return paths


def test_v410e5_distribution_preserves_frozen_compatibility_identity() -> None:
    project = tomllib.loads(_text('pyproject.toml'))['project']
    assert project['name'] == 'digibyte-adn' and project['version'] == '4.0.0'
    assert project['authors'] == [{'name': 'DarekDGB'}]
    assert project['description'] == 'DigiByte Active Defense Network (ADN) - deterministic Shield v4 defense decision evidence component.'
    assert v3_2_lock.PACKAGE_VERSION == v3_2_lock.build_manifest()['package_version'] == '3.2.0'
    assert v3_2_lock.CONTRACT_VERSION == 3
    assert not hasattr(adn_v2, '__version__') and not hasattr(adn_v3, '__version__')
    assert 'Existing v3/legacy handlers' in _text('docs/v4/PROOF_PACK.md')


def test_v410e5_protocol_and_algorithm_identities_remain_frozen() -> None:
    assert (COMPONENT_ID, COMPONENT_ROLE, CONTRACT_VERSION) == ('adn', 'shield_component_adn', 4)
    assert (VERDICT_SCHEMA_VERSION, CANONICALIZATION_PROFILE, POLICY_VERSION) == (
        'shield.verdict.v2', 'shield-v4-canon.v1', 'policy.v1')
    assert (SIGNATURE_BUNDLE_SCHEMA_VERSION, KEY_REGISTRY_SCHEMA_VERSION) == (
        'shield.signature_bundle.v1', 'shield.key_registry.v1')
    assert REQUIRED_ALGORITHMS == ('classical-ed25519', 'ml-dsa')
    assert OPTIONAL_ALGORITHMS == ('fn-dsa',)
    assert SUPPORTED_ALGORITHMS == REQUIRED_ALGORITHMS + OPTIONAL_ALGORITHMS
    assert ALGORITHM_STANDARD_PROFILES == {
        'classical-ed25519': ('rfc8032-ed25519-v1',),
        'ml-dsa': ('fips204-ml-dsa-65-v1',),
        'fn-dsa': ('fips206-draft-falcon1024-v1',),
    }


def test_v410e5_fixture_hashes_and_payload_hash_are_distinct_and_exact() -> None:
    for name, digest in KATS.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
        for doc in ('docs/v4/PROOF_PACK.md', 'docs/v4/MANIFEST.md'):
            assert name in _text(doc) and digest in _text(doc)
    kat = json.loads(_text(next(iter(KATS))))
    assert kat['signed_payload_hash'] in _text('docs/v4/PROOF_PACK.md')


def test_v410e5_release_document_links_and_proof_test_paths_resolve() -> None:
    for name in V4_DOCS:
        assert name in _text('README.md')
    for name in PACK_FILES:
        for link in re.findall(r'\]\(([^)]+)\)', _text(name)):
            if '://' not in link and not link.startswith('#'):
                assert (ROOT / name).parent.joinpath(link.split('#', 1)[0]).exists(), (name, link)
    for name in re.findall(r'`(tests/[^`]+\.py)`', _text('docs/v4/PROOF_PACK.md')):
        assert (ROOT / name).is_file(), name


def test_v410e5_release_status_is_candidate_only() -> None:
    status = _text('docs/v4/RELEASE_STATUS_v4.0.0.md')
    for key, value in {
        'Author attribution': 'DarekDGB', 'Status': 'CONTROLLED PRE-RELEASE',
        'Release decision': 'NOT YET AUTHORIZED', 'Distribution version': '4.0.0',
        'Candidate tag': 'v4.0.0', 'Tag created': 'no',
    }.items():
        assert re.findall(rf'^{re.escape(key)}: (.+)$', status, re.MULTILINE) == [value]
    assert 'Do not create or move `v4.0.0`' in status
    assert 'controlled pre-release; not released and not tagged' in _text('README.md')


def test_v410e5_v3_history_is_scoped_and_has_no_pending_tag_instruction() -> None:
    for name in ('README.md', 'SECURITY.md', 'docs/v3/PROOF_PACK.md',
                 'docs/v3/REASON_IDS.md', 'docs/v3/RELEASE_STATUS_v3.2.0.md'):
        text = re.sub(r'[*`]', '', _text(name))
        for pattern in (r'do not tag v3\.2\.0', r'no v3\.2\.0 tag is allowed',
                        r'ready for the v3\.2\.0.*only after', r'before v3\.2\.0 tagging'):
            assert re.search(pattern, text, re.IGNORECASE | re.DOTALL) is None
    status = _text('docs/v3/RELEASE_STATUS_v3.2.0.md')
    assert 'not an independent v4 audit' in status
    assert 'not a claim\nabout its current version' in status


def test_v410e5_native_workflow_keeps_exact_two_node_guard() -> None:
    workflow = _text('.github/workflows/shield-v4-real-oqs.yml')
    assert tuple(re.findall(r'--require-testcase "([^"]+)"', workflow)) == REAL_NODES
    assert '--min-tests 2' in workflow
    for flag in ('SHIELD_V4_REAL_OQS', 'SHIELD_V4_REAL_OQS_FALCON'):
        assert f'{flag}: "1"' in workflow
    for node in REAL_NODES:
        name, function = node.split('::')
        assert name in workflow
        assert function in {item.name for item in ast.parse(_text(name)).body if isinstance(item, ast.FunctionDef)}
        assert node in _text('docs/v4/PROOF_PACK.md')
    standard = _text('.github/workflows/tests.yml')
    assert 'python-version: "3.11"' in standard
    assert '--cov=adn_v3' in standard and '--cov-fail-under=100' in standard


def test_v410e5_proof_bounds_crypto_authority_and_coverage_claims() -> None:
    proof = ' '.join(_text('docs/v4/PROOF_PACK.md').split())
    for phrase in ('cannot sign or broadcast transactions', 'wallet keys',
                   'AdamantineOS remains the final fail-closed policy and execution boundary',
                   'cannot replace or rescue', 'not final FIPS 206 proof',
                   'does not supply a production classical Ed25519 backend',
                   'signature bytes need not be deterministic',
                   'does not claim complete legacy `adn_v2` coverage',
                   'Historical native runs and local skipped tests cannot close that future gate'):
        assert phrase in proof


def test_v410e5_repository_text_attribution_and_ascii_pack() -> None:
    paths = _scan(ROOT)
    assert len(paths) >= 100
    assert set(PACK_FILES).issubset(path.relative_to(ROOT).as_posix() for path in paths)
    for name in PACK_FILES:
        assert (ROOT / name).read_bytes().isascii(), name


def test_v410e5_hygiene_rejects_corruption_and_tracks_source_not_runtime_output(tmp_path) -> None:
    source = tmp_path / 'source.md'
    valid = 'Author: DarekDGB\nCaf\u00e9 \u2014 \u2011 \u2705\n'
    source.write_text(valid, encoding='utf-8')
    for name in ('.coverage', '.coverage.worker.1', 'src/__pycache__/module.pyc',
                 '.pytest_cache/cache.bin', 'src/package.egg-info/SOURCES.txt'):
        output = tmp_path / name
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b'\xff\x00')
    assert _scan(tmp_path) == [source]
    mutations = [chr(codepoint) + '\n' for codepoint in range(0x80, 0xA0)]
    mutations += [chr(codepoint).encode('utf-8').decode(codec, errors='replace') + '\n'
                  for codepoint in (0x00E9, 0x2014, 0x2011, 0x2705, 0x1F680, 0xFEFF)
                  for codec in ('latin-1', 'cp1252')]
    mutations += ['\ufffd\n', 'e\u0301\n', 'bad\x00\n', 'bad\r\n', '\ufeffbad\n']
    damaged_bytes = [value.encode('utf-8') for value in mutations]
    damaged_bytes += [b'\xff\n', b'missing terminal LF']
    for raw in damaged_bytes:
        source.write_bytes(raw)
        with pytest.raises(AssertionError):
            _scan(tmp_path)
    source.write_text('Author: ' + 'Wrong' + 'Author\n', encoding='ascii')
    with pytest.raises(AssertionError, match='non-canonical attribution'):
        _scan(tmp_path)
    source.write_text(valid, encoding='utf-8')
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    subprocess.run(['git', '-C', str(tmp_path), 'add', 'source.md'], check=True)
    assert _scan(tmp_path) == [source]
    subprocess.run(['git', '-C', str(tmp_path), 'add', '.coverage'], check=True)
    with pytest.raises(AssertionError, match='tracked generated artifact'):
        _scan(tmp_path)
