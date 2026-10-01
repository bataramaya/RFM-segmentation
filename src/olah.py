from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from rfm import load, build_rfm, add_scores, add_segments

df = load(ROOT / "data" / "rfm_data.csv")     # ← satu baris yang berubah
r  = add_segments(add_scores(build_rfm(df)))

print(f"{len(df)} rows -> {len(r)} customers\n")   # rekonsiliasi, tercetak
print(r['segment'].value_counts())
print()
print(r.groupby('segment')[['recency', 'frequency', 'monetary']].mean().round(2))
