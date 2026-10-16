#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""SHA256 verification for locally sourced original research inputs; no network needed."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
expected=json.loads((root/'audit'/'original_source_hashes.json').read_text())
p=argparse.ArgumentParser();p.add_argument('--input-dir',type=Path,default=root/'private_inputs')
a=p.parse_args();good=True
for filename,want in expected.items():
 f=a.input_dir/filename
 if not f.exists():print('MISSING:',f);good=False;continue
 got=hashlib.sha256(f.read_bytes()).hexdigest()
 ok=got==want
 print(('PASS' if ok else 'FAIL')+': '+filename+'; SHA256='+got)
 good &= ok
if not good:raise SystemExit(1)

