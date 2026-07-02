from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from agents.config import settings

COLUMN_MAP = {
    "סוג": "type",
    "מספר הזמנה": "order_number",
    "שם מנה": "item_name",
    "טלפון לקוח": "customer_phone",
    "נפתחה": "opened_at",
    "הגדרה": "definition",
    "מחיר הזמנה": "order_price",
    "מספר פריטים": "item_count",
    "כרטיס מבוטלים": "cancelled_cards",
    "סטטוס": "status",
    "מלצר": "waiter",
    "מספר שולחן": "table_number",
    "שירות": "service",
    "שירות(סכום)": "service_amount",
    "הנחה": "discount",
    "הנחה(סכום)": "discount_amount",
    "מקור הזמנה": "order_source",
    "סועדים": "diners",
}

HEBREW_LABELS = {v: k for k, v in COLUMN_MAP.items()}

DAY_NAMES_HE = {
    0: "שני", 1: "שלישי", 2: "רביעי", 3: "חמישי",
    4: "שישי", 5: "שבת", 6: "ראשון",
}

DAY_ORDER = [6, 0, 1, 2, 3, 4, 5]


def load_discounts() -> pd.DataFrame:
    discount_dir = settings.raw_dir / "discounts"
    if not discount_dir.exists():
        raise FileNotFoundError(f"No discounts directory: {discount_dir}")

    frames = []
    for path in sorted(discount_dir.glob("*.xlsx")):
        df = pd.read_excel(path, engine="openpyxl")
        df.rename(columns=COLUMN_MAP, inplace=True)
        df["_source"] = path.name
        frames.append(df)

    if not frames:
        raise FileNotFoundError("No .xlsx files found in raw/discounts/")

    df = pd.concat(frames, ignore_index=True)

    if "opened_at" in df.columns:
        df["opened_at"] = pd.to_datetime(df["opened_at"], errors="coerce")
        df["hour"] = df["opened_at"].dt.hour
        df["day_of_week"] = df["opened_at"].dt.dayofweek
        df["day_name"] = df["day_of_week"].map(DAY_NAMES_HE)
        df["date"] = df["opened_at"].dt.date
        df["week"] = df["opened_at"].dt.isocalendar().week.astype(int)
        df["month"] = df["opened_at"].dt.to_period("M").astype(str)

    for col in ["discount_amount", "order_price", "service_amount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "diners" in df.columns:
        df["diners"] = pd.to_numeric(df["diners"], errors="coerce")

    return df


def _section(title: str, *charts: str) -> str:
    cards = "\n".join(charts)
    return f'<div class="section"><h2>{title}</h2>{cards}</div>'


def _kpi_card(label: str, value: str) -> str:
    return f'<div class="kpi"><div class="kpi-value">{value}</div><div class="kpi-label">{label}</div></div>'


CHART_LAYOUT = dict(
    font=dict(family="Rubik, sans-serif", size=13, color="#2d2d2d"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=16, r=16, t=48, b=40),
    legend=dict(orientation="h", y=-0.18, font=dict(size=12)),
    title_font=dict(size=15, color="#1a1a1a"),
)

COLORS = ["#3d3d3d", "#c4704b", "#7a9e7e", "#b8a56a", "#8b7bb5", "#5f9ea0"]


def _chart_html(fig: go.Figure) -> str:
    fig.update_layout(**CHART_LAYOUT)
    return fig.to_html(full_html=False, include_plotlyjs=False)


def build_report(df: pd.DataFrame) -> str:
    sections = []

    # --- KPIs ---
    total_discounts = len(df)
    total_amount = df["discount_amount"].sum() if "discount_amount" in df.columns else 0
    avg_amount = df["discount_amount"].mean() if "discount_amount" in df.columns else 0
    unique_items = df["item_name"].nunique() if "item_name" in df.columns else 0
    date_range = ""
    if "opened_at" in df.columns:
        mn, mx = df["opened_at"].min(), df["opened_at"].max()
        if pd.notna(mn) and pd.notna(mx):
            date_range = f"{mn.strftime('%d/%m/%Y')} — {mx.strftime('%d/%m/%Y')}"

    file_count = df["_source"].nunique()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    meta_items = [f"<span>{file_count} קבצים</span>"]
    if date_range:
        meta_items.append(f"<span>{date_range}</span>")
    meta_items.append(f"<span>נוצר {now}</span>")
    meta_html = (
        '<div class="meta-stripe">'
        + '<div class="meta-inner">' + " · ".join(meta_items) + "</div>"
        + "</div>"
    )

    kpis = (
        '<div class="kpi-row">'
        + _kpi_card("סה״כ הנחות", f"{total_discounts:,}")
        + _kpi_card("סכום כולל", f"₪{total_amount:,.0f}")
        + _kpi_card("ממוצע להנחה", f"₪{avg_amount:,.0f}")
        + _kpi_card("פריטים ייחודיים", f"{unique_items:,}")
        + "</div>"
    )
    sections.append(kpis)

    # --- By hour ---
    if "hour" in df.columns:
        hourly = df.groupby("hour").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
        ).reindex(range(24), fill_value=0).reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=hourly["hour"], y=hourly["count"], name="מספר הנחות", marker_color=COLORS[0]),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=hourly["hour"], y=hourly["total"], name="סכום (₪)", mode="lines+markers",
                       line=dict(color=COLORS[1], width=2)),
            secondary_y=True,
        )
        fig.update_layout(title="הנחות לפי שעה", xaxis_title="שעה", height=400)
        fig.update_yaxes(title_text="מספר", secondary_y=False)
        fig.update_yaxes(title_text="₪", secondary_y=True)
        sections.append(_section("ניתוח לפי שעה", _chart_html(fig)))

    # --- By day of week ---
    if "day_of_week" in df.columns:
        daily = df.groupby("day_of_week").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
            avg=("discount_amount", "mean"),
        ).reindex(DAY_ORDER).reset_index()
        daily["day_name"] = daily["day_of_week"].map(DAY_NAMES_HE)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily["day_name"], y=daily["count"], name="מספר הנחות", marker_color=COLORS[0]))
        fig.add_trace(go.Bar(x=daily["day_name"], y=daily["total"], name="סכום (₪)", marker_color=COLORS[1]))
        fig.update_layout(title="הנחות לפי יום בשבוע", barmode="group", height=400)
        sections.append(_section("ניתוח לפי יום", _chart_html(fig)))

    # --- By waiter ---
    if "waiter" in df.columns:
        waiter = df.groupby("waiter").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
        ).sort_values("total", ascending=True).tail(15).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(x=waiter["total"], y=waiter["waiter"], orientation="h",
                             name="סכום (₪)", marker_color=COLORS[0],
                             text=waiter["count"].apply(lambda x: f"{x} הנחות"),
                             textposition="auto"))
        fig.update_layout(title="הנחות לפי מלצר (טופ 15)", height=max(350, len(waiter) * 30),
                          xaxis_title="₪")
        sections.append(_section("ניתוח לפי מלצר", _chart_html(fig)))

    # --- Top items ---
    if "item_name" in df.columns:
        items = df.groupby("item_name").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
        ).sort_values("count", ascending=False).head(20).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(x=items["item_name"], y=items["count"], name="כמות",
                             marker_color=COLORS[0]))
        fig.update_layout(title="פריטים שניתנו הכי הרבה הנחות (טופ 20)", height=450,
                          xaxis_tickangle=-45)
        sections.append(_section("פריטים מובילים", _chart_html(fig)))

    # --- By discount type/definition ---
    if "definition" in df.columns:
        by_def = df.groupby("definition").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
        ).sort_values("total", ascending=False).reset_index()

        fig = px.pie(by_def, values="total", names="definition", title="סכום הנחות לפי סוג",
                     color_discrete_sequence=COLORS)
        fig.update_layout(height=400)
        sections.append(_section("סוגי הנחות", _chart_html(fig)))

    # --- Trend over time ---
    if "date" in df.columns:
        trend = df.groupby("date").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
        ).reset_index()
        trend["date"] = pd.to_datetime(trend["date"])

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=trend["date"], y=trend["count"], name="מספר הנחות", marker_color=COLORS[0], opacity=0.6),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=trend["date"], y=trend["total"].rolling(7, min_periods=1).mean(),
                       name="ממוצע נע 7 ימים (₪)", mode="lines",
                       line=dict(color=COLORS[1], width=2)),
            secondary_y=True,
        )
        fig.update_layout(title="מגמה לאורך זמן", height=400)
        fig.update_yaxes(title_text="מספר", secondary_y=False)
        fig.update_yaxes(title_text="₪", secondary_y=True)
        sections.append(_section("מגמה לאורך זמן", _chart_html(fig)))

    # --- Heatmap: day x hour ---
    if "hour" in df.columns and "day_of_week" in df.columns:
        heat = df.groupby(["day_of_week", "hour"]).agg(
            total=("discount_amount", "sum"),
        ).reset_index()
        heat_pivot = heat.pivot_table(index="day_of_week", columns="hour", values="total", fill_value=0)
        heat_pivot = heat_pivot.reindex(DAY_ORDER)
        y_labels = [DAY_NAMES_HE[d] for d in DAY_ORDER]

        fig = go.Figure(data=go.Heatmap(
            z=heat_pivot.values,
            x=[str(h) for h in heat_pivot.columns],
            y=y_labels,
            colorscale=[[0, "#f5f5f0"], [0.5, "#c4704b"], [1, "#3d3d3d"]],
            colorbar_title="₪",
        ))
        fig.update_layout(title="מפת חום: סכום הנחות לפי יום ושעה", height=350,
                          xaxis_title="שעה", yaxis_title="יום")
        sections.append(_section("מפת חום", _chart_html(fig)))

    # --- Assemble HTML ---
    content = "\n".join(sections)

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>דוח הנחות — Lila</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Rubik', -apple-system, BlinkMacSystemFont, sans-serif;
    font-weight: 400;
    line-height: 1.6;
    background: #f5f5f0;
    color: #2d2d2d;
    -webkit-font-smoothing: antialiased;
  }}

  .meta-stripe {{
    background: #2d2d2d;
    color: #e8e8e4;
    padding: 14px 0;
    font-size: 0.85em;
    font-weight: 300;
    letter-spacing: 0.02em;
  }}
  .meta-inner {{
    max-width: 1060px;
    margin: 0 auto;
    padding: 0 32px;
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
  }}
  .meta-stripe span {{ opacity: 0.85; }}

  .container {{
    max-width: 1060px;
    margin: 0 auto;
    padding: 48px 32px 60px;
  }}

  h1 {{
    font-size: 1.9em;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 36px;
    letter-spacing: -0.01em;
  }}

  h2 {{
    font-size: 1.1em;
    font-weight: 500;
    color: #1a1a1a;
    letter-spacing: -0.005em;
  }}

  .kpi-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 40px;
  }}

  .kpi {{
    background: #fff;
    border: 1px solid #e8e8e4;
    border-radius: 12px;
    padding: 24px 20px;
    text-align: center;
    transition: box-shadow 0.2s ease;
  }}
  .kpi:hover {{ box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}

  .kpi-value {{
    font-size: 2.2em;
    font-weight: 600;
    color: #1a1a1a;
    line-height: 1.1;
  }}

  .kpi-label {{
    font-size: 0.82em;
    font-weight: 400;
    color: #888;
    margin-top: 8px;
    letter-spacing: 0.01em;
  }}

  .section {{
    background: #fff;
    border: 1px solid #e8e8e4;
    border-radius: 12px;
    padding: 28px 24px;
    margin-bottom: 24px;
    transition: box-shadow 0.2s ease;
  }}
  .section:hover {{ box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}

  .section h2 {{
    border-bottom: 1px solid #f0f0ec;
    padding-bottom: 12px;
    margin-bottom: 20px;
  }}

  .footer {{
    text-align: center;
    color: #b0b0a8;
    font-size: 0.78em;
    font-weight: 300;
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid #e8e8e4;
    letter-spacing: 0.02em;
  }}

  .js-plotly-plot .plotly .modebar {{
    right: unset !important;
    left: 0 !important;
  }}
</style>
</head>
<body>
{meta_html}
<div class="container">
<h1>דוח ניתוח הנחות</h1>
{content}
<div class="footer">Lila Analytics</div>
</div>
</body>
</html>"""


def analyze_discounts() -> str:
    df = load_discounts()
    html = build_report(df)

    out_dir = settings.outputs_dir / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "discount-report.html"
    path.write_text(html, encoding="utf-8")

    return f"Report generated: {path.relative_to(settings.vault_root)} ({len(df)} records from {df['_source'].nunique()} files)"
