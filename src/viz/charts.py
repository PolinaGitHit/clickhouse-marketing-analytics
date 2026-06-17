import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def ctr_monthly_line(df: pd.DataFrame) -> go.Figure:
    """Мульти-линейный график CTR по месяцам для всех кампаний."""
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly

    for i, campaign in enumerate(df["campaign_name"].unique()):
        df_c = df[df["campaign_name"] == campaign].sort_values("month")
        color = colors[i % len(colors)]

        fig.add_trace(go.Scatter(
            x=df_c["month"],
            y=df_c["avg_ctr"],
            mode="lines+markers",
            name=campaign,
            marker=dict(size=8, color=color),
            line=dict(color=color),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Месяц: %{x}<br>"
                "CTR: %{y:.2f}%<br>"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        title="CTR по кампаниям по месяцам",
        xaxis_title="Месяц",
        yaxis_title="CTR, %",
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            y=-0.25,
            font=dict(size=10),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e0e0e0",
            borderwidth=1,
        ),
        margin=dict(l=60, r=30, t=60, b=130),
    )
    return fig


def campaign_efficiency_scatter(df: pd.DataFrame) -> go.Figure:
    """Матрица эффективности кампаний: CTR vs CPA, размер = расходы.
    Лучшие кампании — в верхнем левом углу (высокий CTR, низкий CPA)."""
    fig = go.Figure()

    # Scale total_cost to marker sizes
    cost_min, cost_max = df["total_cost"].min(), df["total_cost"].max()
    cost_range = cost_max - cost_min if cost_max != cost_min else 1
    size_min, size_max = 12, 70
    colors = px.colors.qualitative.Plotly

    for i, (_, row) in enumerate(df.iterrows()):
        size = size_min + (row["total_cost"] - cost_min) / cost_range * (size_max - size_min)
        fig.add_trace(go.Scatter(
            x=[row["avg_ctr"]],
            y=[row["avg_cpa"]],
            mode="markers+text",
            name=row["campaign_name"],
            text=row["campaign_name"],
            textposition="middle center",
            textfont=dict(size=13, color="white", family="Arial Black"),
            marker=dict(
                size=size,
                color=colors[i % len(colors)],
                line=dict(width=1, color="rgba(0,0,0,0.2)"),
            ),
            customdata=[[row["total_cost"]]],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "CTR: %{x:.2f}%<br>"
                "CPA: %{y:.2f} руб<br>"
                "Расход: %{customdata[0]:,.0f} руб<br>"
                "<extra></extra>"
            ),
        ))

    # Layout
    fig.update_layout(
        title="Матрица эффективности кампаний",
        xaxis_title="CTR, %",
        yaxis_title="CPA, руб",
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            y=-0.20,
            font=dict(size=10),
            bgcolor="white",
            bordercolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
        margin=dict(l=80, r=30, t=60, b=95),
        yaxis=dict(range=[df["avg_cpa"].min() * 0.9, df["avg_cpa"].max() * 1.1]),
    )

    # Разделительные линии: медиана CTR и медиана CPA
    median_ctr = df["avg_ctr"].median()
    median_cpa = df["avg_cpa"].median()
    fig.add_hline(y=median_cpa, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=median_ctr, line_dash="dash", line_color="gray", opacity=0.5)

    # Аннотация квадрантов
    fig.add_annotation(
        x=df["avg_ctr"].max(), y=df["avg_cpa"].min(),
        text="Лучшие", showarrow=False,
        font=dict(color="green", size=12),
        xshift=-40, yshift=10,
    )
    fig.add_annotation(
        x=df["avg_ctr"].min(), y=df["avg_cpa"].max(),
        text="Худшие", showarrow=False,
        font=dict(color="red", size=12),
        xshift=40, yshift=-10,
    )

    # Аннотации-подсказки по осям (отцентрированы, не пересекаются с подписями осей)
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=-0.06,
        text="← Выше CTR →",
        showarrow=False,
        font=dict(size=11, color="gray", family="Arial"),
        opacity=0.6,
    )
    fig.add_annotation(
        xref="paper", yref="paper",
        x=-0.07, y=0.5,
        text="↓ Ниже CPA",
        showarrow=False,
        font=dict(size=11, color="gray", family="Arial"),
        opacity=0.6,
        textangle=-90,
    )

    return fig


def campaign_sunburst(df_groups: pd.DataFrame) -> go.Figure:
    """Иерархия расходов: Кампания → Группа.
    Размер сектора = расходы, цвет = CTR."""
    fig = px.sunburst(
        df_groups,
        path=["campaign_name", "group_name"],
        values="total_cost",
        color="avg_ctr",
        color_continuous_scale="RdYlGn",
        title="Структура расходов по кампаниям и группам",
        labels={
            "campaign_name": "Кампания",
            "group_name": "Группа",
            "total_cost": "Расход, руб",
            "avg_ctr": "CTR, %",
        },
        template="plotly_white",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Расход: %{value:,.0f} руб<br>"
            "CTR: %{color:.2f}%<br>"
            "<extra></extra>"
        ),
    )
    fig.update_layout(height=600, paper_bgcolor="white", plot_bgcolor="white")
    return fig


def campaign_performance_table(df: pd.DataFrame) -> go.Figure:
    """Красивая таблица эффективности кампаний с рейтингом, цветовыми шкалами и барами."""
    df_display = df.copy()
    n = len(df_display)
    if n == 0:
        return go.Figure()

    # ── Подготовка данных ──
    df_display["rank"] = range(1, n + 1)
    max_cost = df_display["total_cost"].max() or 1
    max_clicks = df_display["total_clicks"].max() or 1
    max_ctr = df_display["avg_ctr"].max() or 1

    # CPA color: lower = greener, higher = redder
    cpa_min = df_display["avg_cpa"].min()
    cpa_max = df_display["avg_cpa"].max()
    cpa_range = cpa_max - cpa_min if cpa_max != cpa_min else 1

    def cpa_color(v):
        if pd.isna(v):
            return "#f0f0f0"
        ratio = (v - cpa_min) / cpa_range  # 0..1
        r = int(40 + 195 * ratio)
        g = int(200 - 180 * ratio)
        b = int(60 - 40 * ratio)
        return f"rgb({r},{g},{b})"

    def bar_html(val, max_val, color="#5b9bd5"):
        frac = val / max_val
        return (
            f'<div style="display:flex;align-items:center;gap:6px;justify-content:center">'
            f'<div style="width:80px;height:14px;background:#e9ecef;border-radius:7px;overflow:hidden">'
            f'<div style="width:{frac * 100:.0f}%;height:100%;background:{color};border-radius:7px"></div>'
            f'</div>'
            f'<span style="font-size:12px">{val:,.0f}</span>'
            f'</div>'
        )

    def ctr_bar_html(val, max_val):
        frac = val / max_val
        green = int(40 + 185 * frac)
        return (
            f'<div style="display:flex;align-items:center;gap:6px;justify-content:center">'
            f'<div style="width:80px;height:14px;background:#e9ecef;border-radius:7px;overflow:hidden">'
            f'<div style="width:{frac * 100:.0f}%;height:100%;background:rgb({255 - green},{green},{80});border-radius:7px"></div>'
            f'</div>'
            f'<span style="font-size:12px;font-weight:500">{val:.2f}</span>'
            f'</div>'
        )

    def cpa_html(val):
        if pd.isna(val):
            return '<span style="color:#aaa">—</span>'
        bg = cpa_color(val)
        text_color = "white" if val > (cpa_min + cpa_range * 0.6) else "#222"
        return (
            f'<div style="display:flex;align-items:center;gap:6px;justify-content:center">'
            f'<div style="background:{bg};color:{text_color};padding:2px 12px;'
            f'border-radius:10px;font-size:12px;font-weight:600;min-width:50px;text-align:center">'
            f'{val:.2f}</div>'
            f'</div>'
        )

    # Build HTML cells with inline styling
    rank_cells = []
    name_cells = []
    ctr_cells = []
    cpa_cells = []
    cost_cells = []
    clicks_cells = []
    conv_cells = []

    for _, row in df_display.iterrows():
        r = int(row["rank"])
        # Rank badge
        if r == 1:
            badge = f'<span style="background:#ffd700;color:#222;border-radius:50%;display:inline-block;width:26px;height:26px;line-height:26px;font-weight:700;font-size:13px">{r}</span>'
        elif r == 2:
            badge = f'<span style="background:#c0c0c0;color:#222;border-radius:50%;display:inline-block;width:26px;height:26px;line-height:26px;font-weight:700;font-size:13px">{r}</span>'
        elif r == 3:
            badge = f'<span style="background:#cd7f32;color:white;border-radius:50%;display:inline-block;width:26px;height:26px;line-height:26px;font-weight:700;font-size:13px">{r}</span>'
        else:
            badge = f'<span style="color:#888;font-weight:500;font-size:13px">{r}</span>'
        rank_cells.append(badge)

        name_cells.append(
            f'<span style="font-weight:600;font-size:13px">{row["campaign_name"]}</span>'
        )

        ctr_cells.append(ctr_bar_html(row["avg_ctr"], max_ctr))
        cpa_cells.append(cpa_html(row["avg_cpa"]))
        cost_cells.append(bar_html(row["total_cost"], max_cost, "#5b9bd5"))
        clicks_cells.append(bar_html(row["total_clicks"], max_clicks, "#70ad47"))
        conv_cells.append(
            f'<span style="font-size:13px;font-weight:500">{row["total_conversions"]:,.0f}</span>'
        )

    # ── Header gradient ──
    header_bg = "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)"

    fig = go.Figure(data=[
        go.Table(
            columnwidth=[50, 200, 140, 100, 140, 130, 100],
            header=dict(
                values=[
                    "<b>№</b>",
                    "<b>Кампания</b>",
                    "<b>CTR, %</b>",
                    "<b>CPA, руб</b>",
                    "<b>Расход, руб</b>",
                    "<b>Клики</b>",
                    "<b>Конверсии</b>",
                ],
                fill_color=header_bg,
                font=dict(color="white", size=13),
                align="center",
                height=38,
                line_color="rgba(255,255,255,0.08)",
            ),
            cells=dict(
                values=[rank_cells, name_cells, ctr_cells, cpa_cells, cost_cells, clicks_cells, conv_cells],
                fill_color=[
                    ["#f8f9fa", "white"] * (n // 2 + 1),
                ] * 7,
                font=dict(size=12, color=["#333"] * 7),
                align="center",
                height=38,
                line_color="#e9ecef",
                line_width=1,
            ),
        )
    ])

    fig.update_layout(
        title=dict(
            text="<b>Рейтинг кампаний</b>  —  по расходам (↓CPA = зелёный, ↑CTR = насыщеннее)",
            font=dict(size=16, color="#1a1a2e"),
            x=0.5,
        ),
        margin=dict(l=10, r=10, t=60, b=20),
        height=120 + 42 * n,
        paper_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )
    return fig


# ── Сохранённые старые функции (для совместимости) ──

def ctr_bar_aggregated(df: pd.DataFrame) -> go.Figure:
    return px.bar(
        df,
        x="campaign_name",
        y="avg_ctr",
        title="CTR по кампаниям (среднее за весь период)",
        labels={"campaign_name": "Кампания", "avg_ctr": "CTR, %"},
        color="avg_ctr",
        color_continuous_scale="blues",
        template="plotly_white",
    )


def daily_line_enhanced(df: pd.DataFrame) -> go.Figure:
    """Линейный график динамики метрик с range slider и secondary y для CTR."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["event_date"], y=df["total_cost"],
        name="Расход, руб",
        mode="lines+markers",
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=df["event_date"], y=df["total_clicks"],
        name="Клики",
        mode="lines+markers",
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=df["event_date"], y=df["total_conversions"],
        name="Конверсии",
        mode="lines+markers",
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=df["event_date"], y=df["avg_ctr"],
        name="CTR, %",
        yaxis="y2",
        mode="lines+markers",
        marker=dict(size=5),
        line=dict(dash="dot"),
    ))

    fig.update_layout(
        title=dict(
            text="Динамика метрик по дням",
            font=dict(size=15),
        ),
        xaxis=dict(
            title="Дата",
            rangeslider_visible=True,
            type="date",
        ),
        yaxis=dict(title="Значение"),
        yaxis2=dict(
            title="CTR, %",
            overlaying="y",
            side="right",
        ),
        height=500,
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            y=-0.38,
            x=0.5,
            xanchor="center",
            font=dict(size=11),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e0e0e0",
            borderwidth=1,
        ),
        margin=dict(l=70, r=50, t=50, b=140),
    )
    return fig


def regions_treemap(df: pd.DataFrame) -> go.Figure:
    """Treemap регионов: размер = расход, цвет = клики."""
    df = df.copy()
    df["label"] = df["region"] + "<br>" + df["total_cost"].apply(
        lambda x: f"{x:,.0f} руб"
    )
    fig = px.treemap(
        df,
        path=["region"],
        values="total_cost",
        color="total_clicks",
        color_continuous_scale="blues",
        title="Топ-10 регионов: расходы и клики",
        labels={
            "region": "Регион",
            "total_cost": "Расход, руб",
            "total_clicks": "Клики",
        },
        template="plotly_white",
    )
    fig.update_traces(
        textinfo="label+value+percent root",
        hovertemplate="<b>%{label}</b><br>Расход: %{value:,.0f} руб<br>Клики: %{color:,.0f}<extra></extra>",
    )
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    return fig


def cpa_bar(df: pd.DataFrame) -> go.Figure:
    """Столбчатая диаграмма CPA по кампаниям."""
    fig = px.bar(
        df,
        x="campaign_name",
        y="avg_cpa",
        title="CPA по кампаниям",
        labels={"campaign_name": "Кампания", "avg_cpa": "CPA, руб"},
        color="avg_cpa",
        color_continuous_scale="Reds",
        template="plotly_white",
    )
    fig.update_xaxes(tickangle=45)
    return fig


def daily_line(df: pd.DataFrame) -> go.Figure:
    return px.line(
        df,
        x="event_date",
        y=["total_cost", "total_clicks", "total_conversions"],
        title="Динамика метрик по дням",
        labels={
            "event_date": "Дата",
            "value": "Значение",
            "variable": "Метрика",
            "total_cost": "Расход, руб",
            "total_clicks": "Клики",
            "total_conversions": "Конверсии",
        },
    )


def cpa_pie(df: pd.DataFrame) -> go.Figure:
    return px.pie(
        df,
        values="total_cost",
        names="region",
        title="Топ-10 регионов по расходам",
    )


def monthly_bar(df: pd.DataFrame, metrics: list[str]) -> go.Figure:
    """Групповая столбчатая диаграмма метрик по месяцам.

    metrics — список строк из набора:
    'Расход', 'Клики', 'Показы', 'Конверсии', 'CTR', 'CPA'.
    """
    _COL_MAP = {
        "Расход": ("total_cost", "left"),
        "Клики": ("total_clicks", "left"),
        "Показы": ("total_impressions", "left"),
        "Конверсии": ("total_conversions", "left"),
        "CTR": ("avg_ctr", "right"),
        "CPA": ("avg_cpa", "right"),
    }
    _COLORS = {
        "Расход": "#5b9bd5",
        "Клики": "#70ad47",
        "Показы": "#ffc000",
        "Конверсии": "#ed7d31",
        "CTR": "#4472c4",
        "CPA": "#a5a5a5",
    }
    _LABELS = {
        "Расход": "Расход, руб",
        "Клики": "Клики",
        "Показы": "Показы",
        "Конверсии": "Конверсии",
        "CTR": "CTR, %",
        "CPA": "CPA, руб",
    }

    if not metrics:
        fig = go.Figure()
        fig.add_annotation(text="Нет выбранных метрик", showarrow=False)
        fig.update_layout(height=300, paper_bgcolor="white")
        return fig

    has_left = any(_COL_MAP[m][1] == "left" for m in metrics if m in _COL_MAP)
    has_right = any(_COL_MAP[m][1] == "right" for m in metrics if m in _COL_MAP)

    fig = go.Figure()

    for metric in metrics:
        entry = _COL_MAP.get(metric)
        if entry is None:
            continue
        col, side = entry
        fig.add_trace(go.Bar(
            x=df["month"],
            y=df[col],
            name=_LABELS.get(metric, metric),
            marker_color=_COLORS.get(metric, "#5b9bd5"),
            yaxis="y" if side == "left" else "y2",
        ))

    # Если выбрана только одна метрика — добавить линию тренда
    if len(metrics) == 1:
        entry = _COL_MAP.get(metrics[0])
        if entry:
            col, side = entry
            fig.add_trace(go.Scatter(
                x=df["month"],
                y=df[col],
                mode="lines+markers",
                name=f"{_LABELS.get(metrics[0], metrics[0])} (тренд)",
                line=dict(color="rgba(200,50,50,0.5)", width=2),
                marker=dict(size=6, color="rgba(200,50,50,0.7)"),
                yaxis="y" if side == "left" else "y2",
            ))

    layout_kw = dict(
        title="Метрики по месяцам",
        xaxis=dict(title="Месяц", type="date"),
        barmode="group",
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=450,
        margin=dict(l=70, r=70, t=50, b=130),
        legend=dict(
            orientation="h",
            y=-0.40,
            x=0.5,
            xanchor="center",
            font=dict(size=11),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e0e0e0",
            borderwidth=1,
        ),
    )

    if has_left and has_right:
        layout_kw["yaxis"] = dict(title="Количество / руб")
        layout_kw["yaxis2"] = dict(
            title="CTR, % / CPA, руб",
            overlaying="y",
            side="right",
        )
    elif has_right:
        layout_kw["yaxis"] = dict(title="CTR, % / CPA, руб")
    else:
        layout_kw["yaxis"] = dict(title="Значение")

    fig.update_layout(**layout_kw)
    return fig