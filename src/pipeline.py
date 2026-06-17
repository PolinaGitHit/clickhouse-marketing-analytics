from src.data.generator import generate, save_generated
from src.data.ingestor import ingest_csv
from src.analytics.runner import run_all, save_results
from src.analytics.cohort import build_cohorts
from src.viz.report import export_all


def run_pipeline(n_rows: int = 100_000, dry_run: bool = False):
    print("1. Генерация данных...")
    df = generate(n_rows=n_rows)
    path = save_generated(df)
    print(f"   → {path} ({len(df)} rows)")

    if dry_run:
        print("   [dry-run] Пропуск загрузки в ClickHouse, аналитики и визуализации")
        return

    print("2. Загрузка в ClickHouse...")
    count = ingest_csv(str(path))
    print(f"   → {count} rows loaded")

    print("3. Когортный анализ...")
    build_cohorts()

    print("4. Выполнение SQL-запросов...")
    results = run_all()
    save_results(results)

    print("5. Экспорт графиков...")
    export_all(results)

    print("✓ Пайплайн завершён")