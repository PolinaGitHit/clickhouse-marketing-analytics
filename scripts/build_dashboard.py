"""Build dashboard: export charts to HTML/PNG."""

import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from src.analytics.runner import run_all, save_results
from src.viz.report import export_all


def main():
    print("Running analytics queries...")
    results = run_all()
    save_results(results)
    print(f"  → {len(results)} queries saved")

    print("Exporting charts...")
    out_dir = export_all(results)
    print(f"  → Charts saved to {out_dir}")


if __name__ == "__main__":
    main()