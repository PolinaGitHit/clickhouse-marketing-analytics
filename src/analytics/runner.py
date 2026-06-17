import json
import pandas as pd
from pathlib import Path
from src.db.client import get_client
from src.analytics.queries import load_query, AVAILABLE_QUERIES
from src.config import settings


def run_all() -> dict[str, pd.DataFrame]:
    client = get_client()
    results = {}

    for name, filename in AVAILABLE_QUERIES.items():
        sql = load_query(filename)
        df = client.query_df(sql)
        results[name] = df
        print(f"  ✓ {name}: {len(df)} rows")

    return results


def save_results(results: dict[str, pd.DataFrame]):
    out_dir = Path(settings.output_dir) / "analytics"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {}
    for name, df in results.items():
        path = out_dir / f"{name}.csv"
        df.to_csv(path, index=False)
        summary[name] = {
            "rows": len(df),
            "columns": list(df.columns),
            "csv_path": str(path),
        }

    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)