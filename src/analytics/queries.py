from pathlib import Path

QUERIES_DIR = Path(__file__).parent.parent.parent / "queries"


def load_query(name: str) -> str:
    path = QUERIES_DIR / name
    if not path.suffix:
        path = path.with_suffix(".sql")
    return path.read_text(encoding="utf-8")


AVAILABLE_QUERIES = {
    "ctr_by_campaign": "01_ctr_by_campaign.sql",
    "cpa_by_campaign": "02_cpa_by_campaign.sql",
    "daily_metrics": "03_daily_metrics.sql",
    "top_regions": "04_top_regions.sql",
    "group_efficiency": "05_group_efficiency.sql",
    "weekday_distribution": "06_weekday_distribution.sql",
    "ctr_by_month": "07_ctr_by_month.sql",
    "campaign_summary": "08_campaign_summary.sql",
    "monthly_metrics": "09_monthly_metrics.sql",
    "daily_by_campaign": "10_daily_by_campaign.sql",
    "cohort_retention_matrix": "cohort/05_retention_matrix.sql",
}