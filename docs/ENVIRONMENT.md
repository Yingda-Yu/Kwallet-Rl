# Environment (verified on the SSH server)

Recorded 2026-09-09 by the execution agent. All items below were actually
checked on the host (not assumed).

## Host
- OS: Ubuntu 22.04
- CPU: 96 threads (Intel Xeon Gold 6248R), 503 GB RAM
- GPU: 10x NVIDIA RTX 3090 (24 GB). Driver supports CUDA 13.0.
  - Observed at audit: GPU0 ~12.5 GB used (others' jobs); GPU3 416 MiB;
    GPU 1/2/4 nearly idle (~21 MiB); GPU 6-9 at 100% (others' jobs).
  - **GPU usage is PENDING explicit user authorization.** Idle != authorized.
  - The PPO workload is batch-1 rollout dominated; CPU is competitive and used
    by default. CUDA torch only installed if/when GPU is authorized.
- Disk `/data`: was 97% full (~225 GB free) at audit — watch footprint.

## Software
- TeX Live 2022 (Debian): `pdflatex`, `latexmk`, `bibtex`, `xelatex`,
  `kpsewhich` present; `pdfinfo`, `pdffonts`, `pdftotext`, `pdfimages`,
  `unzip` present. Reused as-is (no TeX reinstall).
- conda: `/data/yingda/software/miniconda3`
- Dedicated env **`kwallet`** (Python 3.10):
  numpy 2.2.6, scipy 1.15.3, pandas 2.3.3, matplotlib, pyyaml, pytest,
  torch 2.14.0 **CPU-only** (forward/backward verified).
  Activate: `source /data/yingda/software/miniconda3/etc/profile.d/conda.sh && conda activate kwallet`

## Repository / workspace
- Working dir: `/data/yingda/Kwallet-Rl`
- Remote: `https://github.com/Yingda-Yu/Kwallet-Rl.git`
- Work branch: `work/icassp2027-reproduce-improve` (created from
  `origin/docs/kwallet-icassp2027-execution-20260909`; upstream unset to avoid
  pushing to the docs branch).
- Protected, untracked, untouched:
  - `paper/old paper.pdf`
    SHA-256 `3c82e8d888ca90f6d32921fe5639cec1453d69341ecd85cb9565c1af9c65040a`
  - `paper/ICASSP2027_Paper_Templates.zip`
    SHA-256 `fd1cc4102c4ad9a3e85eba96ee5ed261a45fab9c2630875eb2566812230c91a8`
- `.gitignore` excludes `*.pth`, `*.png`, `data/`, `results/`, `runs/`,
  `legacy/`, `__pycache__`, `*.log`. Generated artifacts live there.

## Resource policy
- CPU runs: authorized (lightweight checks + short tests first).
- GPU, large sweeps, killing other processes, driver changes: NOT authorized
  without explicit user confirmation. See `docs/BLOCKERS.md`.
