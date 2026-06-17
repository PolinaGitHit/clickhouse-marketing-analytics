import logging
from pathlib import Path

from src.config import settings
from src.viz.charts import ctr_bar_aggregated as ctr_bar, daily_line, cpa_pie
from src.viz.heatmap import cohort_heatmap, weekday_heatmap

logger = logging.getLogger(__name__)


def export_all(results: dict) -> Path:
    out_dir = Path(settings.output_dir) / "charts"
    out_dir.mkdir(parents=True, exist_ok=True)

    chart_map = {
        "ctr_by_campaign": ctr_bar,
        "daily_metrics": daily_line,
        "top_regions": cpa_pie,
    }

    for name, df in results.items():
        if name in chart_map:
            fig = chart_map[name](df)
            fig.write_html(out_dir / f"{name}.html")

            try:
                fig.write_image(out_dir / f"{name}.png", scale=2)
            except Exception as exc:
                logger.warning(
                    "PNG export skipped for '%s': %s", name, exc
                )

    return out_dir