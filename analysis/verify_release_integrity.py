#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Validate repository file byte hashes against the audit manifest."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'audit/REPOSITORY_FILES_SHA256.json'
d=json.loads(manifest.read_text(encoding='utf-8'))
assert d['manifest_excludes_self'] is True
for rel,expected in d['sha256_by_relative_path'].items():
    p=ROOT/rel
    assert p.is_file(),f'Missing file: {rel}'
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual==expected,f'Hash mismatch: {rel}'
print(f"PASS: {len(d['sha256_by_relative_path'])} repository files verified (excluding manifest itself)")

