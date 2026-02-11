![CI](https://github.com/Rahhal-SWE/netwatch/actions/workflows/ci.yml/badge.svg)

# netwatch (Python CLI)

Linux-friendly CLI tool that monitors host availability and latency using `ping`,
writes structured CSV logs, and prints summary reliability metrics.

## Usage

```bash
python -m netwatch.cli --hosts 1.1.1.1 google.com --count 3 --interval 1 --out logs.csv
