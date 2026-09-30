#!/bin/bash
source /data/yingda/software/miniconda3/etc/profile.d/conda.sh
conda activate kwallet
cd /data/yingda/Kwallet-Rl
LOG=runs/sw_finalize.log
echo "watch_sw start $(date)" > $LOG
# wait until no shard processes remain (this script's name does not match them)
while [ "$(pgrep -f 'scripts/run_switching' | wc -l)" -gt 0 ]; do sleep 45; done
echo "all switching shards finished $(date)" >> $LOG
python - <<'PY' >> $LOG 2>&1
import pandas as pd, glob
from pathlib import Path
root=Path("runs/switching"); root.mkdir(exist_ok=True)
frames=[pd.read_csv(f) for f in sorted(glob.glob("runs/sw_*/switch_summary.csv"))]
df=pd.concat(frames, ignore_index=True)
# rules are identical across shards -> keep one copy; keep all learned rows
rules=df[df.kind=="rule"].drop_duplicates(subset=["policy","a","b","frac"])
learned=df[df.kind=="learned"]
out=pd.concat([rules,learned], ignore_index=True)
out.to_csv(root/"switch_summary.csv", index=False)
learned.to_csv(root/"switch_learned.csv", index=False)
rules.to_csv(root/"switch_rules.csv", index=False)
print("merged rows:",len(out),"| rules:",len(rules),"| learned:",len(learned))
print(out.groupby(["kind","policy"]).size())
PY
echo "rc-merge=$?" >> $LOG
python scripts/make_paper_assets.py --exp matrix_main --ablation matrix_ablation --kscale kscale >> $LOG 2>&1
echo "rc-assets=$?" >> $LOG
cd paper/icassp2027
pdflatex -interaction=nonstopmode main.tex >>../../$LOG 2>&1
bibtex main >>../../$LOG 2>&1
pdflatex -interaction=nonstopmode main.tex >>../../$LOG 2>&1
pdflatex -interaction=nonstopmode main.tex >>../../$LOG 2>&1
cd /data/yingda/Kwallet-Rl
echo "pdf-pages: $(pdfinfo paper/icassp2027/main.pdf 2>/dev/null | grep Pages)" >> $LOG
echo "overfull: $(grep -c Overfull paper/icassp2027/build.log 2>/dev/null)" >> $LOG
mkdir -p paper/icassp2027/render
pdftoppm -png -r 110 paper/icassp2027/main.pdf paper/icassp2027/render/page >> $LOG 2>&1
echo "SW_FINALIZE_DONE $(date)" >> $LOG
