"""Generate synthetic ads data from real CSV patterns."""

import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from src.data.generator import generate, save_generated


def main():
    print("Generating 100 000 rows of synthetic ads data...")
    df = generate(n_rows=100_000)
    path = save_generated(df)
    print(f"Done: {path} ({len(df)} rows)")


if __name__ == "__main__":
    main()