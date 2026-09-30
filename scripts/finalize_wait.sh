#!/bin/bash
# Comprehensive, durable finalization for the K-Wallet ICASSP round.
# Waits for the three experiment drivers, then aggregates, stats, switching,
# regenerates paper assets, and compiles. Each step logs its exit code.
source /data/yingda/software/miniconda3/etc/profile.d/conda.sh
conda activate kwallet
cd /data/yingda/Kwallet-Rl
LOG=runs/finalize.log
echo "finalize(v3) started $(date)" > "$LOG"

step() { echo "----- STEP: $*  ($(date)) -----" >> "$LOG"; "$@" >> "$LOG" 2>&1; echo "  rc=$?  ($(date))" >> "$LOG"; }

# 1) Wait until no driver processes remain (pattern won't match this bash).
echo "waiting for drivers to finish..." >> "$LOG"
while true; do
  n=$(pgrep -f 'python scripts/run_' | wc -l)
  t=$(pgrep -f 'envs/kwallet/bin/python -m kwallet.cli train' | wc -l)
  if [ "$n" -eq 0 ] && [ "$t" -eq 0 ]; then break; fi
  sleep 60
done
echo "=== all drivers + train procs finished $(date) ===" >> "$LOG"
# extra drain for eval subprocesses
while [ "$(pgrep -f 'envs/kwallet/bin/python -m kwallet.cli evaluate' | wc -l)" -gt 0 ]; do sleep 30; done
echo "=== eval procs drained $(date) ===" >> "$LOG"

# 2) Aggregation
step python scripts/aggregate_results.py --exp matrix_main
step python scripts/aggregate_results.py --exp matrix_ablation
step python scripts/aggregate_kscale.py --exp kscale
# 3) Paired statistics (seed-level CIs)
step python scripts/paired_stats.py --exp matrix_main
step python scripts/paired_stats.py --exp matrix_ablation
# 4) Learned-policy switching on trained matrix checkpoints (3 seeds)
step python scripts/run_switching.py --exp switching --train-exp matrix_main --seeds 123 323 532 --n 200
# 5) Regenerate all tables/figures/claims from CSVs
step python scripts/make_paper_assets.py --exp matrix_main --ablation matrix_ablation --kscale kscale
# 6) Compile PDF (clean)
cd paper/icassp2027
step rm -f main.aux main.bbl main.blg main.out main.log
step pdflatex -interaction=nonstopmode main.tex
step bibtex main
step pdflatex -interaction=nonstopmode main.tex
step pdflatex -interaction=nonstopmode main.tex
cd /data/yingda/Kwallet-Rl
echo "===== PDF CHECK =====" >> "$LOG"
pdfinfo paper/icassp2027/main.pdf >> "$LOG" 2>&1
pdffonts paper/icassp2027/main.pdf >> "$LOG" 2>&1
mkdir -p paper/icassp2027/render
pdftoppm -png -r 110 paper/icassp2027/main.pdf paper/icassp2027/render/page >> "$LOG" 2>&1
echo "rendered pages:" >> "$LOG"; ls paper/icassp2027/render/ >> "$LOG" 2>&1
echo "FINALIZE_DONE $(date)" >> "$LOG"
