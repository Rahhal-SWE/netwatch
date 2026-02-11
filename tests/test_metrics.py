import pytest
from netwatch.metrics import ProbeResult, summarize, percentile


def test_summarize_empty():
    s = summarize([])
    assert s["total"] == 0
    assert s["success_rate"] == 0.0


def test_summarize_mixed():
    rs = [
        ProbeResult("a", True, 10.0),
        ProbeResult("a", False, None),
        ProbeResult("b", True, 30.0),
    ]
    s = summarize(rs)
    assert s["total"] == 3
    assert s["success_rate"] == pytest.approx(2 / 3)
    assert s["avg_latency_ms"] == pytest.approx(20.0)


def test_percentile_bounds():
    xs = [10.0, 20.0, 30.0]
    assert percentile(xs, 0) == 10.0
    assert percentile(xs, 100) == 30.0
