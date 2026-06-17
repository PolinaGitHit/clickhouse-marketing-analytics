import pandas as pd
from pathlib import Path
from src.config import settings


def load_real_data() -> pd.DataFrame:
    path = Path(settings.dataset_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, skiprows=[1], sep=",").dropna(how="all")
    return df


def get_unique_values(df: pd.DataFrame) -> dict:
    return {
        "campaigns": df["Название кампании"].unique(),
        "groups": df["Название группы"].unique(),
        "regions": (
            df[["Регион местонахождения", "Регион местонахождения.1"]]
            .drop_duplicates()
            .values
        ),
        "keywords": df["Ключевая фраза"].dropna().unique(),
    }