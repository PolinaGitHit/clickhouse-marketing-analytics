from src.db.client import get_client
from src.analytics.queries import load_query
from src.config import settings
import clickhouse_connect


def build_cohorts():
    client = get_client()
    db = settings.clickhouse_db
    sql = load_query("cohort/01_create_cohorts.sql")
    client.command(sql.replace("{db}", db))


def retention_weekly() -> list:
    client = get_client()
    sql = load_query("cohort/03_retention_function.sql")
    return client.query(sql).result_rows


def retention_matrix_df() -> "pd.DataFrame":
    """Возвращает матрицу удержания (cohort_week, week_num, active_campaigns) как DataFrame."""
    import pandas as pd
    client = clickhouse_connect.get_client(
        host=settings.clickhouse_host,
        port=settings.clickhouse_port,
        username=settings.clickhouse_user,
        password=settings.clickhouse_password,
    )
    sql = load_query("cohort/05_retention_matrix.sql").replace("{db}", settings.clickhouse_db)
    return client.query_df(sql)


def keyword_retention() -> list:
    client = get_client()
    sql = load_query("cohort/04_keyword_retention.sql")
    return client.query(sql).result_rows