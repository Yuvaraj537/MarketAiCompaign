import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Marketing Analyst Investment Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
*, body { font-family: 'Inter', sans-serif !important; }

.stApp { background: #060d1f; color: #e2e8f0; }
.block-container { padding: 0.5rem 1.5rem 2rem 1.5rem !important; }
section[data-testid="stSidebar"] { background: #0a1628 !important; border-right: 1px solid #1e3a5f; }
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* Metric overrides */
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-size: 20px !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* Landing card */
.land-card {
    background: linear-gradient(135deg, #0f2044 0%, #0a1628 50%, #091422 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 40px 30px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 10px;
    position: relative;
    overflow: hidden;
}
.land-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.land-card:hover { border-color: #3b82f6; transform: translateY(-4px); box-shadow: 0 20px 40px rgba(59,130,246,0.2); }
.land-icon { font-size: 52px; margin-bottom: 14px; display: block; }
.land-title { color: white; font-size: 20px; font-weight: 800; margin-bottom: 8px; }
.land-desc { color: #64748b; font-size: 13px; line-height: 1.6; }
.land-badge { display: inline-block; background: #1d4ed8; color: white; border-radius: 20px; padding: 3px 12px; font-size: 11px; font-weight: 700; margin-top: 12px; }

/* Section headers */
.sec-hdr {
    background: linear-gradient(90deg, #1d4ed8 0%, rgba(29,78,216,0.15) 60%, transparent 100%);
    border-left: 4px solid #3b82f6;
    padding: 10px 18px;
    border-radius: 0 10px 10px 0;
    margin: 24px 0 14px 0;
    color: white;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.5px;
}
.sec-hdr2 {
    border-left: 4px solid #8b5cf6;
    background: linear-gradient(90deg, rgba(139,92,246,0.2) 0%, transparent 100%);
    padding: 10px 18px;
    border-radius: 0 10px 10px 0;
    margin: 24px 0 14px 0;
    color: white;
    font-size: 16px;
    font-weight: 800;
}

/* KPI Cards */
.kcard {
    background: linear-gradient(140deg, #0f2044 0%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 16px 14px;
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
}
.kcard-glow { border-color: #3b82f6 !important; box-shadow: 0 0 20px rgba(59,130,246,0.15); }
.kcard-glow2 { border-color: #8b5cf6 !important; box-shadow: 0 0 20px rgba(139,92,246,0.15); }
.kcard-glow3 { border-color: #10b981 !important; box-shadow: 0 0 20px rgba(16,185,129,0.15); }
.kcard-glow4 { border-color: #f59e0b !important; box-shadow: 0 0 20px rgba(245,158,11,0.15); }

.klabel { color: #64748b; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; }
.kval { color: white; font-size: 26px; font-weight: 900; margin: 4px 0; line-height: 1.1; }
.ksub { color: #475569; font-size: 10px; margin: 2px 0 8px 0; }
.ktag { display: inline-block; border-radius: 5px; padding: 2px 7px; font-size: 10px; font-weight: 600; margin: 2px 1px; }
.ktag-b { background: rgba(59,130,246,0.2); color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
.ktag-g { background: rgba(16,185,129,0.2); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }
.ktag-p { background: rgba(139,92,246,0.2); color: #c4b5fd; border: 1px solid rgba(139,92,246,0.3); }
.ktag-o { background: rgba(245,158,11,0.2); color: #fcd34d; border: 1px solid rgba(245,158,11,0.3); }
.ktag-r { background: rgba(239,68,68,0.2); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }

.kdivider { height: 1px; background: linear-gradient(90deg, #1e3a5f, transparent); margin: 8px 0; }
.krow-label { color: #475569; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin: 4px 0 2px 0; }

/* Month row */
.mrow { display: flex; justify-content: space-between; align-items: center; background: #0f1e35; border-radius: 8px; padding: 6px 12px; margin: 3px 0; }
.mrow-label { color: #64748b; font-size: 11px; }
.mrow-val { color: white; font-weight: 700; font-size: 12px; }
.mrow-delta { font-size: 11px; font-weight: 600; }

/* Optional metrics expander */
.opt-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 8px 0; }
.opt-mini { background: #0f1e35; border: 1px solid #1e3a5f; border-radius: 10px; padding: 10px 12px; }
.opt-mlabel { color: #64748b; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.opt-mval { color: white; font-size: 16px; font-weight: 800; margin: 2px 0; }
.opt-msub { color: #475569; font-size: 9px; }

/* Filter pill */
.filter-pill { background: #0f1e35; border: 1px solid #1e3a5f; border-radius: 30px; padding: 6px 16px; font-size: 11px; color: #64748b; display: inline-block; margin: 2px 4px; }
.filter-pill b { color: #93c5fd; }

/* Back button */
.back-btn { background: #0f1e35; border: 1px solid #1e3a5f; border-radius: 8px; padding: 6px 16px; font-size: 12px; color: #93c5fd; cursor: pointer; }

/* Hero banner */
.hero { background: linear-gradient(135deg, #0f2044 0%, #071428 50%, #0a1628 100%); border: 1px solid #1e3a5f; border-radius: 18px; padding: 22px 28px; margin-bottom: 18px; }
.hero-title { color: white; font-size: 28px; font-weight: 900; margin: 0; }
.hero-sub { color: #64748b; font-size: 13px; margin: 4px 0 0 0; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a1628; }
::-webkit-scrollbar-thumb { background: #1d4ed8; border-radius: 10px; }

/* Streamlit overrides */
.stSelectbox label, .stMultiSelect label, .stSlider label { color: #94a3b8 !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 1px; }
div[data-testid="stExpander"] { background: #0a1628 !important; border: 1px solid #1e3a5f !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ─────────────────────────────────────────────
# DATA LOAD
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/compaign_analyst.csv")
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M")
    df["Month_str"] = df["Date"].dt.strftime("%b %Y")
    df["Month_sort"] = df["Date"].dt.to_period("M").astype(str)
    # Duration buckets
    df["Duration_Bucket"] = pd.cut(
        df["Duration"],
        bins=[0, 10, 20, 31],
        labels=["Short (≤10d)", "Medium (11-20d)", "Long (21-30d)"]
    )
    # Duration label for 30min / 1hr context
    df["Duration_Label"] = df["Duration"].apply(
        lambda x: "≤30 Min Equivalent" if x <= 15 else "1 Hr+ Equivalent"
    )
    return df

df = load_data()

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def fmt_ind(val, prefix=""):
    """Format number in Indian style: K / L / Cr"""
    if pd.isna(val):
        return "—"
    val = float(val)
    sign = "-" if val < 0 else ""
    val = abs(val)
    if val >= 1_00_00_000:
        return f"{sign}{prefix}{val/1_00_00_000:.2f} Cr"
    elif val >= 1_00_000:
        return f"{sign}{prefix}{val/1_00_000:.2f} L"
    elif val >= 1_000:
        return f"{sign}{prefix}{val/1_000:.1f} K"
    else:
        return f"{sign}{prefix}{val:,.0f}"

def fmt_pct(val):
    if pd.isna(val): return "—"
    return f"{float(val):.2f}%"

def delta_pct(curr, prev):
    if prev == 0: return 0
    return ((curr - prev) / abs(prev)) * 100

def delta_html(d):
    arrow = "▲" if d >= 0 else "▼"
    color = "#10b981" if d >= 0 else "#ef4444"
    return f'<span style="color:{color};font-size:11px;font-weight:700;">{arrow} {abs(d):.1f}%</span>'

PLOT_CFG = dict(template="plotly_dark", height=230,
                plot_bgcolor="#060d1f", paper_bgcolor="#060d1f")

def slim(fig, title=""):
    fig.update_layout(
        height=230, margin=dict(t=32, b=4, l=4, r=4),
        showlegend=False, plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
        font=dict(color="#94a3b8", size=10),
        title=dict(text=title, font=dict(size=11, color="#94a3b8"), x=0.5)
    )
    fig.update_xaxes(gridcolor="#0f1e35", showgrid=True, tickfont=dict(size=9))
    fig.update_yaxes(gridcolor="#0f1e35", showgrid=True, tickfont=dict(size=9))
    return fig

COLOR_SEQ = ["#3b82f6","#8b5cf6","#10b981","#f59e0b","#ef4444","#06b6d4","#ec4899"]

# ─────────────────────────────────────────────
# KPI CARD BUILDER
# ─────────────────────────────────────────────
def kpi_card(label, val_str, sub, camp_rows, chan_rows, seg_rows,
             dur_rows=None, glow_class="kcard-glow"):
    def tags(rows, cls):
        return "".join(f'<span class="ktag {cls}">{n}: {v}</span>' for n, v in rows)

    dur_html = ""
    if dur_rows:
        dur_html = f'<div class="krow-label">⏱ Duration</div>{tags(dur_rows, "ktag-o")}'

    html = f"""
    <div class="kcard {glow_class}">
      <div class="klabel">{label}</div>
      <div class="kval">{val_str}</div>
      <div class="ksub">{sub}</div>
      <div class="kdivider"></div>
      <div class="krow-label">📢 Campaign</div>
      {tags(camp_rows, "ktag-b")}
      <div class="krow-label">📡 Channel</div>
      {tags(chan_rows, "ktag-g")}
      <div class="krow-label">👥 Segment</div>
      {tags(seg_rows, "ktag-p")}
      {dur_html}
    </div>"""
    return html

def top_rows(col, fdf, n=3, agg="sum", fmt_fn=fmt_ind, prefix=""):
    def _top(grp_col):
        if agg == "sum":
            s = fdf.groupby(grp_col)[col].sum()
        else:
            s = fdf.groupby(grp_col)[col].mean()
        return [(nm, fmt_fn(v) if prefix == "" else fmt_fn(v)) 
                for nm, v in s.sort_values(ascending=False).head(n).items()]
    return _top("Campaign_Type"), _top("Channel_Used"), _top("Customer_Segment"), _top("Duration_Bucket")

# ─────────────────────────────────────────────
# SECTION RENDERER
# ─────────────────────────────────────────────
def render_section(title, col, fdf, agg="sum", fmt_fn=fmt_ind, prefix="",
                   chart_type="bar", glow="kcard-glow", extra_html="",
                   optional_cols=None, month_col=None):
    st.markdown(f'<div class="sec-hdr">{title}</div>', unsafe_allow_html=True)

    if agg == "sum":
        total = fdf[col].sum()
        avg = fdf[col].mean()
    else:
        total = fdf[col].mean()
        avg = fdf[col].std()

    bc, bch, bs, bd = top_rows(col, fdf, agg=agg)

    sub_str = f"Avg: {fmt_fn(avg)}" if agg == "sum" else f"Std: {fmt_fn(avg)}"
    if extra_html:
        sub_str += extra_html

    c1, c2, c3, c4 = st.columns([1.3, 1.1, 1.1, 1.1])

    with c1:
        st.markdown(kpi_card(col.replace("_", " ").title(),
                             fmt_fn(total), sub_str, bc, bch, bs, bd, glow),
                    unsafe_allow_html=True)

        # Month-wise mini table
        if fdf["Date"].notna().any():
            month_data = (
                fdf.dropna(subset=["Date"])
                .groupby("Month_sort")[col]
                .sum() if agg == "sum" else
                fdf.dropna(subset=["Date"]).groupby("Month_sort")[col].mean()
            )
            if len(month_data) >= 2:
                months = sorted(month_data.index)[-4:]  # last 4 months
                rows = ""
                for i, m in enumerate(months):
                    v = month_data[m]
                    prev_v = month_data[months[i - 1]] if i > 0 else v
                    d = delta_pct(v, prev_v) if i > 0 else 0
                    rows += f"""
                    <div class="mrow">
                      <span class="mrow-label">📅 {m}</span>
                      <span class="mrow-val">{fmt_fn(v)}</span>
                      {delta_html(d) if i > 0 else '<span style="color:#475569;font-size:10px;">base</span>'}
                    </div>"""
                st.markdown(f'<div style="margin-top:6px;">{rows}</div>', unsafe_allow_html=True)

    # Chart by Campaign Type
    with c2:
        gdf = (fdf.groupby("Campaign_Type")[col].sum() if agg == "sum"
               else fdf.groupby("Campaign_Type")[col].mean()).reset_index()
        if chart_type == "bar":
            fig = px.bar(gdf, x="Campaign_Type", y=col, color="Campaign_Type",
                         color_discrete_sequence=COLOR_SEQ, title="By Campaign")
        else:
            fig = px.pie(gdf, names="Campaign_Type", values=col,
                         color_discrete_sequence=COLOR_SEQ, hole=0.45, title="By Campaign")
        st.plotly_chart(slim(fig, "By Campaign Type"), use_container_width=True)

    # Chart by Channel
    with c3:
        gdf2 = (fdf.groupby("Channel_Used")[col].sum() if agg == "sum"
                else fdf.groupby("Channel_Used")[col].mean()).reset_index()
        fig2 = px.bar(gdf2, x=col, y="Channel_Used", orientation="h",
                      color="Channel_Used", color_discrete_sequence=COLOR_SEQ, title="By Channel")
        fig2.update_layout(height=230, margin=dict(t=32, b=4, l=4, r=4),
                           showlegend=False, plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                           font=dict(color="#94a3b8", size=9),
                           yaxis=dict(tickfont=dict(size=8)),
                           title=dict(text="By Channel", font=dict(size=11, color="#94a3b8"), x=0.5))
        st.plotly_chart(fig2, use_container_width=True)

    # Chart by Segment + Duration
    with c4:
        gdf3 = fdf.groupby(["Customer_Segment", "Duration_Label"])[col]\
                  .sum().reset_index() if agg == "sum" else \
               fdf.groupby(["Customer_Segment", "Duration_Label"])[col]\
                  .mean().reset_index()
        fig3 = px.bar(gdf3, x="Customer_Segment", y=col, color="Duration_Label",
                      barmode="group", color_discrete_sequence=["#3b82f6","#f59e0b"],
                      title="Segment × Duration")
        st.plotly_chart(slim(fig3, "Segment × Duration"), use_container_width=True)

    # Optional metrics expander
    if optional_cols:
        with st.expander(f"📊 Drill-Down: Additional Metrics for {col}", expanded=False):
            opt_cols = st.columns(4)
            for i, (opt_label, opt_col, opt_fmt) in enumerate(optional_cols):
                with opt_cols[i % 4]:
                    try:
                        ov = fdf[opt_col].sum() if "Cost" in opt_col or "Revenue" in opt_col or "Profit" in opt_col or "RPC" in opt_col else fdf[opt_col].mean()
                        st.markdown(f"""
                        <div class="opt-mini">
                          <div class="opt-mlabel">{opt_label}</div>
                          <div class="opt-mval">{opt_fmt(ov)}</div>
                          <div class="opt-msub">Avg: {opt_fmt(fdf[opt_col].mean())}</div>
                        </div>""", unsafe_allow_html=True)
                    except:
                        pass

# ─────────────────────────────────────────────
# OPTIONAL DRILLDOWN SPEC (shared)
# ─────────────────────────────────────────────
OPTIONALS = [
    ("Ads Cost", "Ads cost", fmt_ind),
    ("Engagement Score", "Engagement_Score", fmt_pct),
    ("Actively Engaged", "Engage of interest(actively  user engaged)", fmt_ind),
    ("Duration Earn", "Duration wise earn", fmt_ind),
    ("CTR", "CTR", fmt_pct),
    ("LCR (People)", "LCR(people)", fmt_pct),
    ("CAC (₹)", "CAC(rupees)", lambda x: fmt_ind(x, "₹")),
    ("RPC (₹)", "RPC(people cR)", lambda x: fmt_ind(x, "₹")),
    ("Revenue", "Revenue", lambda x: fmt_ind(x, "₹")),
    ("Profit", "Profit", lambda x: fmt_ind(x, "₹")),
    ("ROI", "ROI", fmt_pct),
    ("Return Inv. Cost", "Return Of Investment Cost", lambda x: fmt_ind(x, "₹")),
    ("Ret. Inv. Ads", "Return inverstmene ad", fmt_ind),
    ("Month Count", "Date", lambda x: f"{int(x)}"),
]


# ═══════════════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════════════
def landing_page():
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 20px 0;">
        <div style="font-size:60px;">📈</div>
        <h1 style="color:white; font-size:38px; font-weight:900; margin:10px 0 4px 0;">
            Marketing Analyst Investment
        </h1>
        <p style="color:#64748b; font-size:16px; margin:0 0 40px 0;">
            Choose your dashboard to begin deep-dive analytics
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="land-card">
            <span class="land-icon">📊</span>
            <div class="land-title">Internal Analytics Dashboard</div>
            <div class="land-desc">KPI deep-dive with impressions, clicks, leads, conversions, revenue, profit &amp; engagement — broken down by campaign, channel, segment and duration.</div>
            <div class="land-badge">16 KPI Sections · Live Filters</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Open Internal Analytics", key="btn_internal", use_container_width=True):
            st.session_state.page = "internal"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="land-card">
            <span class="land-icon">💰</span>
            <div class="land-title">Investment ROI Dashboard</div>
            <div class="land-desc">Track ROI, Return Investment Cost, Acquisition Cost, CAC, RPC and Profit Margin across all campaigns with month-wise trend analysis.</div>
            <div class="land-badge">Financial KPIs · Month Trends</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Open ROI Dashboard", key="btn_roi", use_container_width=True):
            st.session_state.page = "roi"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="land-card">
            <span class="land-icon">🎯</span>
            <div class="land-title">Engagement Intelligence</div>
            <div class="land-desc">Analyse engagement scores, CTR, LCR, actively engaged users and duration-wise earning patterns across audience segments.</div>
            <div class="land-badge">Engagement · CTR · LCR</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Open Engagement Intel", key="btn_eng", use_container_width=True):
            st.session_state.page = "engagement"
            st.rerun()

    # Dataset snapshot
    st.markdown('<div class="sec-hdr" style="margin-top:40px;">📋 Dataset Snapshot</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Total Records", f"{len(df):,}")
    with c2: st.metric("Campaign Types", df["Campaign_Type"].nunique())
    with c3: st.metric("Channels", df["Channel_Used"].nunique())
    with c4: st.metric("Segments", df["Customer_Segment"].nunique())
    with c5: st.metric("Date Range", f"{df['Date'].min().strftime('%b %y')} → {df['Date'].max().strftime('%b %y')}")

    # Quick charts
    st.markdown('<div class="sec-hdr">📈 Data Overview</div>', unsafe_allow_html=True)
    qc1, qc2, qc3 = st.columns(3)
    with qc1:
        fig = px.pie(df, names="Campaign_Type", values="Revenue",
                     color_discrete_sequence=COLOR_SEQ, hole=0.5,
                     title="Revenue Share by Campaign")
        fig.update_layout(height=280, margin=dict(t=40, b=0, l=0, r=0),
                          plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                          font=dict(color="#94a3b8", size=10),
                          title=dict(font=dict(size=12, color="#94a3b8"), x=0.5))
        st.plotly_chart(fig, use_container_width=True)
    with qc2:
        fig2 = px.bar(df.groupby("Customer_Segment")[["Impressions","Clicks","Leads","Conversions"]]\
                      .sum().reset_index().melt(id_vars="Customer_Segment"),
                      x="Customer_Segment", y="value", color="variable",
                      barmode="group", color_discrete_sequence=COLOR_SEQ,
                      title="Funnel by Segment")
        fig2.update_layout(height=280, margin=dict(t=40, b=4, l=4, r=4),
                           plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                           font=dict(color="#94a3b8", size=10),
                           xaxis=dict(tickfont=dict(size=9)),
                           title=dict(font=dict(size=12, color="#94a3b8"), x=0.5))
        st.plotly_chart(fig2, use_container_width=True)
    with qc3:
        mdf = df.dropna(subset=["Date"]).groupby("Month_sort")[["Revenue","Profit"]].sum().reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=mdf["Month_sort"], y=mdf["Revenue"],
                              name="Revenue", marker_color="#3b82f6"))
        fig3.add_trace(go.Bar(x=mdf["Month_sort"], y=mdf["Profit"],
                              name="Profit", marker_color="#10b981"))
        fig3.update_layout(barmode="group", height=280, margin=dict(t=40, b=4, l=4, r=4),
                           plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                           font=dict(color="#94a3b8", size=10), showlegend=True,
                           title=dict(text="Month-wise Revenue vs Profit",
                                      font=dict(size=12, color="#94a3b8"), x=0.5))
        st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# SIDEBAR FILTERS (shared)
# ═══════════════════════════════════════════════════════════════
def sidebar_filters():
    st.sidebar.markdown("""
    <div style="text-align:center; padding: 10px 0 4px 0;">
        <div style="font-size:28px;">🔍</div>
        <div style="color:white; font-size:14px; font-weight:800;">Filters</div>
    </div>""", unsafe_allow_html=True)

    campaign_filter = st.sidebar.multiselect(
        "Campaign Type", sorted(df["Campaign_Type"].dropna().unique()),
        sorted(df["Campaign_Type"].dropna().unique()), key="cf")

    channel_filter = st.sidebar.multiselect(
        "Channel Used", sorted(df["Channel_Used"].dropna().unique()),
        sorted(df["Channel_Used"].dropna().unique()), key="ch")

    segment_filter = st.sidebar.multiselect(
        "Customer Segment", sorted(df["Customer_Segment"].dropna().unique()),
        sorted(df["Customer_Segment"].dropna().unique()), key="sg")

    dur_filter = st.sidebar.multiselect(
        "Duration Bucket",
        ["Short (≤10d)", "Medium (11-20d)", "Long (21-30d)"],
        ["Short (≤10d)", "Medium (11-20d)", "Long (21-30d)"], key="db")

    lang_filter = st.sidebar.multiselect(
        "Language", sorted(df["Language"].dropna().unique()),
        sorted(df["Language"].dropna().unique()), key="lg")

    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 Back to Home", use_container_width=True):
        st.session_state.page = "landing"
        st.rerun()

    fdf = df[
        df["Campaign_Type"].isin(campaign_filter) &
        df["Channel_Used"].isin(channel_filter) &
        df["Customer_Segment"].isin(segment_filter) &
        df["Duration_Bucket"].isin(dur_filter) &
        df["Language"].isin(lang_filter)
    ].copy()

    return fdf


# ═══════════════════════════════════════════════════════════════
# INTERNAL ANALYTICS DASHBOARD
# ═══════════════════════════════════════════════════════════════
def internal_dashboard():
    fdf = sidebar_filters()

    # Hero
    st.markdown(f"""
    <div class="hero">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <div class="hero-title">📊 Internal Analytics Dashboard</div>
                <div class="hero-sub">Analyst-Level Campaign Intelligence · KPI Drill-Down View · {len(fdf):,} records</div>
            </div>
            <div>
                <span class="filter-pill">Records: <b>{len(fdf):,}</b></span>
                <span class="filter-pill">Campaigns: <b>{fdf['Campaign_Type'].nunique()}</b></span>
                <span class="filter-pill">Channels: <b>{fdf['Channel_Used'].nunique()}</b></span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    if fdf.empty:
        st.warning("No data matches current filters. Please adjust sidebar selections.")
        return

    # ── SECTION 1: KPI OVERVIEW COUNT METRICS ──
    st.markdown('<div class="sec-hdr">📌 KPI Overview — Count Metrics</div>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        ct = fdf["Campaign_ID"].count()
        tags = "".join(f'<span class="ktag ktag-b">{n}: {v:,}</span>'
                       for n, v in fdf["Campaign_Type"].value_counts().head(3).items())
        st.markdown(f"""<div class="kcard kcard-glow">
            <div class="klabel">Count ID (Records)</div>
            <div class="kval">{ct:,}</div>
            <div class="ksub">Total Campaign IDs</div>
            <div class="kdivider"></div>{tags}</div>""", unsafe_allow_html=True)

    with k2:
        ct_n = fdf["Campaign_Type"].nunique()
        tags = "".join(f'<span class="ktag ktag-p">{n}: {v:,}</span>'
                       for n, v in fdf["Campaign_Type"].value_counts().head(4).items())
        st.markdown(f"""<div class="kcard kcard-glow2">
            <div class="klabel">Campaign Type Count</div>
            <div class="kval">{ct_n}</div>
            <div class="ksub">Unique types</div>
            <div class="kdivider"></div>{tags}</div>""", unsafe_allow_html=True)

    with k3:
        ch_n = fdf["Channel_Used"].nunique()
        tags = "".join(f'<span class="ktag ktag-g">{n[:14]}: {v:,}</span>'
                       for n, v in fdf["Channel_Used"].value_counts().head(4).items())
        st.markdown(f"""<div class="kcard kcard-glow3">
            <div class="klabel">Channel Count</div>
            <div class="kval">{ch_n}</div>
            <div class="ksub">Unique channels</div>
            <div class="kdivider"></div>{tags}</div>""", unsafe_allow_html=True)

    with k4:
        seg_n = fdf["Customer_Segment"].nunique()
        tags = "".join(f'<span class="ktag ktag-o">{n}: {v:,}</span>'
                       for n, v in fdf["Customer_Segment"].value_counts().head(4).items())
        st.markdown(f"""<div class="kcard kcard-glow4">
            <div class="klabel">Customer Segment Count</div>
            <div class="kval">{seg_n}</div>
            <div class="ksub">Unique segments</div>
            <div class="kdivider"></div>{tags}</div>""", unsafe_allow_html=True)

    with k5:
        dur_tags = "".join(f'<span class="ktag ktag-r">{n}: {v:,}</span>'
                           for n, v in fdf["Duration_Bucket"].value_counts().items())
        ads_total = fdf["Ads cost"].sum()
        st.markdown(f"""<div class="kcard kcard-glow">
            <div class="klabel">Duration Count / Ads Cost</div>
            <div class="kval">{fmt_ind(ads_total, '₹')}</div>
            <div class="ksub">Total Ads Spend · Avg dur: {fdf['Duration'].mean():.0f}d</div>
            <div class="kdivider"></div>{dur_tags}</div>""", unsafe_allow_html=True)

    # Duration breakdown bar
    st.markdown('<div class="sec-hdr">⏱ Duration Bucket × Engagement Overview</div>', unsafe_allow_html=True)
    da1, da2, da3 = st.columns(3)
    dur_metrics = fdf.groupby("Duration_Bucket")[["Impressions","Clicks","Leads","Conversions","Revenue"]].sum().reset_index()
    with da1:
        fig = px.bar(dur_metrics.melt(id_vars="Duration_Bucket",
                                      value_vars=["Impressions","Clicks","Leads","Conversions"]),
                     x="Duration_Bucket", y="value", color="variable", barmode="group",
                     color_discrete_sequence=COLOR_SEQ, title="Funnel by Duration")
        st.plotly_chart(slim(fig), use_container_width=True)
    with da2:
        fig2 = px.bar(dur_metrics, x="Duration_Bucket", y="Revenue",
                      color="Duration_Bucket", color_discrete_sequence=COLOR_SEQ,
                      title="Revenue by Duration Bucket")
        st.plotly_chart(slim(fig2), use_container_width=True)
    with da3:
        eng_dur = fdf.groupby("Duration_Label")["Engage of interest(actively  user engaged)"].sum().reset_index()
        fig3 = px.pie(eng_dur, names="Duration_Label",
                      values="Engage of interest(actively  user engaged)",
                      color_discrete_sequence=["#3b82f6","#f59e0b"], hole=0.5,
                      title="Engagement Share by Duration")
        fig3.update_layout(height=230, margin=dict(t=32, b=0, l=0, r=0),
                           plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                           font=dict(color="#94a3b8", size=10),
                           title=dict(font=dict(size=11, color="#94a3b8"), x=0.5))
        st.plotly_chart(fig3, use_container_width=True)

    # ── SECTION 2: ENGAGE OF INTEREST ──
    st.markdown('<div class="sec-hdr">🔥 Engage of Interest (Actively User Engaged)</div>', unsafe_allow_html=True)
    eng_col = "Engage of interest(actively  user engaged)"
    ec1, ec2, ec3 = st.columns(3)
    total_eng = fdf[eng_col].sum()
    avg_eng = fdf[eng_col].mean()

    with ec1:
        camp_rows = [(n, fmt_ind(v)) for n, v in fdf.groupby("Campaign_Type")[eng_col].sum().sort_values(ascending=False).head(3).items()]
        chan_rows  = [(n[:16], fmt_ind(v)) for n, v in fdf.groupby("Channel_Used")[eng_col].sum().sort_values(ascending=False).head(3).items()]
        seg_rows   = [(n, fmt_ind(v)) for n, v in fdf.groupby("Customer_Segment")[eng_col].sum().sort_values(ascending=False).head(3).items()]
        dur_rows   = [(str(n), fmt_ind(v)) for n, v in fdf.groupby("Duration_Bucket")[eng_col].sum().sort_values(ascending=False).items()]
        st.markdown(kpi_card("Actively Engaged Users",
                             fmt_ind(total_eng), f"Avg: {fmt_ind(avg_eng)}",
                             camp_rows, chan_rows, seg_rows, dur_rows, "kcard-glow3"),
                    unsafe_allow_html=True)
    with ec2:
        gdf = fdf.groupby("Campaign_Type")[eng_col].sum().reset_index()
        fig = px.bar(gdf, x="Campaign_Type", y=eng_col, color="Campaign_Type",
                     color_discrete_sequence=COLOR_SEQ, title="By Campaign")
        st.plotly_chart(slim(fig), use_container_width=True)
    with ec3:
        gdf2 = fdf.groupby("Customer_Segment")[eng_col].sum().reset_index()
        fig2 = px.pie(gdf2, names="Customer_Segment", values=eng_col,
                      color_discrete_sequence=COLOR_SEQ, hole=0.5, title="By Segment")
        fig2.update_layout(height=230, margin=dict(t=32, b=0, l=0, r=0),
                           plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                           font=dict(color="#94a3b8", size=10),
                           title=dict(font=dict(size=11, color="#94a3b8"), x=0.5))
        st.plotly_chart(fig2, use_container_width=True)

    # ── SECTION 3–9: MAIN METRIC SECTIONS ──
    render_section("👁 Impressions Count", "Impressions", fdf, fmt_fn=fmt_ind,
                   optional_cols=OPTIONALS, glow="kcard-glow")

    render_section("🖱 Clicks Count", "Clicks", fdf, fmt_fn=fmt_ind,
                   optional_cols=OPTIONALS, glow="kcard-glow2",
                   extra_html=f" | CTR: {fmt_pct(fdf['CTR'].mean())}")

    render_section("🎯 Lead Count", "Leads", fdf, fmt_fn=fmt_ind,
                   optional_cols=OPTIONALS, glow="kcard-glow3",
                   extra_html=f" | LCR: {fmt_pct(fdf['LCR(people)'].mean())}")

    render_section("🔄 Conversions Count", "Conversions", fdf, fmt_fn=fmt_ind,
                   optional_cols=OPTIONALS, glow="kcard-glow4",
                   extra_html=f" | Conv Rate: {fmt_pct(fdf['Conversions'].sum()/max(fdf['Clicks'].sum(),1)*100)}")

    render_section("💰 Acquisition Cost (₹)", "Acquisition_Cost", fdf,
                   fmt_fn=lambda x: fmt_ind(x, "₹"),
                   optional_cols=OPTIONALS, glow="kcard-glow")

    render_section("⚡ Engagement Score", "Engagement_Score", fdf, agg="mean",
                   fmt_fn=fmt_pct, optional_cols=OPTIONALS, glow="kcard-glow2")

    render_section("📈 Revenue (₹)", "Revenue", fdf, fmt_fn=lambda x: fmt_ind(x, "₹"),
                   optional_cols=OPTIONALS, glow="kcard-glow3")

    render_section("💎 Profit (₹)", "Profit", fdf, fmt_fn=lambda x: fmt_ind(x, "₹"),
                   optional_cols=OPTIONALS, glow="kcard-glow4",
                   extra_html=f" | Margin: {fmt_pct(fdf['Profit'].sum()/max(fdf['Revenue'].sum(),1)*100)}")

    # ── SECTION 10: CURRENT vs PREVIOUS MONTH ──
    if fdf["Date"].notna().any():
        st.markdown('<div class="sec-hdr">📅 Current Month vs Previous Month Comparison</div>', unsafe_allow_html=True)
        max_date = fdf["Date"].max()
        curr_m = max_date.to_period("M")
        prev_m = curr_m - 1
        curr = fdf[fdf["Month"] == curr_m]
        prev = fdf[fdf["Month"] == prev_m]

        mv_cols = [
            ("Count", len(curr), len(prev), ""),
            ("Impressions", curr["Impressions"].sum(), prev["Impressions"].sum(), ""),
            ("Clicks", curr["Clicks"].sum(), prev["Clicks"].sum(), ""),
            ("Leads", curr["Leads"].sum(), prev["Leads"].sum(), ""),
            ("Conversions", curr["Conversions"].sum(), prev["Conversions"].sum(), ""),
            ("Revenue", curr["Revenue"].sum(), prev["Revenue"].sum(), "₹"),
            ("Profit", curr["Profit"].sum(), prev["Profit"].sum(), "₹"),
            ("Acq. Cost", curr["Acquisition_Cost"].sum(), prev["Acquisition_Cost"].sum(), "₹"),
            ("ROI", curr["ROI"].mean(), prev["ROI"].mean(), ""),
            ("Engagement", curr["Engagement_Score"].mean(), prev["Engagement_Score"].mean(), ""),
        ]

        mc1, mc2 = st.columns([1, 1.6])
        with mc1:
            st.markdown(f"**📅 {curr_m}** vs **{prev_m}**", unsafe_allow_html=False)
            for label, cv, pv, sym in mv_cols:
                d = delta_pct(cv, pv)
                arrow = "▲" if d >= 0 else "▼"
                color = "#10b981" if d >= 0 else "#ef4444"
                v_str = f"{sym}{fmt_ind(cv)}" if sym else fmt_ind(cv)
                st.markdown(f"""
                <div class="mrow">
                  <span class="mrow-label">{label}</span>
                  <span class="mrow-val">{v_str}</span>
                  <span style="color:{color};font-size:11px;font-weight:700;">{arrow} {abs(d):.1f}%</span>
                </div>""", unsafe_allow_html=True)

        with mc2:
            camp_trend = fdf[fdf["Month"].isin([curr_m, prev_m])]\
                .groupby(["Month_sort","Campaign_Type"])[["Revenue","Profit"]]\
                .sum().reset_index()
            fig = px.bar(camp_trend, x="Campaign_Type", y="Revenue",
                         color="Month_sort", barmode="group",
                         color_discrete_sequence=["#3b82f6","#f59e0b"],
                         title=f"Revenue Comparison: {prev_m} vs {curr_m}")
            fig.update_layout(height=340, margin=dict(t=40, b=4, l=4, r=4),
                               plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                               font=dict(color="#94a3b8", size=10),
                               title=dict(font=dict(size=12, color="#94a3b8"), x=0.5))
            st.plotly_chart(fig, use_container_width=True)

    # ── SUMMARY TABLE ──
    st.markdown('<div class="sec-hdr">📋 Full Analyst Data Table</div>', unsafe_allow_html=True)
    display_cols = ["Campaign_ID","Campaign_Type","Channel_Used","Customer_Segment",
                    "Duration","Duration_Bucket","Impressions","Clicks","Leads",
                    "Conversions","Revenue","Profit","Acquisition_Cost",
                    "CAC(rupees)","CTR","LCR(people)","RPC(people cR)",
                    "Engagement_Score","ROI","Ads cost","Date"]
    st.dataframe(
        fdf[[c for c in display_cols if c in fdf.columns]]\
          .sort_values("Profit", ascending=False),
        use_container_width=True, height=380
    )
    st.markdown(f"""<div style="text-align:center;color:#334155;margin-top:12px;font-size:11px;">
        📊 Internal Analytics · {len(fdf):,} records · All monetary values in ₹ INR
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# ROI DASHBOARD
# ═══════════════════════════════════════════════════════════════
def roi_dashboard():
    fdf = sidebar_filters()
    st.markdown(f"""<div class="hero">
        <div class="hero-title">💰 Investment ROI Dashboard</div>
        <div class="hero-sub">Financial Performance · {len(fdf):,} records · ROI, CAC, RPC, Profit Analysis</div>
    </div>""", unsafe_allow_html=True)

    if fdf.empty:
        st.warning("No data. Adjust filters.")
        return

    # Top KPIs
    r1, r2, r3, r4, r5 = st.columns(5)
    kpis = [
        ("Total Revenue", fdf["Revenue"].sum(), "₹", "#3b82f6"),
        ("Total Profit", fdf["Profit"].sum(), "₹", "#10b981"),
        ("Avg ROI", fdf["ROI"].mean(), "%", "#8b5cf6"),
        ("Avg CAC", fdf["CAC(rupees)"].mean(), "₹", "#f59e0b"),
        ("Ret. Inv. Cost", fdf["Return Of Investment Cost"].sum(), "₹", "#ef4444"),
    ]
    for col_, (label, val, sym, color) in zip([r1, r2, r3, r4, r5], kpis):
        with col_:
            v_str = fmt_ind(val, sym) if sym == "₹" else f"{val:.2f}%"
            st.markdown(f"""<div class="kcard" style="border-color:{color}30;box-shadow:0 0 16px {color}15;">
                <div class="klabel">{label}</div>
                <div class="kval" style="color:{color};">{v_str}</div>
            </div>""", unsafe_allow_html=True)

    render_section("💰 Acquisition Cost (₹)", "Acquisition_Cost", fdf, fmt_fn=lambda x: fmt_ind(x,"₹"), glow="kcard-glow")
    render_section("📊 ROI (%)", "ROI", fdf, agg="mean", fmt_fn=fmt_pct, glow="kcard-glow2")
    render_section("💸 CAC — Customer Acquisition Cost (₹)", "CAC(rupees)", fdf, agg="mean", fmt_fn=lambda x: fmt_ind(x,"₹"), glow="kcard-glow3")
    render_section("🏆 RPC — Revenue Per Click (₹)", "RPC(people cR)", fdf, fmt_fn=lambda x: fmt_ind(x,"₹"), glow="kcard-glow4")
    render_section("📈 Revenue (₹)", "Revenue", fdf, fmt_fn=lambda x: fmt_ind(x,"₹"), glow="kcard-glow")
    render_section("💎 Profit (₹)", "Profit", fdf, fmt_fn=lambda x: fmt_ind(x,"₹"), glow="kcard-glow2")
    render_section("🔁 Return Investment Cost (₹)", "Return Of Investment Cost", fdf, fmt_fn=lambda x: fmt_ind(x,"₹"), glow="kcard-glow3")
    render_section("📣 Return Investment Ads Count", "Return inverstmene ad", fdf, fmt_fn=fmt_ind, glow="kcard-glow4")

    # Month-wise trend
    if fdf["Date"].notna().any():
        st.markdown('<div class="sec-hdr">📅 Month-Wise Financial Trend</div>', unsafe_allow_html=True)
        mdf = fdf.dropna(subset=["Date"]).groupby("Month_sort")[
            ["Revenue","Profit","Acquisition_Cost","Return Of Investment Cost"]].sum().reset_index()
        fig = go.Figure()
        colors = ["#3b82f6","#10b981","#ef4444","#f59e0b"]
        for i, col_ in enumerate(["Revenue","Profit","Acquisition_Cost","Return Of Investment Cost"]):
            fig.add_trace(go.Scatter(x=mdf["Month_sort"], y=mdf[col_],
                                     name=col_, mode="lines+markers",
                                     line=dict(color=colors[i], width=2),
                                     marker=dict(size=5)))
        fig.update_layout(height=320, margin=dict(t=40, b=4, l=4, r=4),
                          plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                          font=dict(color="#94a3b8", size=10), showlegend=True,
                          title=dict(text="Monthly Trend: Revenue, Profit, Acq. Cost, Return Inv.",
                                     font=dict(size=12, color="#94a3b8"), x=0.5))
        fig.update_xaxes(gridcolor="#0f1e35")
        fig.update_yaxes(gridcolor="#0f1e35")
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# ENGAGEMENT DASHBOARD
# ═══════════════════════════════════════════════════════════════
def engagement_dashboard():
    fdf = sidebar_filters()
    st.markdown(f"""<div class="hero">
        <div class="hero-title">🎯 Engagement Intelligence Dashboard</div>
        <div class="hero-sub">CTR · LCR · Engagement Score · Active Users · Duration Patterns · {len(fdf):,} records</div>
    </div>""", unsafe_allow_html=True)

    if fdf.empty:
        st.warning("No data. Adjust filters.")
        return

    e1, e2, e3, e4, e5 = st.columns(5)
    ekpis = [
        ("Avg Engagement Score", fdf["Engagement_Score"].mean(), "%", "#3b82f6"),
        ("Avg CTR", fdf["CTR"].mean(), "%", "#8b5cf6"),
        ("Avg LCR", fdf["LCR(people)"].mean(), "%", "#10b981"),
        ("Total Engaged Users", fdf["Engage of interest(actively  user engaged)"].sum(), "", "#f59e0b"),
        ("Total Duration Earn", fdf["Duration wise earn"].sum(), "₹", "#ef4444"),
    ]
    for col_, (label, val, sym, color) in zip([e1, e2, e3, e4, e5], ekpis):
        with col_:
            v_str = fmt_pct(val) if sym == "%" else fmt_ind(val, sym)
            st.markdown(f"""<div class="kcard" style="border-color:{color}30;box-shadow:0 0 16px {color}15;">
                <div class="klabel">{label}</div>
                <div class="kval" style="color:{color};">{v_str}</div>
            </div>""", unsafe_allow_html=True)

    render_section("⚡ Engagement Score", "Engagement_Score", fdf, agg="mean", fmt_fn=fmt_pct, glow="kcard-glow")
    render_section("📊 CTR — Click Through Rate (%)", "CTR", fdf, agg="mean", fmt_fn=fmt_pct, glow="kcard-glow2")
    render_section("🎯 LCR — Lead Conversion Rate (%)", "LCR(people)", fdf, agg="mean", fmt_fn=fmt_pct, glow="kcard-glow3")
    render_section("🔥 Actively Engaged Users", "Engage of interest(actively  user engaged)", fdf, fmt_fn=fmt_ind, glow="kcard-glow4")
    render_section("⏱ Duration Wise Earn (₹)", "Duration wise earn", fdf, fmt_fn=lambda x: fmt_ind(x,"₹"), glow="kcard-glow")
    render_section("💡 Ads Cost (₹)", "Ads cost", fdf, fmt_fn=lambda x: fmt_ind(x,"₹"), glow="kcard-glow2")

    # Heatmap: Engagement by Segment × Campaign
    if fdf["Date"].notna().any():
        st.markdown('<div class="sec-hdr2">🗺 Engagement Heatmap: Segment × Campaign</div>', unsafe_allow_html=True)
        hm_data = fdf.groupby(["Customer_Segment","Campaign_Type"])["Engagement_Score"].mean().reset_index()
        hm_pivot = hm_data.pivot(index="Customer_Segment", columns="Campaign_Type", values="Engagement_Score")
        fig = go.Figure(data=go.Heatmap(
            z=hm_pivot.values,
            x=hm_pivot.columns.tolist(),
            y=hm_pivot.index.tolist(),
            colorscale="Blues",
            text=[[f"{v:.1f}" for v in row] for row in hm_pivot.values],
            texttemplate="%{text}",
            showscale=True
        ))
        fig.update_layout(height=300, margin=dict(t=40, b=4, l=4, r=4),
                          plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                          font=dict(color="#94a3b8", size=10),
                          title=dict(text="Avg Engagement Score: Segment × Campaign",
                                     font=dict(size=12, color="#94a3b8"), x=0.5))
        st.plotly_chart(fig, use_container_width=True)

        # Month-wise engagement trend
        st.markdown('<div class="sec-hdr2">📅 Month-Wise Engagement Trend</div>', unsafe_allow_html=True)
        mdf = fdf.dropna(subset=["Date"]).groupby("Month_sort")[
            ["Engagement_Score","CTR","LCR(people)"]].mean().reset_index()
        fig2 = go.Figure()
        for col_, color in zip(["Engagement_Score","CTR","LCR(people)"],
                                ["#3b82f6","#8b5cf6","#10b981"]):
            fig2.add_trace(go.Scatter(x=mdf["Month_sort"], y=mdf[col_],
                                      name=col_, mode="lines+markers",
                                      line=dict(color=color, width=2),
                                      marker=dict(size=5)))
        fig2.update_layout(height=300, margin=dict(t=40, b=4, l=4, r=4),
                           plot_bgcolor="#060d1f", paper_bgcolor="#060d1f",
                           font=dict(color="#94a3b8", size=10), showlegend=True,
                           title=dict(text="Monthly Engagement Score, CTR & LCR Trends",
                                      font=dict(size=12, color="#94a3b8"), x=0.5))
        fig2.update_xaxes(gridcolor="#0f1e35")
        fig2.update_yaxes(gridcolor="#0f1e35")
        st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "internal":
    internal_dashboard()
elif st.session_state.page == "roi":
    roi_dashboard()
elif st.session_state.page == "engagement":
    engagement_dashboard()