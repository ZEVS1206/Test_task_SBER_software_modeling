#!/usr/bin/env python3

import re
import csv
from pathlib import Path

RESULTS_DIR = Path("./results")
OUTPUT_CSV = "hit_rates.csv"

pattern_l2 = re.compile(r"cpu0->cpu0_L2C TOTAL\s+ACCESS:\s+(\d+)\s+HIT:\s+(\d+)\s+MISS:\s+\d+\s+MSHR_MERGE:\s+\d+")
pattern_name = re.compile(r"champsim_(\w+)_(\w+(?:_\w+)?)_(\d+)_(\d+)_(.+)\.log")

rows = []
for log_file in RESULTS_DIR.glob("*.log"):
    text = log_file.read_text()
    match_l2 = pattern_l2.search(text)
    if not match_l2:
        print(f"No L2C stats in {log_file.name}")
        continue
    access = int(match_l2.group(1))
    hit = int(match_l2.group(2))
    hit_rate = hit / access if access > 0 else 0

    match_name = pattern_name.match(log_file.name)
    if not match_name:
        print(f"Filename pattern mismatch: {log_file.name}")
        continue

    replacement = match_name.group(1)
    prefetcher = match_name.group(2)
    sets = match_name.group(3)
    ways = match_name.group(4)
    trace = match_name.group(5)

    rows.append([replacement, prefetcher, sets, ways, trace, hit_rate])
    print(f"Processed: {log_file.name} -> hit_rate={hit_rate:.4f}")

with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["replacement", "prefetcher", "sets", "ways", "trace", "hit_rate"])
    writer.writerows(rows)

print(f"Saved {len(rows)} entries to {OUTPUT_CSV}")
