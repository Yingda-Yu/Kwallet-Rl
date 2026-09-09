"""Model-only compute benchmark (paper: parameter count, wall-clock latency).

Environment simulation is excluded so all methods share the same sim cost; only
the policy forward/action sampling is timed. Warmup + explicit CUDA sync.
"""
from __future__ import annotations

import time
from typing import Dict

import numpy as np
import torch

from ..policies.actors import build_policy


def count_parameters(policy) -> int:
    return sum(p.numel() for p in policy.parameters() if p.requires_grad)


def benchmark_policy(method: str, obs_dim: int, k: int, hidden: int = 256,
                     embed: int = 32, n_layers: int = 2, device: str = "cpu",
                     repeats: int = 2000, warmup: int = 200,
                     batch_size: int = 1) -> Dict:
    dev = torch.device(device if device == "cpu" or torch.cuda.is_available()
                       else "cpu")
    policy = build_policy(method, obs_dim, k, hidden=hidden, embed=embed,
                          n_layers=n_layers).to(dev).eval()
    n_params = count_parameters(policy)
    x = torch.zeros(batch_size, obs_dim, device=dev)

    def _once():
        with torch.no_grad():
            policy.step(x, deterministic=True)
        if dev.type == "cuda":
            torch.cuda.synchronize()

    for _ in range(warmup):
        _once()
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        _once()
        times.append(time.perf_counter() - t0)
    times = np.asarray(times)
    mem = 0.0
    if dev.type == "cuda":
        torch.cuda.reset_peak_memory_stats(dev)
        for _ in range(50):
            _once()
        mem = torch.cuda.max_memory_allocated(dev) / 1e6  # MB
    return {
        "method": method,
        "device": str(dev),
        "batch_size": batch_size,
        "params": int(n_params),
        "output_logits": int(policy.output_logits()),
        "lat_p50_ms": float(np.percentile(times, 50) * 1e3),
        "lat_p95_ms": float(np.percentile(times, 95) * 1e3),
        "lat_mean_ms": float(times.mean() * 1e3),
        "throughput_eps": float(batch_size / times.mean()),
        "peak_mem_mb": float(mem),
    }
