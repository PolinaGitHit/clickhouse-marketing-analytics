import pandas as pd
import numpy as np
import random
from pathlib import Path
from src.config import settings
from src.data.loader import load_real_data, get_unique_values

COLUMNS = [
    "День",
    "№ Кампании",
    "Название кампании",
    "Название группы",
    "№ Группы",
    "№ Объявления",
    "Регион местонахождения",
    "Регион местонахождения.1",
    "Ключевая фраза",
    "Расход, ₽",
    "Показы",
    "Клики",
    "Конверсии",
    "CR, %",
    "CPA, ₽",
    "CTR, %",
]


def generate(n_rows: int = 100_000, seed: int = 42) -> pd.DataFrame:
    df_real = load_real_data()
    uniques = get_unique_values(df_real)

    np.random.seed(seed)
    random.seed(seed)
    dates = pd.date_range(start="2025-09-01", end="2026-06-17", freq="D")
    data = []

    for _ in range(n_rows):
        day = random.choice(dates)
        impressions = np.random.poisson(80) + 1
        clicks = max(0, int(np.random.poisson(impressions * 0.08)))
        cost = round(clicks * np.random.uniform(50, 300), 2)
        conversions = max(0, np.random.poisson(clicks * 0.08))

        data.append(
            [
                day.strftime("%d.%m.%Y"),
                random.randint(706_000_000, 710_999_999),
                random.choice(uniques["campaigns"]),
                random.choice(uniques["groups"]),
                random.randint(570_000_000, 579_999_999),
                random.randint(17_000_000_000, 19_999_999_999),
                *(random.choice(uniques["regions"])),
                random.choice(uniques["keywords"]),
                cost,
                impressions,
                clicks,
                conversions,
                round(conversions / clicks * 100, 2) if clicks > 0 else 0.0,
                round(cost / conversions, 2) if conversions > 0 else None,
                round(clicks / impressions * 100, 2),
            ]
        )

    return pd.DataFrame(data, columns=COLUMNS)


def save_generated(df: pd.DataFrame) -> Path:
    path = Path(settings.generated_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    return path