"""Execute all analytics SQL queries and save results."""

import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from src.analytics.runner import run_all, save_results
from src.analytics.cohort import build_cohorts


def main():
    print("Building cohorts...")
    build_cohorts()
    print("Done\n")

    print("Running analytics queries...")
    results = run_all()
    save_results(results)
    print(f"\nDone: {len(results)} queries saved to output/analytics/")


if __name__ == "__main__":
    main()