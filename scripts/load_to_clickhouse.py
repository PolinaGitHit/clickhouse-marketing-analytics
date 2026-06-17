"""Load generated CSV data into ClickHouse."""

import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from src.data.ingestor import ingest_csv
from src.config import settings


def main():
    csv_path = settings.generated_file
    print(f"Ingesting {csv_path} into ClickHouse...")
    count = ingest_csv(csv_path)
    print(f"Done: {count} rows in ClickHouse")


if __name__ == "__main__":
    main()