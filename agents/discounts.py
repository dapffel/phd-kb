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


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def _section_heading(title: str) -> str:
    return f'<h2>{title}</h2>'


def _panel(*strips: str) -> str:
    inner = "\n".join(strips)
    return f'<div class="panel">{inner}</div>'


def _strip(tag: str, items: list[tuple[str, str]]) -> str:
    cells = "".join(
        f"<div class='item'><span class='k'>{k}</span><span class='v'>{v}</span></div>"
        for k, v in items
    )
    return f"<div class='strip'><span class='strip-tag'>{tag}</span><div class='items'>{cells}</div></div>"


def _chart_card(*charts: str) -> str:
    inner = "\n".join(charts)
    return f'<div class="panel chart-panel">{inner}</div>'


CHART_LAYOUT = dict(
    font=dict(family="Nunito, sans-serif", size=13, color="#1f2937"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=16, r=16, t=48, b=48),
    legend=dict(orientation="h", y=-0.18, font=dict(size=12)),
    title_font=dict(size=15, color="#1f2937", weight=700),
)

COLORS = ["#1f2937", "#d97706", "#16a34a", "#6366f1", "#dc2626", "#94a3b8"]


def _chart_html(fig: go.Figure) -> str:
    fig.update_layout(**CHART_LAYOUT)
    return fig.to_html(full_html=False, include_plotlyjs=False)


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def build_report(df: pd.DataFrame) -> str:
    sections: list[str] = []

    # --- Compute metadata ---
    total_discounts = len(df)
    total_amount = df["discount_amount"].sum() if "discount_amount" in df.columns else 0
    avg_amount = df["discount_amount"].mean() if "discount_amount" in df.columns else 0
    unique_items = df["item_name"].nunique() if "item_name" in df.columns else 0
    unique_waiters = df["waiter"].nunique() if "waiter" in df.columns else 0
    file_count = df["_source"].nunique()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    date_range = ""
    if "opened_at" in df.columns:
        mn, mx = df["opened_at"].min(), df["opened_at"].max()
        if pd.notna(mn) and pd.notna(mx):
            date_range = f"{mn.strftime('%d/%m/%Y')} — {mx.strftime('%d/%m/%Y')}"

    # --- Metadata panel ---
    sections.append(_section_heading("נתוני הרצה"))
    data_items: list[tuple[str, str]] = [("קבצים", str(file_count))]
    if date_range:
        data_items.append(("טווח תאריכים", date_range))
    data_items.append(("נוצר", now))

    sections.append(_panel(
        _strip("נתונים", data_items),
        _strip("סיכום", [
            ("הנחות", f"{total_discounts:,}"),
            ("סכום כולל", f"₪{total_amount:,.0f}"),
            ("ממוצע להנחה", f"₪{avg_amount:,.0f}"),
            ("פריטים", f"{unique_items:,}"),
            ("מלצרים", f"{unique_waiters:,}"),
        ]),
    ))

    # --- Overall ---
    sections.append(_section_heading("סה״כ"))
    sections.append(
        f'<div class="overall">'
        f'<span class="pct">₪{total_amount:,.0f}</span>'
        f'<span class="meta2">{total_discounts:,} הנחות · ממוצע ₪{avg_amount:,.0f}</span>'
        f'</div>'
    )

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
        sections.append(_section_heading("ניתוח לפי שעה"))
        sections.append(_chart_card(_chart_html(fig)))

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
        sections.append(_section_heading("ניתוח לפי יום"))
        sections.append(_chart_card(_chart_html(fig)))

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
        sections.append(_section_heading("ניתוח לפי מלצר"))
        sections.append(_chart_card(_chart_html(fig)))

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
        sections.append(_section_heading("פריטים מובילים"))
        sections.append(_chart_card(_chart_html(fig)))

    # --- By discount type/definition ---
    if "definition" in df.columns:
        by_def = df.groupby("definition").agg(
            count=("order_number", "count"),
            total=("discount_amount", "sum"),
        ).sort_values("total", ascending=False).reset_index()

        fig = px.pie(by_def, values="total", names="definition", title="סכום הנחות לפי סוג",
                     color_discrete_sequence=COLORS)
        fig.update_layout(height=400)
        sections.append(_section_heading("סוגי הנחות"))
        sections.append(_chart_card(_chart_html(fig)))

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
        sections.append(_section_heading("מגמה לאורך זמן"))
        sections.append(_chart_card(_chart_html(fig)))

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
            colorscale=[[0, "#f4f6f9"], [0.5, "#d97706"], [1, "#1f2937"]],
            colorbar_title="₪",
        ))
        fig.update_layout(title="מפת חום: סכום הנחות לפי יום ושעה", height=350,
                          xaxis_title="שעה", yaxis_title="יום")
        sections.append(_section_heading("מפת חום"))
        sections.append(_chart_card(_chart_html(fig)))

    # --- Assemble HTML ---
    content = "\n".join(sections)

    return f"""<!doctype html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>דוח הנחות — Lila</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
:root {{ --ink: #1f2937; --muted: #94a3b8; --line: #e9edf2; --bg: #f4f6f9; --amber: #d97706; }}
* {{ box-sizing: border-box; }}
body {{ font-family: 'Nunito', -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
       margin: 0; color: var(--ink); background: var(--bg); -webkit-font-smoothing: antialiased; }}

header {{ padding: 30px 40px 10px; max-width: 1080px; margin: 0 auto; }}
header h1 {{ margin: 0; font-size: 22px; font-weight: 800; letter-spacing: -.01em; }}
header .sub {{ color: var(--muted); font-size: 13px; font-weight: 600; margin-top: 2px; }}

main {{ padding: 8px 40px 64px; max-width: 1080px; margin: 0 auto; }}

h2 {{ font-size: 12px; text-transform: uppercase; letter-spacing: .08em;
     color: var(--muted); font-weight: 800; margin: 30px 0 12px; }}

.panel {{ background: #fff; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }}
.chart-panel {{ padding: 20px; margin-bottom: 8px; }}
.strip {{ display: flex; align-items: center; gap: 18px; padding: 14px 20px; }}
.strip + .strip {{ border-top: 1px solid var(--line); }}
.strip-tag {{ font-size: 11px; font-weight: 800; text-transform: uppercase;
             letter-spacing: .06em; color: #b3bcc8; min-width: 64px; }}
.items {{ display: flex; flex-wrap: wrap; gap: 28px; }}
.item {{ display: flex; flex-direction: column; gap: 1px; }}
.item .k {{ font-size: 10px; text-transform: uppercase; letter-spacing: .05em;
           color: var(--muted); font-weight: 700; }}
.item .v {{ font-size: 14px; font-weight: 700; }}

.overall {{ display: flex; align-items: baseline; gap: 14px; margin-bottom: 12px; }}
.overall .pct {{ font-size: 44px; font-weight: 800; letter-spacing: -.02em; color: var(--ink); }}
.overall .meta2 {{ color: var(--muted); font-weight: 700; font-size: 14px; }}

.footer {{ text-align: center; color: var(--muted); font-size: 11px; font-weight: 600;
          margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--line); }}

.js-plotly-plot .plotly .modebar {{ right: unset !important; left: 0 !important; }}
</style>
</head>
<body>
<header>
<h1>דוח ניתוח הנחות</h1>
<div class="sub">Lila Analytics</div>
</header>
<main>
{content}
<div class="footer">נוצר {now} · Lila</div>
</main>
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
