from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional
import statistics


@dataclass(frozen=True)
class ProbeResult:
    host: str
    ok: bool
    latency_ms: Optional[float]


def percentile(values: list[float], p: float) -> float:
    if not values:
        raise ValueError("values must be non-empty")
    if not (0 <= p <= 100):
        raise ValueError("p must be between 0 and 100")

    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]

    k = (len(xs) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    if f == c:
        return xs[f]
    d0 = xs[f] * (c - k)
    d1 = xs[c] * (k - f)
    return d0 + d1


def summarize(results: Iterable[ProbeResult]) -> dict:
    results = list(results)
    total = len(results)
    if total == 0:
        return {"total": 0, "success_rate": 0.0, "avg_latency_ms": None, "p95_latency_ms": None}

    oks = [r for r in results if r.ok and r.latency_ms is not None]
    success_rate = len(oks) / total
    latencies = [r.latency_ms for r in oks]  # type: ignore[list-item]

    if not latencies:
        return {"total": total, "success_rate": success_rate, "avg_latency_ms": None, "p95_latency_ms": None}

    return {
        "total": total,
        "success_rate": success_rate,
        "avg_latency_ms": statistics.fmean(latencies),
        "p95_latency_ms": percentile(latencies, 95),
    }
