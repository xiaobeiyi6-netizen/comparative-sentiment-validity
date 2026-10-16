#!/usr/bin/env python3
"""Flag known restricted inputs, unsafe review CSV schemas and likely secrets.

This static check does not establish data-use rights, ethics approval or
universal absence of sensitive information. Run from any current directory.
"""
from pathlib import Path
import csv
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SAFE = ROOT / "reviewer_safe" / "aggregate_results"
restricted = {"tweets.csv", "gop_rel_only.csv", "airline_predictions.csv",
              "gop_external_validation_results.zip", ".env", "id_rsa",
              "id_ed25519", "credentials.json", "secrets.json"}
private_dirs = {"private_inputs", "private_data", "raw_tweets", "identifiable_records"}
result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                        check=True, capture_output=True)
paths = [Path(b.decode("utf-8")) for b in result.stdout.split(b"\0") if b]
assert paths, "No tracked files found"
for rel in paths:
    parts = {p.lower() for p in rel.parts}
    assert rel.name.lower() not in restricted, f"Potential restricted file: {rel}"
    assert not parts.intersection(private_dirs), f"Potential private input path: {rel}"
    assert rel.suffix.lower() not in {".pem", ".p12", ".key"}, f"Key file: {rel}"

expected = {
 "S3_group_confusion_aggregates.csv": (32, {
   "corpus","group","model","n","TP","FN","FP","TN",
   "reference_negative_pct","predicted_negative_pct","FNR_pct",
   "FPR_pct","bias_pp","FP_component_pp","FN_component_pp"}),
 "S4_strong_gap_reversals.csv": (8, {
   "corpus","model","group_a","group_b","ref_diff_pp","pred_diff_pp",
   "gap_pp","FP_difference_pp","FN_difference_pp","bias_diff_pp"}),
}
for filename, (count, columns) in expected.items():
    with (SAFE / filename).open(encoding="utf-8-sig",newline="") as f:
        rows = csv.DictReader(f)
        assert set(rows.fieldnames or []) == columns, f"Unexpected fields: {filename}"
        assert sum(1 for row in rows) == count, f"Unexpected rows: {filename}"

patterns = [r"ghp_[A-Za-z0-9]{36}", r"github_pat_[A-Za-z0-9_]{40,}",
            r"sk-[A-Za-z0-9]{32}",
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]
for rel in paths:
    if not (rel.parts and rel.parts[0] == "reviewer_safe"):
        continue
    if rel.suffix.lower() not in {".py",".md",".csv",".txt",".json"}:
        continue
    body = (ROOT/rel).read_text(encoding="utf-8")
    for pat in patterns:
        assert not re.search(pat,body), f"Possible credential: {rel}"

print(f"PASS: {len(paths)} tracked paths checked for restricted filenames")
print("PASS: S3/S4 contain expected aggregate-only schema and row counts")
print("PASS: No recognizable API-token patterns in reviewer_safe files")
print("LIMIT: Human review of licensing, privacy and ethics remains necessary")
