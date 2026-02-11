from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import re
import subprocess
import time


@dataclass(frozen=True)
class PingOutcome:
    ok: bool
    latency_ms: Optional[float]
    raw: str


# Typical Linux ping output includes: "time=12.3 ms"
_TIME_RE = re.compile(r"time=(\d+(\.\d+)?)\s*ms")


def parse_ping_output(output: str) -> PingOutcome:
    m = _TIME_RE.search(output)
    if m:
        return PingOutcome(ok=True, latency_ms=float(m.group(1)), raw=output)
    # If no time=... found, treat as failure
    return PingOutcome(ok=False, latency_ms=None, raw=output)


def ping_once(host: str, timeout_seconds: int = 2) -> PingOutcome:
    """
    Uses system ping (Linux):
      ping -c 1 -W <timeout> <host>
    """
    try:
        cp = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout_seconds), host],
            capture_output=True,
            text=True,
            check=False,
        )
        combined = (cp.stdout or "") + "\n" + (cp.stderr or "")
        if cp.returncode == 0:
            return parse_ping_output(combined)
        return PingOutcome(ok=False, latency_ms=None, raw=combined)
    except FileNotFoundError:
        return PingOutcome(ok=False, latency_ms=None, raw="ping command not found")


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
