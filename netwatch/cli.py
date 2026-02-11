from __future__ import annotations

import argparse
import csv
import time

from netwatch.metrics import ProbeResult, summarize
from netwatch.ping import ping_once, now_iso


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="netwatch", description="Ping hosts, log results, print summary.")
    p.add_argument("--hosts", nargs="+", required=True, help="Hostnames or IPs to ping")
    p.add_argument("--count", type=int, default=5, help="Number of rounds to run")
    p.add_argument("--interval", type=float, default=1.0, help="Seconds between rounds")
    p.add_argument("--out", default="netwatch_log.csv", help="CSV output file")
    p.add_argument("--timeout", type=int, default=2, help="Ping timeout seconds")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    results: list[ProbeResult] = []

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["timestamp", "host", "ok", "latency_ms"]
        )
        writer.writeheader()

        for i in range(args.count):
            for host in args.hosts:
                outcome = ping_once(host, timeout_seconds=args.timeout)
                r = ProbeResult(host=host, ok=outcome.ok, latency_ms=outcome.latency_ms)
                results.append(r)
                writer.writerow(
                    {
                        "timestamp": now_iso(),
                        "host": host,
                        "ok": outcome.ok,
                        "latency_ms": outcome.latency_ms if outcome.latency_ms is not None else "",
                    }
                )
            if i != args.count - 1:
                time.sleep(args.interval)

    s = summarize(results)
    print("Summary")
    print(f"  Total probes:   {s['total']}")
    print(f"  Success rate:   {s['success_rate']:.2%}")
    print(f"  Avg latency ms: {s['avg_latency_ms'] if s['avg_latency_ms'] is not None else 'N/A'}")
    print(f"  P95 latency ms: {s['p95_latency_ms'] if s['p95_latency_ms'] is not None else 'N/A'}")
    print(f"  Log written to: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
