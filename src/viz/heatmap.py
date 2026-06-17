import plotly.express as px
import pandas as pd


def cohort_heatmap(df: pd.DataFrame) -> "plotly.graph_objects.Figure":
    pivot = df.pivot(
        index="cohort_week", columns="week_num", values="active_campaigns"
    )
    pivot_norm = pivot.divide(pivot[0], axis=0) * 100

    fig = px.imshow(
        pivot_norm,
        title="Когортный анализ: удержание кампаний (неделя 0 = 100%)",
        labels={
            "x": "Неделя после старта",
            "y": "Неделя когорты",
            "color": "% кампаний",
        },
        color_continuous_scale="RdYlGn",
        aspect="equal",
        text_auto=".0f",
        width=800,
        height=600,
    )
    fig.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="white")
    return fig


def weekday_heatmap(df: pd.DataFrame) -> "plotly.graph_objects.Figure":
    pivot = df.pivot(
        index="campaign_name", columns="dow", values="total_clicks"
    ).fillna(0)

    fig = px.imshow(
        pivot,
        title="Тепловая карта: клики по дням недели и кампаниям",
        labels={"x": "День недели", "y": "Кампания", "color": "Клики"},
        color_continuous_scale="YlOrRd",
        aspect="auto",
        text_auto=".0f",
        width=800,
        height=500,
    )
    fig.update_xaxes(
        tickvals=list(range(7)),
        ticktext=["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    )
    fig.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="white")
    return fig