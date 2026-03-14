import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image, ImageDraw, ImageFont
import io

# ─────────────────────────────────────────────
#  FAVICON  –  Orange "S" on dark background
# ─────────────────────────────────────────────
def make_favicon() -> Image.Image:
    size = 64
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Orange rounded-square background
    r = 14
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=r,
                            fill=(252, 128, 25, 255))

    # Try to load a bold system font; fall back gracefully
    font_size = 44
    font = None
    for candidate in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:/Windows/Fonts/arialbd.ttf",
    ]:
        try:
            font = ImageFont.truetype(candidate, font_size)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    # Draw white "S" centred
    bbox = draw.textbbox((0, 0), "S", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1] - 2
    draw.text((x, y), "S", fill=(255, 255, 255, 255), font=font)
    return img

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Swiggy Sales Analysis",
    page_icon=make_favicon(),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  SWIGGY PIN LOGO  (SVG — matches the real logo)
# ─────────────────────────────────────────────
SWIGGY_LOGO_SVG = """
<svg height="72" viewBox="-7.3 3.6 2520.1 3702.8" width="49" xmlns="http://www.w3.org/2000/svg">
  <path d="m1255.2 3706.3c-2.4-1.7-5-4-7.8-6.3-44.6-55.3-320.5-400.9-601.6-844.2-84.4-141.2-139.1-251.4-128.5-279.9 27.5-74.1 517.6-114.7 668.5-47.5 45.9 20.4 44.7 47.3 44.7 63.1 0 67.8-3.3 249.8-3.3 249.8 0 37.6 30.5 68.1 68.2 68 37.7 0 68.1-30.7 68-68.4l-.7-453.3h-.1c0-39.4-43-49.2-51-50.8-78.8-.5-238.7-.9-410.5-.9-379 0-463.8 15.6-528-26.6-139.5-91.2-367.6-706-372.9-1052-7.5-488 281.5-910.5 688.7-1119.8 170-85.6 362-133.9 565-133.9 644.4 0 1175.2 486.4 1245.8 1112.3 0 .5 0 1.2.1 1.7 13 151.3-820.9 183.4-985.8 139.4-25.3-6.7-31.7-32.7-31.7-43.8-.1-115-.9-438.8-.9-438.8-.1-37.7-30.7-68.1-68.4-68.1-37.6 0-68.1 30.7-68.1 68.4l1.5 596.4c1.2 37.6 32.7 47.7 41.4 49.5 93.8 0 313.1-.1 517.4-.1 276.1 0 392.1 32 469.3 90.7 51.3 39.1 71.1 114 53.8 211.4-154.9 866-1135.9 1939.1-1172.8 1983.8z" fill="#fc8019"/>
</svg>
"""

# ─────────────────────────────────────────────
#  FOOD IMAGES  – loaded from food_icons/ folder
# ─────────────────────────────────────────────
import base64, pathlib

def _img_b64(name: str) -> str:
    path = pathlib.Path(__file__).parent / "food_icons" / f"{name}.png"
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()

FOOD_IMAGES = {
    "Biryani":      _img_b64("biryani"),
    "South Indian": _img_b64("south_indian"),
    "North Indian": _img_b64("north_indian"),
    "Desserts":     _img_b64("desserts"),
    "Pizza":        _img_b64("pizza"),
    "Salads":       _img_b64("salads"),
}

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&family=Space+Grotesk:wght@400;500;700&display=swap');

:root {
    --orange:  #FC8019;
    --orange2: #FF6B35;
    --dark:    #1A1A2E;
    --card-bg: #16213E;
    --card2:   #0F3460;
    --text:    #E0E0E0;
    --muted:   #9A9AB0;
    --white:   #FFFFFF;
    --green:   #60D394;
    --yellow:  #FFD166;
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}
.stApp { background: linear-gradient(135deg, #1A1A2E 0%, #16213E 60%, #0F3460 100%); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

/* ── HERO ── */
.hero {
    background: linear-gradient(120deg, #1A1A2E 0%, #16213E 45%, #0F3460 100%);
    border: 1px solid rgba(252,128,25,0.35);
    border-radius: 20px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.55);
    display: flex;
    align-items: center;
    gap: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 80% 50%, rgba(252,128,25,0.07) 0%, transparent 70%);
    pointer-events: none;
}

.hero-logo { flex-shrink: 0; line-height: 0; }

.hero-brand {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.hero-brand .brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--orange);
    letter-spacing: 3px;
    text-transform: uppercase;
    line-height: 1;
    margin-bottom: 4px;
}
.hero-brand .brand-tag {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.1;
}
.hero-brand .brand-sub {
    font-size: 0.95rem;
    color: var(--muted);
    margin-top: 0.35rem;
}

.hero-divider {
    width: 1px;
    height: 70px;
    background: rgba(252,128,25,0.3);
    flex-shrink: 0;
    margin: 0 1rem;
}

/* food icons – stretch full remaining width */
.hero-icons {
    display: flex;
    flex: 1;
    justify-content: space-evenly;
    align-items: center;
    padding: 0 0.5rem;
}
.food-icon {
    width: 62px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;
}
.fi-img {
    width: 55px;
    height: 55px;
    object-fit: cover;
    border-radius: 50%;
    border: 2.5px solid rgba(252,128,25,0.6);
    box-shadow: 0 4px 14px rgba(0,0,0,0.5);
    display: block;
}
.fi-label {
    font-size: 0.55rem;
    font-weight: 700;
    color: #FC8019;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: center;
    line-height: 1.3;
    font-family: 'Space Grotesk', sans-serif;
    white-space: nowrap;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--orange);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 1.8rem 0 0.9rem;
    padding-left: 10px;
    border-left: 4px solid var(--orange);
}

/* ── KPI CARDS ── */
.kpi-card {
    background: linear-gradient(145deg, #1e2d50, #16213E);
    border: 1px solid rgba(252,128,25,0.22);
    border-radius: 16px;
    padding: 1.3rem 1.4rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    border-radius: 16px 16px 0 0;
    background: linear-gradient(90deg, var(--orange), var(--orange2));
}
.kpi-icon  { font-size: 1.9rem; margin-bottom: 0.3rem; }
.kpi-label { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.kpi-value { font-family: 'Space Grotesk', sans-serif; font-size: 1.75rem; font-weight: 700; color: var(--white); margin: 0.15rem 0; line-height: 1; }
.kpi-sub   { font-size: 0.7rem; color: var(--green); font-weight: 600; }

/* ── QUARTERLY TABLE ── */
.qt-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.qt-table th {
    background: rgba(252,128,25,0.18);
    color: var(--orange);
    text-align: center;
    padding: 10px 12px;
    font-weight: 700;
    border-bottom: 2px solid rgba(252,128,25,0.3);
}
.qt-table td {
    text-align: center;
    padding: 9px 12px;
    color: var(--text);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.qt-table tr:hover td { background: rgba(252,128,25,0.07); }

/* ── FOOTER ── */
.dash-footer {
    text-align: center;
    padding: 1.4rem;
    color: var(--muted);
    font-size: 0.78rem;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLOTLY DEFAULTS
# ─────────────────────────────────────────────
PLOT_BG    = "rgba(0,0,0,0)"
PAPER_BG   = "rgba(0,0,0,0)"
FONT_COLOR = "#E0E0E0"
ORANGE     = "#FC8019"
ORANGE2    = "#FF6B35"
GRID_COLOR = "rgba(255,255,255,0.06)"

def base_layout(**kwargs):
    return dict(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Nunito"),
        margin=dict(t=50, b=40, l=40, r=20),
        **kwargs,
    )

# ─────────────────────────────────────────────
#  DATA LOAD
# ─────────────────────────────────────────────
@st.cache_data
def load_data(file) -> pd.DataFrame:
    df = pd.read_excel(file)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["YearMonth"]  = df["Order Date"].dt.to_period("M").astype(str)
    df["DayName"]    = df["Order Date"].dt.day_name()
    df["Quarter"]    = df["Order Date"].dt.to_period("Q").astype(str)
    non_veg_kw = ["chicken","egg","fish","mutton","prawn","biryani","kabab","kebab","non-veg","non veg"]
    df["Food Category"] = np.where(
        df["Dish Name"].str.lower().str.contains("|".join(non_veg_kw), na=False),
        "Non-Veg", "Veg"
    )
    return df

# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-logo">{SWIGGY_LOGO_SVG}</div>
  <div class="hero-brand">
    <div class="brand-name">Swiggy</div>
    <div class="brand-tag">Sales Analysis</div>
    <div class="brand-sub">Revenue &nbsp;•&nbsp; Ratings &nbsp;•&nbsp; City &amp; Cuisine Insights</div>
  </div>
  <div class="hero-divider"></div>
  <div class="hero-icons">
    <div class="food-icon"><img src="{FOOD_IMAGES['Biryani']}" class="fi-img"/><span class="fi-label">Biryani</span></div>
    <div class="food-icon"><img src="{FOOD_IMAGES['South Indian']}" class="fi-img"/><span class="fi-label">South Indian</span></div>
    <div class="food-icon"><img src="{FOOD_IMAGES['North Indian']}" class="fi-img"/><span class="fi-label">North Indian</span></div>
    <div class="food-icon"><img src="{FOOD_IMAGES['Desserts']}" class="fi-img"/><span class="fi-label">Desserts</span></div>
    <div class="food-icon"><img src="{FOOD_IMAGES['Pizza']}" class="fi-img"/><span class="fi-label">Pizza</span></div>
    <div class="food-icon"><img src="{FOOD_IMAGES['Salads']}" class="fi-img"/><span class="fi-label">Salads</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FILE UPLOADER
# ─────────────────────────────────────────────
uploaded = st.file_uploader(
    "📂  Upload your Swiggy Excel file to begin",
    type=["xlsx", "xls"],
    label_visibility="visible",
)
if uploaded is None:
    st.info("👆  Please upload your **swiggy_data.xlsx** file to load the dashboard.")
    st.stop()

df = load_data(uploaded)

# ─────────────────────────────────────────────
#  SLICERS
# ─────────────────────────────────────────────
all_states = sorted(df["State"].dropna().unique().tolist())

st.markdown('<div class="section-title">🔍 Filters</div>', unsafe_allow_html=True)
sl1, sl2 = st.columns(2)

with sl1:
    st.markdown('<p style="color:#FC8019;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">🗺️ Select State(s)</p>', unsafe_allow_html=True)
    sel_states = st.multiselect(
        label="state_filter", options=all_states, default=[],
        placeholder="All States — select to filter…",
        label_visibility="collapsed",
    )

city_pool = (
    sorted(df[df["State"].isin(sel_states)]["City"].dropna().unique().tolist())
    if sel_states else sorted(df["City"].dropna().unique().tolist())
)
with sl2:
    st.markdown('<p style="color:#FC8019;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">🏙️ Select City / Cities</p>', unsafe_allow_html=True)
    sel_cities = st.multiselect(
        label="city_filter", options=city_pool, default=[],
        placeholder="All Cities — select to filter…",
        label_visibility="collapsed",
    )

dff = df.copy()
if sel_states: dff = dff[dff["State"].isin(sel_states)]
if sel_cities: dff = dff[dff["City"].isin(sel_cities)]

if dff.empty:
    st.warning("⚠️ No data matches your selection. Please adjust the filters.")
    st.stop()

active = []
if sel_states: active.append(f"States: {', '.join(sel_states)}")
if sel_cities: active.append(f"Cities: {', '.join(sel_cities)}")
if active:
    st.markdown(
        f'<p style="color:#60D394;font-size:0.8rem;margin-top:-0.4rem">'
        f'✅ Active filters: {" &nbsp;|&nbsp; ".join(active)} &nbsp;— <b>{len(dff):,}</b> records</p>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────────
total_sales  = dff["Price (INR)"].sum()
avg_rating   = dff["Rating"].mean()
avg_order    = dff["Price (INR)"].mean()
rating_count = dff["Rating Count"].sum()
total_orders = len(dff)

st.markdown('<div class="section-title">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, "💰", "Total Revenue",   f"₹{total_sales/1e6:.2f}M", "All-time GMV"),
    (k2, "⭐", "Avg Rating",      f"{avg_rating:.1f} / 5",     "Customer satisfaction"),
    (k3, "🛒", "Avg Order Value", f"₹{avg_order:.0f}",         "Per transaction"),
    (k4, "🗳️",  "Total Ratings",  f"{int(rating_count):,}",    "Cumulative votes"),
    (k5, "📦", "Total Orders",   f"{total_orders:,}",          "Rows in dataset"),
]
for col, icon, label, value, sub in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ROW 1 – Monthly | Daily
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Sales Trends</div>', unsafe_allow_html=True)
c1, c2 = st.columns([3, 2])

with c1:
    monthly = dff.groupby("YearMonth")["Price (INR)"].sum().reset_index()
    fig_m = go.Figure()
    fig_m.add_trace(go.Scatter(
        x=monthly["YearMonth"], y=monthly["Price (INR)"],
        mode="lines+markers",
        line=dict(color=ORANGE, width=3),
        marker=dict(size=8, color=ORANGE2, line=dict(color="#fff", width=1.5)),
        fill="tozeroy", fillcolor="rgba(252,128,25,0.12)", name="Revenue",
    ))
    fig_m.update_layout(
        **base_layout(title=dict(text="📅 Monthly Revenue Trend", font=dict(size=14, color=ORANGE))),
        xaxis=dict(tickangle=-40, showgrid=False, color=FONT_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR,
                   tickprefix="₹", tickformat=".2s"),
        height=320,
    )
    st.plotly_chart(fig_m, use_container_width=True)

with c2:
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    daily = dff.groupby("DayName")["Price (INR)"].sum().reindex(day_order).reset_index()
    fig_d = px.bar(
        daily, x="DayName", y="Price (INR)",
        color="Price (INR)",
        color_continuous_scale=[[0,"#0F3460"],[0.5,ORANGE2],[1,ORANGE]],
        labels={"DayName":"Day","Price (INR)":"Revenue (INR)"},
    )
    fig_d.update_traces(marker_line_width=0)
    fig_d.update_layout(
        **base_layout(title=dict(text="📆 Daily Revenue Pattern", font=dict(size=14, color=ORANGE))),
        xaxis=dict(tickangle=-30, showgrid=False, color=FONT_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR,
                   tickprefix="₹", tickformat=".2s"),
        coloraxis_showscale=False, height=320,
    )
    st.plotly_chart(fig_d, use_container_width=True)

# ─────────────────────────────────────────────
#  ROW 2 – Veg/Non-Veg | Top 5 Cities
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🍽️ Cuisine & City Breakdown</div>', unsafe_allow_html=True)
c3, c4 = st.columns([2, 3])

with c3:
    food_rev = dff.groupby("Food Category")["Price (INR)"].sum().reset_index()
    # Map labels to emoji-rich display names
    food_rev["Label"] = food_rev["Food Category"].map({
        "Veg":     "🟢 Veg",
        "Non-Veg": "🍗 Non-Veg",
    })
    fig_pie = px.pie(
        food_rev, values="Price (INR)", names="Label", hole=0.55,
        color="Label",
        color_discrete_map={"🟢 Veg":"#60D394","🍗 Non-Veg":ORANGE},
    )
    fig_pie.update_traces(
        textinfo="percent+label", pull=[0.06, 0],
        marker=dict(line=dict(color="#16213E", width=3)),
        textfont=dict(size=13),
    )
    fig_pie.update_layout(
        **base_layout(title=dict(text="🥗 Veg  vs  🍗 Non-Veg Revenue", font=dict(size=14, color=ORANGE))),
        legend=dict(font=dict(color=FONT_COLOR, size=13)), height=320,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c4:
    top5 = dff.groupby("City")["Price (INR)"].sum().nlargest(5).sort_values().reset_index()
    fig_city = px.bar(
        top5, x="Price (INR)", y="City", orientation="h",
        color="Price (INR)",
        color_continuous_scale=[[0,ORANGE2],[1,"#FFD166"]],
        text="Price (INR)",
    )
    fig_city.update_traces(texttemplate="₹%{x:,.0f}", textposition="outside", marker_line_width=0)
    fig_city.update_layout(
        **base_layout(title=dict(text="🏙️ Top 5 Cities by Revenue", font=dict(size=14, color=ORANGE))),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR,
                   tickprefix="₹", tickformat=".2s"),
        yaxis=dict(showgrid=False, color=FONT_COLOR),
        coloraxis_showscale=False, height=320,
    )
    st.plotly_chart(fig_city, use_container_width=True)

# ─────────────────────────────────────────────
#  ROW 3 – Revenue by State
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🗺️ State-wise Revenue</div>', unsafe_allow_html=True)
state_rev = (dff.groupby("State", as_index=False)["Price (INR)"].sum()
               .sort_values("Price (INR)", ascending=True))
fig_state = px.bar(
    state_rev, x="Price (INR)", y="State", orientation="h",
    color="Price (INR)",
    color_continuous_scale=[[0,"#0F3460"],[0.5,ORANGE2],[1,"#FFD166"]],
    text="Price (INR)",
)
fig_state.update_traces(texttemplate="₹%{x:,.0f}", textposition="outside", marker_line_width=0)
fig_state.update_layout(
    **base_layout(title=dict(text="Revenue by State (INR)", font=dict(size=14, color=ORANGE))),
    xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR,
               tickprefix="₹", tickformat=".2s"),
    yaxis=dict(showgrid=False, color=FONT_COLOR),
    coloraxis_showscale=False,
    height=max(400, len(state_rev) * 32),
)
st.plotly_chart(fig_state, use_container_width=True)

# ─────────────────────────────────────────────
#  ROW 4 – Quarterly Summary
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Quarterly Performance Summary</div>', unsafe_allow_html=True)
quarterly = (
    dff.groupby("Quarter")
       .agg(Revenue=("Price (INR)","sum"),
            Avg_Rating=("Rating","mean"),
            Total_Orders=("Quarter","count"))
       .reset_index().sort_values("Quarter")
)
quarterly["Avg_Rating"]   = quarterly["Avg_Rating"].round(2)
quarterly["Revenue_Fmt"]  = quarterly["Revenue"].apply(lambda x: f"₹{x:,.0f}")
quarterly["Rating_Stars"] = quarterly["Avg_Rating"].apply(lambda r: "⭐" * int(round(r)))

qc1, qc2 = st.columns([3, 2])
with qc1:
    fig_q = make_subplots(specs=[[{"secondary_y": True}]])
    fig_q.add_trace(go.Bar(
        x=quarterly["Quarter"], y=quarterly["Revenue"],
        name="Revenue", marker_color=ORANGE, marker_line_width=0, opacity=0.85,
    ), secondary_y=False)
    fig_q.add_trace(go.Scatter(
        x=quarterly["Quarter"], y=quarterly["Avg_Rating"],
        name="Avg Rating", mode="lines+markers",
        line=dict(color="#60D394", width=2.5), marker=dict(size=8),
    ), secondary_y=True)
    fig_q.update_layout(
        **base_layout(title=dict(text="📊 Quarterly Revenue & Rating", font=dict(size=14, color=ORANGE))),
        legend=dict(font=dict(color=FONT_COLOR), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=False, color=FONT_COLOR), height=300,
    )
    fig_q.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR,
                       tickprefix="₹", tickformat=".2s", secondary_y=False)
    fig_q.update_yaxes(showgrid=False, color="#60D394", range=[0,5],
                       title_text="Rating", secondary_y=True)
    st.plotly_chart(fig_q, use_container_width=True)

with qc2:
    rows_html = ""
    for _, row in quarterly.iterrows():
        rows_html += f"""
        <tr>
            <td><b>{row['Quarter']}</b></td>
            <td>{row['Revenue_Fmt']}</td>
            <td>{row['Avg_Rating']} {row['Rating_Stars']}</td>
            <td>{int(row['Total_Orders']):,}</td>
        </tr>"""
    st.markdown(f"""
    <div style="margin-top:1.5rem">
    <table class="qt-table">
        <thead><tr><th>Quarter</th><th>Revenue</th><th>Rating</th><th>Orders</th></tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="dash-footer">
    {SWIGGY_LOGO_SVG.replace('height="72"','height="22"').replace('width="49"','width="15"')}
    &nbsp; Swiggy Sales Analysis &nbsp;|&nbsp; Built with Streamlit &amp; Plotly
</div>
""", unsafe_allow_html=True)
