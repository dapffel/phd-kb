from datetime import datetime
from pathlib import Path

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


def _chart_html(fig: go.Figure) -> str:
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

    kpis = (
        '<div class="kpi-row">'
        + _kpi_card("סה״כ הנחות", f"{total_discounts:,}")
        + _kpi_card("סכום כולל", f"₪{total_amount:,.0f}")
        + _kpi_card("ממוצע להנחה", f"₪{avg_amount:,.0f}")
        + _kpi_card("פריטים ייחודיים", f"{unique_items:,}")
        + "</div>"
    )
    if date_range:
        kpis += f'<p class="date-range">{date_range}</p>'
    sections.append(kpis)

    # --- By hour ---
    if "hour" in df.columns:
        hourly = df.groupby("hour").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
        ).reindex(range(24), fill_value=0).reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=hourly["hour"], y=hourly["count"], name="מספר הנחות", marker_color="#4a90d9"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=hourly["hour"], y=hourly["total"], name="סכום (₪)", mode="lines+markers",
                       line=dict(color="#e8913a", width=2)),
            secondary_y=True,
        )
        fig.update_layout(title="הנחות לפי שעה", xaxis_title="שעה", height=400,
                          legend=dict(orientation="h", y=-0.15))
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
        fig.add_trace(go.Bar(x=daily["day_name"], y=daily["count"], name="מספר הנחות", marker_color="#4a90d9"))
        fig.add_trace(go.Bar(x=daily["day_name"], y=daily["total"], name="סכום (₪)", marker_color="#e8913a"))
        fig.update_layout(title="הנחות לפי יום בשבוע", barmode="group", height=400,
                          legend=dict(orientation="h", y=-0.15))
        sections.append(_section("ניתוח לפי יום", _chart_html(fig)))

    # --- By waiter ---
    if "waiter" in df.columns:
        waiter = df.groupby("waiter").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
        ).sort_values("total", ascending=True).tail(15).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(x=waiter["total"], y=waiter["waiter"], orientation="h",
                             name="סכום (₪)", marker_color="#4a90d9",
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
                             marker_color="#4a90d9"))
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
                     color_discrete_sequence=px.colors.qualitative.Set2)
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
            go.Bar(x=trend["date"], y=trend["count"], name="מספר הנחות", marker_color="#4a90d9", opacity=0.6),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=trend["date"], y=trend["total"].rolling(7, min_periods=1).mean(),
                       name="ממוצע נע 7 ימים (₪)", mode="lines",
                       line=dict(color="#e8913a", width=2)),
            secondary_y=True,
        )
        fig.update_layout(title="מגמה לאורך זמן", height=400,
                          legend=dict(orientation="h", y=-0.15))
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
            colorscale="YlOrRd",
            colorbar_title="₪",
        ))
        fig.update_layout(title="מפת חום: סכום הנחות לפי יום ושעה", height=350,
                          xaxis_title="שעה", yaxis_title="יום")
        sections.append(_section("מפת חום", _chart_html(fig)))

    # --- Assemble HTML ---
    body = "\n".join(sections)
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<title>דוח הנחות — Lila</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         max-width: 1100px; margin: 0 auto; padding: 20px; background: #f8f9fa; color: #333; }}
  h1 {{ color: #2c3e50; border-bottom: 3px solid #e8913a; padding-bottom: 10px; }}
  h2 {{ color: #34495e; margin-top: 30px; }}
  .kpi-row {{ display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }}
  .kpi {{ background: white; border-radius: 10px; padding: 20px; flex: 1; min-width: 150px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
  .kpi-value {{ font-size: 2em; font-weight: bold; color: #4a90d9; }}
  .kpi-label {{ font-size: 0.9em; color: #666; margin-top: 5px; }}
  .date-range {{ text-align: center; color: #888; font-size: 0.9em; }}
  .section {{ background: white; border-radius: 10px; padding: 20px; margin: 20px 0;
              box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  .footer {{ text-align: center; color: #aaa; font-size: 0.8em; margin-top: 40px; }}
</style>
</head>
<body>
<h1>דוח ניתוח הנחות</h1>
{body}
<div class="footer">נוצר ב-{now} | Lila Analytics</div>
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
