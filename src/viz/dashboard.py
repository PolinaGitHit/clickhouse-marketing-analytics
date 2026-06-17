import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import pandas as pd
import plotly.express as px
import streamlit as st
import clickhouse_connect
from src.config import settings
from src.analytics.queries import load_query, AVAILABLE_QUERIES
from src.viz.charts import (
    ctr_monthly_line,
    daily_line_enhanced,
    monthly_bar,
    regions_treemap,
    campaign_efficiency_scatter,
    campaign_sunburst,
)
from src.viz.heatmap import cohort_heatmap, weekday_heatmap
from src.analytics.cohort import build_cohorts, retention_matrix_df

st.set_page_config(page_title="Маркетинговая аналитика", layout="wide")

# ── Кастомный CSS ──
st.markdown("""<meta name="color-scheme" content="light dark">
<style>
    /* Основной фон — светлый */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    /* Табы */
    .stTabs [data-baseweb="tab-list"] {
        background: #e8f0e8;
        border-radius: 12px;
        padding: 6px;
        gap: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        margin-top: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
        font-size: 14px;
        color: #5a6f5a;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #c5dfc8, #b8d4ba);
        color: #2d3e2d !important;
        box-shadow: 0 2px 8px rgba(181,199,175,0.3);
    }
    /* Subheader — без серой линии */
    h2, h3 {
        color: #2d3e2d;
        font-weight: 600;
        font-size: 18px;
        padding: 6px 0 4px 0;
    }
    /* Expanders */
    .streamlit-expanderHeader {
        background: #f0f5f0;
        border-radius: 8px;
        border: 1px solid #d4e0d4;
        font-weight: 500;
        color: #2d3e2d;
    }
    /* Карточки для графиков — центрирование содержимого */
    div[data-testid="stPlotlyChart"] {
        background: white;
        border-radius: 14px;
        padding: 10px 14px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 16px;
        transition: box-shadow 0.2s;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    div[data-testid="stPlotlyChart"] > div {
        width: 100%;
        max-width: 100%;
        overflow: hidden;
    }
    div[data-testid="stPlotlyChart"]:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    /* Selectbox & Slider — в карточках */
    .stSelectbox, .stSlider {
        background: white;
        padding: 12px 16px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    }
    /* Error/info boxes */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    /* Caption */
    .stCaption {
        color: #555;
        font-size: 13px;
        padding-left: 4px;
        margin-bottom: 8px;
    }
    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    }
    /* Убрать все hr */
    hr, .stDivider {
        display: none !important;
    }
    /* Скрыть верхнюю панель Streamlit (Deploy, Manage app, меню) */
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    /* ═══════════════════════════════════════════════════
       ТЁМНАЯ ТЕМА — единая цветовая гамма
       ═══════════════════════════════════════════════════ */
    @media (prefers-color-scheme: dark) {
        :root {color-scheme: dark !important;}

        .stApp {
            background: linear-gradient(135deg, #0f1117 0%, #1a1d2e 50%, #12141c 100%) !important;
            color: #e0e0e0 !important;
        }
        .stApp > header,
        .stApp > [data-testid="stHeader"] {
            background: transparent !important;
        }

        h2, h3 {
            color: #c0caf5 !important;
        }
        h2, h3, .stMarkdown p, .stMarkdown span, label, .st-bb, .st-bc {
            color: #c0caf5 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: #1e2132 !important;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #7a7f9a !important;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #3b3f5c, #2d3250) !important;
            color: #c0caf5 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
        }

        div[data-testid="stPlotlyChart"] {
            background: #1a1d2e !important;
            box-shadow: 0 2px 16px rgba(0,0,0,0.3) !important;
        }
        div[data-testid="stPlotlyChart"]:hover {
            box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
        }

        .stSelectbox, .stSlider {
            background: #1a1d2e !important;
            box-shadow: 0 1px 8px rgba(0,0,0,0.2) !important;
        }
        .stSelectbox label, .stSlider label {
            color: #c0caf5 !important;
        }
        .stSelectbox > div > div,
        .stSelectbox [data-baseweb="select"] > div {
            background: #252838 !important;
            border-color: #3a3e55 !important;
            color: #c0caf5 !important;
        }
        .stSelectbox [data-baseweb="select"] > div:hover {
            border-color: #565b7a !important;
        }

        .streamlit-expanderHeader {
            background: #1e2132 !important;
            border-color: #2d3250 !important;
            color: #c0caf5 !important;
        }
        .streamlit-expanderHeader:hover {
            background: #252838 !important;
        }

        .stAlert {
            background: #1a1d2e !important;
            color: #c0caf5 !important;
            border: 1px solid #2d3250 !important;
        }
        .stAlert strong, .stAlert span {
            color: #c0caf5 !important;
        }
        /* Заголовок дашборда (зелёный градиент → тёмный) */
        div[style*="background: linear-gradient(135deg, #c5dfc8"] {
            background: linear-gradient(135deg, #1a1d2e, #252838) !important;
            border-bottom-color: rgba(192,202,245,0.1) !important;
        }
        div[style*="background: linear-gradient(135deg, #e8f2e8"],
        div[style*="background: linear-gradient(135deg, #e8efe8"],
        div[style*="background: linear-gradient(135deg, #edf2ed"] {
            background: linear-gradient(135deg, #1e2132, #252838) !important;
        }
        div[style*="border-left: 4px solid #7da07d"],
        div[style*="border-left: 4px solid #7d9a7d"],
        div[style*="border-left: 4px solid #8fa68f"] {
            border-left-color: #565b7a !important;
        }
        div[style*="color: #2d3e2d"] {
            color: #c0caf5 !important;
        }

        .stDataFrame {
            background: #1a1d2e !important;
            box-shadow: 0 1px 8px rgba(0,0,0,0.2) !important;
        }
        .stDataFrame table, .stDataFrame th, .stDataFrame td {
            background: #1a1d2e !important;
            color: #c0caf5 !important;
            border-color: #2d3250 !important;
        }
        .stDataFrame th {
            background: #252838 !important;
        }
        .stDataFrame tr:nth-child(even) td {
            background: #1e2132 !important;
        }

        .stCaption {
            color: #7a7f9a !important;
        }

        input, textarea {
            background: #252838 !important;
            color: #c0caf5 !important;
            border-color: #3a3e55 !important;
        }

        button, [data-baseweb="button"] {
            background: #2d3250 !important;
            color: #c0caf5 !important;
            border-color: #3a3e55 !important;
        }
        button:hover, [data-baseweb="button"]:hover {
            background: #3b3f5c !important;
        }

        [data-baseweb="menu"], [role="listbox"] {
            background: #1e2132 !important;
            border-color: #3a3e55 !important;
        }
        [data-baseweb="menu"] [role="option"] {
            color: #c0caf5 !important;
        }
        [data-baseweb="menu"] [role="option"]:hover {
            background: #252838 !important;
        }

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f1117;
        }
        ::-webkit-scrollbar-thumb {
            background: #3a3e55;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #565b7a;
        }

        .st-bd, .st-be, .st-bg, .st-cf, .st-cg, .st-ch, .st-ci, .st-cj,
        .st-bx, .st-bw, .st-bv, .st-bu, .st-bt, .st-bs, .st-br, .st-bq {
            background-color: transparent !important;
            color: inherit !important;
        }
        .st-at, .st-au, .st-aw, .st-ax, .st-ay, .st-az, .st-b0, .st-b1 {
            color: #c0caf5 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background: linear-gradient(135deg, #c5dfc8 0%, #b8d4ba 100%);
    color: #2d3e2d;
    padding: 20px 30px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(181,199,175,0.3);
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 3px solid rgba(45,62,45,0.08);
">
    <div style="
        background: rgba(45,62,45,0.08);
        border-radius: 12px;
        padding: 8px 12px;
        font-size: 26px;
    ">📊</div>
    <div>
        <div style="font-size: 23px; font-weight: 700; letter-spacing: 0.3px; line-height: 1.3;">
            Маркетинговая аналитика
        </div>
        <div style="font-size: 13px; opacity: 0.6; letter-spacing: 0.3px; margin-top: 2px;">
            ClickHouse · Streamlit · Plotly
        </div>
    </div>
    <div style="margin-left: auto; font-size: 12px; opacity: 0.5; text-align: right; line-height: 1.5;">
        made by<br>PolinaGitHit
    </div>
</div>
""", unsafe_allow_html=True)

db_name = "marketing"


def _query_df(sql_name: str, **replacements: str) -> "pd.DataFrame":
    """Выполняет SQL-запрос через новый клиент (свой на каждый вызов).
    Streamlit рендерит табы в параллельных потоках — синглтон-клиент не подходит."""
    client = clickhouse_connect.get_client(
        host=settings.clickhouse_host,
        port=settings.clickhouse_port,
        username=settings.clickhouse_user,
        password=settings.clickhouse_password,
    )
    sql = load_query(AVAILABLE_QUERIES[sql_name]).replace("{db}", db_name)
    for k, v in replacements.items():
        sql = sql.replace("{" + k + "}", v)
    return client.query_df(sql)


@st.cache_resource
def _check_connection() -> bool:
    try:
        client = clickhouse_connect.get_client(
            host=settings.clickhouse_host,
            port=settings.clickhouse_port,
            username=settings.clickhouse_user,
            password=settings.clickhouse_password,
        )
        client.query("SELECT 1")
        return True
    except Exception:
        return False


if not _check_connection():
    st.error("ClickHouse недоступен. Запустите `docker compose up`.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs([
    "CTR & CPA",
    "Динамика",
    "Когорты",
    "Регионы",
])

# ─────────────────────── Tab 1: CTR & CPA ───────────────────────
with tab1:
    st.subheader("Матрица эффективности кампаний")

    df_summary = _query_df("campaign_summary")
    st.plotly_chart(
        campaign_efficiency_scatter(df_summary),
        width='stretch',
    )

    st.markdown("""<div style="background: linear-gradient(135deg, #e8f2e8, #d4e5d4); border-radius: 10px; padding: 14px 18px; margin: 8px 0; border-left: 4px solid #7da07d;">
      <strong>🧭 Как читать:</strong> CTR vs CPA — лучшие кампании в <strong>верхнем левом углу</strong> (высокий CTR, низкий CPA).
      Размер пузырька = общий расход в рублях.
    </div>""", unsafe_allow_html=True)

    st.subheader("Структура расходов")
    df_groups = _query_df("group_efficiency")
    st.plotly_chart(
        campaign_sunburst(df_groups),
        width='stretch',
    )

    st.subheader("CTR по месяцам")
    df_ctr_monthly = _query_df("ctr_by_month")
    st.plotly_chart(
        ctr_monthly_line(df_ctr_monthly),
        width='stretch',
    )

    with st.expander("Сводная таблица по кампаниям"):
        st.markdown("""<div style="background: linear-gradient(135deg, #e8efe8, #d6e2d6); border-radius: 10px; padding: 14px 18px; margin: 8px 0; border-left: 4px solid #7d9a7d;">
          <strong>📊 Что это значит:</strong> Все кампании отсортированы по расходам (убывание).
          <strong>Чем ниже CPA</strong> — тем эффективнее кампания, <strong>чем выше CTR</strong> — тем лучше вовлечение.
        </div>""", unsafe_allow_html=True)
        df_campaigns_display = df_summary.copy()
        df_campaigns_display.columns = [
            "Кампания",
            "CTR, %",
            "CPA, руб",
            "Расход, руб",
            "Клики",
            "Показы",
            "Конверсии",
        ]
        st.dataframe(
            df_campaigns_display,
            column_config={
                "CTR, %": st.column_config.NumberColumn(format="%.2f"),
                "CPA, руб": st.column_config.NumberColumn(format="%.2f"),
                "Расход, руб": st.column_config.NumberColumn(format="%d"),
                "Клики": st.column_config.NumberColumn(format="%d"),
                "Показы": st.column_config.NumberColumn(format="%d"),
                "Конверсии": st.column_config.NumberColumn(format="%d"),
            },
            width='stretch',
        )

# ─────────────────────── Tab 2: Динамика ───────────────────────
with tab2:
    # ── Блок 1: По месяцам ──
    st.subheader("По месяцам")

    df_monthly = _query_df("monthly_metrics")

    if not df_monthly.empty:
        df_monthly["month"] = pd.to_datetime(df_monthly["month"])

        monthly_metrics = st.multiselect(
            "Метрики",
            options=[
                "Расход", "Клики", "Показы", "Конверсии", "CTR", "CPA",
            ],
            default=["Расход", "Клики"],
        )

        fig_monthly = monthly_bar(df_monthly, monthly_metrics)
        st.plotly_chart(fig_monthly, width='stretch')
    else:
        st.info("Нет данных для месячной агрегации.")

    st.markdown("<hr style='margin: 20px 0; opacity: 0.2;'>", unsafe_allow_html=True)

    # ── Блок 2: По дням ──
    st.subheader("По дням")

    df_daily = _query_df("daily_metrics")

    if not df_daily.empty:
        df_daily["event_date"] = pd.to_datetime(df_daily["event_date"])
        date_min = df_daily["event_date"].min().date()
        date_max = df_daily["event_date"].max().date()

        # Селектор кампании
        df_campaigns = _query_df("campaign_summary")
        campaign_names = df_campaigns["campaign_name"].tolist()
        selected_campaign = st.selectbox(
            "Кампания",
            options=["Все кампании"] + campaign_names,
            index=0,
        )

        col_f1, col_f2 = st.columns([1, 3])
        with col_f1:
            daily_metric = st.selectbox(
                "Метрика",
                options=["все", "Расход", "Клики", "Конверсии", "CTR"],
                index=1,
            )
        with col_f2:
            date_range = st.slider(
                "Диапазон дат",
                min_value=date_min,
                max_value=date_max,
                value=(date_min, date_max),
                format="YYYY-MM-DD",
            )

        # Фильтр по дате
        mask = (df_daily["event_date"].dt.date >= date_range[0]) & (
            df_daily["event_date"].dt.date <= date_range[1]
        )

        # Фильтр по кампании
        if selected_campaign != "Все кампании":
            df_campaign_daily = _query_df(
                "daily_by_campaign", campaign_name=selected_campaign
            )
            df_campaign_daily["event_date"] = pd.to_datetime(
                df_campaign_daily["event_date"]
            )
            cmask = (df_campaign_daily["event_date"].dt.date >= date_range[0]) & (
                df_campaign_daily["event_date"].dt.date <= date_range[1]
            )
            df_filtered = df_campaign_daily[cmask].copy()
        else:
            df_filtered = df_daily[mask].copy()

        if not df_filtered.empty:
            match daily_metric:
                case "Расход":
                    df_plot = df_filtered[["event_date", "total_cost"]].copy()
                    df_plot.rename(
                        columns={"total_cost": "Расход, руб"}, inplace=True
                    )
                    fig = px.line(
                        df_plot,
                        x="event_date",
                        y="Расход, руб",
                        title="Расходы по дням",
                        template="plotly_white",
                    )
                    fig.update_xaxes(rangeslider_visible=True)
                    fig.update_layout(
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        height=500,
                        margin=dict(l=70, r=30, t=50, b=60),
                        title_x=0.5,
                    )
                case "Клики":
                    df_plot = df_filtered[["event_date", "total_clicks"]].copy()
                    df_plot.rename(columns={"total_clicks": "Клики"}, inplace=True)
                    fig = px.line(
                        df_plot,
                        x="event_date",
                        y="Клики",
                        title="Клики по дням",
                        template="plotly_white",
                    )
                    fig.update_xaxes(rangeslider_visible=True)
                    fig.update_layout(
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        height=500,
                        margin=dict(l=70, r=30, t=50, b=60),
                        title_x=0.5,
                    )
                case "Конверсии":
                    df_plot = df_filtered[
                        ["event_date", "total_conversions"]
                    ].copy()
                    df_plot.rename(
                        columns={"total_conversions": "Конверсии"}, inplace=True
                    )
                    fig = px.line(
                        df_plot,
                        x="event_date",
                        y="Конверсии",
                        title="Конверсии по дням",
                        template="plotly_white",
                    )
                    fig.update_xaxes(rangeslider_visible=True)
                    fig.update_layout(
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        height=500,
                        margin=dict(l=70, r=30, t=50, b=60),
                        title_x=0.5,
                    )
                case "CTR":
                    df_plot = df_filtered[["event_date", "avg_ctr"]].copy()
                    df_plot.rename(columns={"avg_ctr": "CTR, %"}, inplace=True)
                    fig = px.line(
                        df_plot,
                        x="event_date",
                        y="CTR, %",
                        title="CTR по дням",
                        template="plotly_white",
                    )
                    fig.update_xaxes(rangeslider_visible=True)
                    fig.update_layout(
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        height=500,
                        margin=dict(l=70, r=30, t=50, b=60),
                        title_x=0.5,
                    )
                case _:
                    fig = daily_line_enhanced(df_filtered)

            st.plotly_chart(fig, width='stretch')

            with st.expander("Исходные данные (таблица)"):
                st.dataframe(df_filtered, width='stretch')
        else:
            st.info("Нет данных за выбранный период.")
    else:
        st.info("Нет данных для дневной агрегации.")

# ─────────────────────── Tab 3: Когорты ───────────────────────
with tab3:
    st.subheader("Когортная матрица удержания кампаний")

    try:
        build_cohorts()
        df_retention = retention_matrix_df()

        if not df_retention.empty:
            st.plotly_chart(cohort_heatmap(df_retention), width='stretch')

            st.markdown("""<div style="background: linear-gradient(135deg, #edf2ed, #dfe7df); border-radius: 10px; padding: 14px 18px; margin: 8px 0; border-left: 4px solid #8fa68f;">
              <strong>📈 Когортная матрица удержания</strong><br>
              • <strong>Строки</strong> — неделя первого появления кампании (когорта).<br>
              • <strong>Столбцы</strong> — номер недели после старта (0 = первая неделя).<br>
              • <strong>Цвет / число</strong> — процент кампаний когорты, которые всё ещё активны.<br>
              • Чем правее зелёный цвет, тем лучше удержание.
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Когортные данные пока пусты — сначала запустите `make pipeline`.")
    except Exception as e:
        st.error(f"Не удалось построить когорты: {e}")

    st.subheader("Тепловая карта: дни недели × кампании")

    df_dow = _query_df("weekday_distribution")
    if not df_dow.empty:
        st.plotly_chart(weekday_heatmap(df_dow), width='stretch')
    else:
        st.info("Нет данных для тепловой карты.")

# ─────────────────────── Tab 4: Регионы ───────────────────────
with tab4:
    st.subheader("Топ регионов по расходам")

    df_regions = _query_df("top_regions")

    if not df_regions.empty:
        top_n = st.slider("Сколько регионов показать", min_value=5, max_value=15, value=10)

        st.plotly_chart(regions_treemap(df_regions.head(top_n)), width='stretch')

        with st.expander("Таблица по регионам"):
            df_regions_display = df_regions.head(top_n).copy()
            df_regions_display.columns = [
                "Регион",
                "Расход, руб",
                "Клики",
                "Показы",
                "Конверсии",
                "CTR, %",
            ]
            st.dataframe(
                df_regions_display,
                column_config={
                    "Расход, руб": st.column_config.NumberColumn(format="%d"),
                    "Клики": st.column_config.NumberColumn(format="%d"),
                    "Показы": st.column_config.NumberColumn(format="%d"),
                    "CTR, %": st.column_config.NumberColumn(format="%.2f"),
                },
                width='stretch',
            )
    else:
        st.info("Нет данных по регионам.")