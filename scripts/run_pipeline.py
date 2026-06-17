"""Run full pipeline: generate → load → analytics → viz."""

import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import argparse
from src.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run full analytics pipeline")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate data only, skip ClickHouse and analytics",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=100_000,
        help="Number of rows to generate (default: 100000)",
    )
    args = parser.parse_args()

    run_pipeline(n_rows=args.rows, dry_run=args.dry_run)


if __name__ == "__main__":
    main()