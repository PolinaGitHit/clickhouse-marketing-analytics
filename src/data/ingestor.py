import pandas as pd
from src.db.client import get_client
from src.config import settings


def ingest_csv(csv_path: str) -> int:
    client = get_client()

    df = pd.read_csv(csv_path)
    df["День"] = pd.to_datetime(df["День"], format="%d.%m.%Y")
    df["CPA, ₽"] = df["CPA, ₽"].replace("-", None).astype(float)

    client.insert_df(
        table=f"{settings.clickhouse_db}.ads_data",
        df=df,
        column_names=[
            "event_date",
            "campaign_id",
            "campaign_name",
            "group_name",
            "group_id",
            "ad_id",
            "region",
            "region_code",
            "keyword",
            "cost",
            "impressions",
            "clicks",
            "conversions",
            "cr",
            "cpa",
            "ctr",
        ],
    )

    result = client.query(f"SELECT count() FROM {settings.clickhouse_db}.ads_data")
    return result.result_rows[0][0]