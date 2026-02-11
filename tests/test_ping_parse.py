from netwatch.ping import parse_ping_output


def test_parse_ping_success():
    out = "64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=12.3 ms"
    r = parse_ping_output(out)
    assert r.ok is True
    assert r.latency_ms == 12.3


def test_parse_ping_fail():
    out = "ping: connect: Network is unreachable"
    r = parse_ping_output(out)
    assert r.ok is False
    assert r.latency_ms is None
