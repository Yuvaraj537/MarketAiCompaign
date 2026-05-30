"""
╔══════════════════════════════════════════════════════════════╗
║   AI MARKETING INTELLIGENCE PLATFORM — UNIFIED APP          ║
║   4 Sections:                                                ║
║     1. Performance Overview  (main.py renamed)              ║
║     2. Internal Analytics    (analytics.py)                 ║
║     3. Marketing Analyst     (Marketing_Analyst.py)         ║
║     4. AI Chatbot            (PDF-based, Groq + FAISS)      ║
╚══════════════════════════════════════════════════════════════╝
"""

import re
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Marketing Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────
if "section" not in st.session_state:
    st.session_state.section = "home"
if "chat" not in st.session_state:
    st.session_state.chat = []
if "ma_page" not in st.session_state:
    st.session_state.ma_page = "internal"   # sub-page inside Marketing Analyst

# ──────────────────────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
*, body { font-family: 'Inter', sans-serif !important; }

.stApp { background: #060d1f; color: #e2e8f0; }
.block-container { padding: 0.5rem 1.5rem 2rem 1.5rem !important; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #060d1f 100%) !important;
    border-right: 1px solid #1e3a5f;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

h1 { color:#fff !important; font-size:36px !important; font-weight:900 !important; }
h2, h3 { color:#e2e8f0 !important; font-weight:700 !important; }

/* Nav buttons in sidebar */
.nav-btn { width:100%; margin:3px 0; }

/* Metric */
[data-testid="stMetricLabel"] { color:#64748b !important; font-size:11px !important; text-transform:uppercase; letter-spacing:1px; }
[data-testid="stMetricValue"] { color:#f1f5f9 !important; font-size:22px !important; font-weight:800 !important; }
[data-testid="stMetricDelta"] { font-size:11px !important; }

/* KPI Cards — performance overview style */
.kpi-ov {
    background: linear-gradient(145deg, #111827, #1f2937);
    border: 1px solid #374151;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    transition: 0.3s;
    margin-bottom:8px;
}
.kpi-ov:hover { transform:translateY(-3px); border-color:#10b981; box-shadow:0 0 14px rgba(16,185,129,0.3); }
.kpi-label-ov { color:#9ca3af; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; }
.kpi-value-ov { color:white; font-size:26px; font-weight:900; margin:4px 0; }
.kpi-sub-ov   { color:#6b7280; font-size:10px; }
.kpi-tag-ov   { display:inline-block; background:#1d4ed8; color:white; border-radius:4px; padding:1px 6px; font-size:10px; margin:2px 1px; }
.kpi-tag-g    { background:#065f46 !important; }
.kpi-tag-p    { background:#4c1d95 !important; }
.kpi-tag-o    { background:#92400e !important; }

/* Section header bar */
.sec-hdr {
    background: linear-gradient(90deg, #1d4ed8 0%, rgba(29,78,216,0.15) 60%, transparent 100%);
    border-left: 4px solid #3b82f6;
    padding: 9px 16px;
    border-radius: 0 10px 10px 0;
    margin: 22px 0 12px 0;
    color: white;
    font-size: 16px;
    font-weight: 800;
}
.sec-hdr2 {
    border-left: 4px solid #8b5cf6;
    background: linear-gradient(90deg, rgba(139,92,246,0.2) 0%, transparent 100%);
    padding: 9px 16px;
    border-radius: 0 10px 10px 0;
    margin: 22px 0 12px 0;
    color: white;
    font-size: 16px;
    font-weight: 800;
}

/* Marketing Analyst KPI cards */
.kcard {
    background: linear-gradient(140deg, #0f2044 0%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 16px 14px;
    margin-bottom: 8px;
}
.kcard-glow  { border-color:#3b82f6 !important; box-shadow:0 0 20px rgba(59,130,246,0.15); }
.kcard-glow2 { border-color:#8b5cf6 !important; box-shadow:0 0 20px rgba(139,92,246,0.15); }
.kcard-glow3 { border-color:#10b981 !important; box-shadow:0 0 20px rgba(16,185,129,0.15); }
.kcard-glow4 { border-color:#f59e0b !important; box-shadow:0 0 20px rgba(245,158,11,0.15); }
.klabel { color:#64748b; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; }
.kval   { color:white; font-size:24px; font-weight:900; margin:4px 0; line-height:1.1; }
.ksub   { color:#475569; font-size:10px; margin:2px 0 8px 0; }
.ktag   { display:inline-block; border-radius:5px; padding:2px 7px; font-size:10px; font-weight:600; margin:2px 1px; }
.ktag-b { background:rgba(59,130,246,0.2); color:#93c5fd; border:1px solid rgba(59,130,246,0.3); }
.ktag-g { background:rgba(16,185,129,0.2); color:#6ee7b7; border:1px solid rgba(16,185,129,0.3); }
.ktag-p { background:rgba(139,92,246,0.2); color:#c4b5fd; border:1px solid rgba(139,92,246,0.3); }
.ktag-o { background:rgba(245,158,11,0.2); color:#fcd34d;  border:1px solid rgba(245,158,11,0.3); }
.kdivider { height:1px; background:linear-gradient(90deg,#1e3a5f,transparent); margin:8px 0; }
.krow-label { color:#475569; font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin:4px 0 2px 0; }
.mrow { display:flex; justify-content:space-between; align-items:center; background:#0f1e35; border-radius:8px; padding:6px 12px; margin:3px 0; }
.mrow-label { color:#64748b; font-size:11px; }
.mrow-val   { color:white; font-weight:700; font-size:12px; }

/* Hero banner */
.hero { background:linear-gradient(135deg,#0f2044,#071428,#0a1628); border:1px solid #1e3a5f; border-radius:18px; padding:22px 28px; margin-bottom:18px; }
.hero-title { color:white; font-size:26px; font-weight:900; margin:0; }
.hero-sub   { color:#64748b; font-size:13px; margin:4px 0 0 0; }

/* Home cards */
.home-card {
    background: linear-gradient(135deg,#0f2044,#0a1628);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 32px 24px;
    text-align: center;
    transition: 0.3s;
    margin: 6px;
    cursor: pointer;
}
.home-card:hover { border-color:#3b82f6; transform:translateY(-4px); box-shadow:0 20px 40px rgba(59,130,246,0.2); }
.home-icon  { font-size:52px; display:block; margin-bottom:14px; }
.home-title { color:white; font-size:19px; font-weight:800; margin-bottom:8px; }
.home-desc  { color:#64748b; font-size:12px; line-height:1.6; }
.home-badge { display:inline-block; background:#1d4ed8; color:white; border-radius:20px; padding:3px 12px; font-size:11px; font-weight:700; margin-top:12px; }

/* Chat bubbles */
.user-bubble { background:#1E88E5; color:white; padding:11px 16px; border-radius:18px 18px 4px 18px; margin:8px 0 2px auto; max-width:78%; width:fit-content; font-size:15px; line-height:1.5; margin-left:auto; }
.bot-bubble  { background:#0f1e35; color:#e2e8f0; padding:11px 16px; border-radius:18px 18px 18px 4px; margin:8px auto 2px 0; max-width:85%; width:fit-content; font-size:15px; line-height:1.65; border:1px solid #1e3a5f; }
.ts { font-size:11px; color:#475569; margin-bottom:10px; }
.ts-right { text-align:right; }
.ts-left  { text-align:left;  }
.pill { display:inline-block; background:#0f1e35; color:#93c5fd; border-radius:20px; padding:2px 10px; font-size:11px; margin:2px; border:1px solid #1e3a5f; }

/* Download button */
.stDownloadButton button { background:linear-gradient(90deg,#10b981,#059669); color:white !important; border:none; border-radius:12px; padding:10px 20px; font-weight:bold; }

/* Scrollbar */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#060d1f; }
::-webkit-scrollbar-thumb { background:#3b82f6; border-radius:10px; }

/* Filter info */
.filter-info { background:#0f1e35; border:1px solid #1e3a5f; border-radius:8px; padding:8px 14px; font-size:12px; color:#64748b; margin-bottom:16px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════
CSV_PATH = "data/compaign_analyst.csv"

@st.cache_data
def load_base_data():
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip() for c in df.columns]
    # Derived categoricals (for main.py / performance overview)
    campaign_cats = ["Social Media","Paid Ads","Influencer","Email","CEO"]
    channel_cats  = ["WhatsApp","YouTube","Instagram","Email","Facebook","Google"]
    customer_cats = ["College Student","Tier 2 City Customers","Youth","Working Women","Premium Shoppers"]
    if "Campaign_Type" not in df.columns:
        df["Campaign_Type"] = [campaign_cats[i % len(campaign_cats)] for i in range(len(df))]
    if "Channel_Used" not in df.columns:
        df["Channel_Used"] = [channel_cats[i % len(channel_cats)] for i in range(len(df))]
    if "Customer_Segment" not in df.columns:
        df["Customer_Segment"] = [customer_cats[i % len(customer_cats)] for i in range(len(df))]
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["Month"]      = df["Date"].dt.to_period("M")
    df["Month_str"]  = df["Date"].dt.strftime("%b %Y")
    df["Month_sort"] = df["Date"].dt.to_period("M").astype(str)
    # Duration buckets
    if "Duration" in df.columns:
        df["Duration_Bucket"] = pd.cut(df["Duration"], bins=[0,10,20,31],
                                        labels=["Short (≤10d)","Medium (11-20d)","Long (21-30d)"])
        df["Duration_Label"] = df["Duration"].apply(
            lambda x: "≤30 Min Equivalent" if x <= 15 else "1 Hr+ Equivalent")
    # Calculated metrics
    if "Clicks" in df.columns and "Impressions" in df.columns:
        df["Calculated_CTR"]    = (df["Clicks"] / df["Impressions"].replace(0,1)) * 100
        df["Conversion_Rate"]   = (df["Conversions"] / df["Clicks"].replace(0,1)) * 100
    if "Acquisition_Cost" in df.columns:
        df["CPA"]               = df["Acquisition_Cost"] / df["Conversions"].replace(0,1)
        df["Calculated_Profit"] = df["Revenue"] - df["Acquisition_Cost"]
        df["ROAS"]              = df["Revenue"] / df["Acquisition_Cost"].replace(0,1)
    return df

try:
    DF = load_base_data()
    DATA_OK = True
except FileNotFoundError:
    DF = pd.DataFrame()
    DATA_OK = False

# ══════════════════════════════════════════════════════════════
# SHARED HELPERS
# ══════════════════════════════════════════════════════════════
PLOTLY_BG = "#060d1f"
COLOR_SEQ  = ["#3b82f6","#8b5cf6","#10b981","#f59e0b","#ef4444","#06b6d4","#ec4899"]

def slim_fig(fig, title=""):
    fig.update_layout(
        height=220, margin=dict(t=30, b=4, l=4, r=4),
        showlegend=False, plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
        font=dict(color="#94a3b8", size=10),
        title=dict(text=title, font=dict(size=11, color="#94a3b8"), x=0.5),
    )
    fig.update_xaxes(gridcolor="#0f1e35", tickfont=dict(size=9))
    fig.update_yaxes(gridcolor="#0f1e35", tickfont=dict(size=9))
    return fig

def fmt_ind(val, prefix=""):
    if pd.isna(val): return "—"
    val = float(val); sign = "-" if val < 0 else ""; val = abs(val)
    if val >= 1_00_00_000: return f"{sign}{prefix}{val/1_00_00_000:.2f} Cr"
    elif val >= 1_00_000:  return f"{sign}{prefix}{val/1_00_000:.2f} L"
    elif val >= 1_000:     return f"{sign}{prefix}{val/1_000:.1f} K"
    else:                  return f"{sign}{prefix}{val:,.0f}"

def fmt_pct(val):
    if pd.isna(val): return "—"
    return f"{float(val):.2f}%"

def delta_pct(a, b):
    return ((a - b) / abs(b) * 100) if b != 0 else 0

def delta_html(d):
    arrow = "▲" if d >= 0 else "▼"
    color = "#10b981" if d >= 0 else "#ef4444"
    return f'<span style="color:{color};font-size:11px;font-weight:700;">{arrow} {abs(d):.1f}%</span>'

def format_inr(value):
    if value >= 10_000_000: return f"₹{value/10_000_000:.2f} Cr"
    elif value >= 100_000:  return f"₹{value/100_000:.2f} L"
    elif value >= 1_000:    return f"₹{value/1_000:.2f} K"
    else:                   return f"₹{value:.0f}"

# ══════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════
def sidebar_nav():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:12px 0 20px 0;'>
            <div style='font-size:36px;'>🚀</div>
            <div style='color:white; font-size:15px; font-weight:800; margin-top:6px;'>AI Marketing Platform</div>
            <div style='color:#475569; font-size:11px;'>Intelligence Dashboard Suite</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        nav_items = [
            ("🏠", "home",           "Home"),
            ("📊", "performance",    "Performance Overview"),
            ("🔬", "internal",       "Internal Analytics"),
            ("📈", "marketing",      "Marketing Analyst"),
            ("💬", "chatbot",        "AI Chatbot (PDF)"),
        ]
        for icon, key, label in nav_items:
            is_active = st.session_state.section == key
            btn_style = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {label}", key=f"nav_{key}",
                         type=btn_style, use_container_width=True):
                st.session_state.section = key
                st.rerun()

        st.markdown("---")

        # Global filters (only when data is loaded)
        if DATA_OK and st.session_state.section in ("performance", "internal", "marketing"):
            st.markdown("### 🎛 Filters")
            campaign_opts = sorted(DF["Campaign_Type"].dropna().unique())
            channel_opts  = sorted(DF["Channel_Used"].dropna().unique())
            segment_opts  = sorted(DF["Customer_Segment"].dropna().unique())

            if "f_campaign" not in st.session_state: st.session_state.f_campaign = campaign_opts
            if "f_channel"  not in st.session_state: st.session_state.f_channel  = channel_opts
            if "f_segment"  not in st.session_state: st.session_state.f_segment  = segment_opts

            st.session_state.f_campaign = st.multiselect("📢 Campaign Type", campaign_opts, st.session_state.f_campaign)
            st.session_state.f_channel  = st.multiselect("📡 Channel",        channel_opts,  st.session_state.f_channel)
            st.session_state.f_segment  = st.multiselect("👥 Segment",        segment_opts,  st.session_state.f_segment)

def get_filtered():
    return DF[
        DF["Campaign_Type"].isin(st.session_state.get("f_campaign", DF["Campaign_Type"].unique())) &
        DF["Channel_Used"].isin(st.session_state.get("f_channel",   DF["Channel_Used"].unique())) &
        DF["Customer_Segment"].isin(st.session_state.get("f_segment", DF["Customer_Segment"].unique()))
    ].copy()

# ══════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════
def render_home():
    st.markdown("""
    <div style='text-align:center; padding:30px 0 20px 0;'>
        <div style='font-size:64px;'>🚀</div>
        <h1 style='font-size:42px !important; margin:10px 0 6px 0;'>AI Marketing Intelligence Platform</h1>
        <p style='color:#64748b; font-size:16px; margin:0 0 36px 0;'>
            Unified Campaign Analytics · AI-Powered Insights · Real-Time Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("performance", "📊", "Performance Overview",
         "High-level KPIs: Revenue, ROAS, CTR, channel performance & campaign profit trends.",
         "KPI · Trends · Charts"),
        ("internal", "🔬", "Internal Analytics",
         "Deep-dive analyst view: Impressions, Clicks, Leads, Conversions, CAC, CTR, RPC & Engagement.",
         "16 KPI Sections · Drill-Down"),
        ("marketing", "📈", "Marketing Analyst",
         "Investment ROI · Acquisition Cost · CAC · Engagement Intelligence · Month-wise trends.",
         "ROI · Engagement · Finance"),
        ("chatbot", "💬", "AI Chatbot (PDF)",
         "Upload a PDF campaign report and ask questions. Powered by FAISS + Groq LLaMA.",
         "RAG · PDF · LLaMA"),
    ]

    for col, (key, icon, title, desc, badge) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""
            <div class='home-card'>
                <span class='home-icon'>{icon}</span>
                <div class='home-title'>{title}</div>
                <div class='home-desc'>{desc}</div>
                <div class='home-badge'>{badge}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open {title}", key=f"home_{key}", use_container_width=True):
                st.session_state.section = key
                st.rerun()

    if DATA_OK:
        st.markdown('<div class="sec-hdr" style="margin-top:36px;">📋 Dataset Snapshot</div>',
                    unsafe_allow_html=True)
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric("Total Records",    f"{len(DF):,}")
        s2.metric("Campaign Types",   DF["Campaign_Type"].nunique())
        s3.metric("Channels",         DF["Channel_Used"].nunique())
        s4.metric("Segments",         DF["Customer_Segment"].nunique())
        if "Revenue" in DF.columns:
            s5.metric("Total Revenue", format_inr(DF["Revenue"].sum()))
    else:
        st.warning("⚠️ CSV file not found at `data/compaign_analyst.csv`. Place your file there to enable dashboards.")

# ══════════════════════════════════════════════════════════════
# SECTION 1 — PERFORMANCE OVERVIEW  (main.py)
# ══════════════════════════════════════════════════════════════
def render_performance():
    if not DATA_OK:
        st.error("❌ CSV not found. Add `data/compaign_analyst.csv` and restart.")
        return

    fdf = get_filtered()

    st.markdown("""
    <div class='hero'>
        <div class='hero-title'>📊 Performance Overview</div>
        <div class='hero-sub'>Real-Time Campaign Analytics & AI Insights</div>
    </div>""", unsafe_allow_html=True)

    # ── KPI row ──
    st.markdown('<div class="sec-hdr">📌 KPI Overview</div>', unsafe_allow_html=True)
    total_revenue = fdf["Revenue"].sum()
    total_cost    = fdf["Acquisition_Cost"].sum()
    total_profit  = fdf["Calculated_Profit"].sum()

    k1, k2, k3, k4, k5 = st.columns(5)
    for col, label, val in [
        (k1, "Revenue",  format_inr(total_revenue)),
        (k2, "Cost",     format_inr(total_cost)),
        (k3, "Profit",   format_inr(total_profit)),
        (k4, "ROAS",     f"{fdf['ROAS'].mean():.2f}x"),
        (k5, "CTR",      f"{fdf['Calculated_CTR'].mean():.2f}%"),
    ]:
        with col:
            st.markdown(f"""
            <div class='kpi-ov'>
                <div class='kpi-label-ov'>{label}</div>
                <div class='kpi-value-ov'>{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Channel & Campaign ──
    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="sec-hdr">📡 Channel Performance</div>', unsafe_allow_html=True)
        ch_data = fdf.groupby("Channel_Used")[["Revenue","Acquisition_Cost"]].sum().reset_index()
        fig = px.bar(ch_data, x="Channel_Used", y=["Revenue","Acquisition_Cost"],
                     barmode="group", template="plotly_dark", color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(paper_bgcolor=PLOTLY_BG, plot_bgcolor=PLOTLY_BG, font_color="white", height=320)
        st.plotly_chart(fig, use_container_width=True)

    with cb:
        st.markdown('<div class="sec-hdr">🎯 Campaign Profit</div>', unsafe_allow_html=True)
        camp_data = fdf.groupby("Campaign_Type")["Calculated_Profit"].sum().reset_index()
        fig2 = px.bar(camp_data, x="Campaign_Type", y="Calculated_Profit",
                      color="Calculated_Profit", template="plotly_dark", color_continuous_scale="Teal")
        fig2.update_layout(paper_bgcolor=PLOTLY_BG, plot_bgcolor=PLOTLY_BG, font_color="white", height=320)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Revenue trend ──
    st.markdown('<div class="sec-hdr">📅 Revenue Trend</div>', unsafe_allow_html=True)
    trend = fdf.groupby("Date")["Revenue"].sum().reset_index()
    fig3  = px.line(trend, x="Date", y="Revenue", template="plotly_dark",
                    color_discrete_sequence=["#3b82f6"])
    fig3.update_layout(paper_bgcolor=PLOTLY_BG, plot_bgcolor=PLOTLY_BG, font_color="white", height=280)
    st.plotly_chart(fig3, use_container_width=True)

    # ── Pie + Scatter ──
    pa, pb = st.columns(2)
    with pa:
        st.markdown('<div class="sec-hdr">👥 Segment Revenue Share</div>', unsafe_allow_html=True)
        fig4 = px.pie(fdf, names="Customer_Segment", values="Revenue", hole=0.4,
                      template="plotly_dark", color_discrete_sequence=COLOR_SEQ)
        fig4.update_layout(paper_bgcolor=PLOTLY_BG, plot_bgcolor=PLOTLY_BG, font_color="white", height=300)
        st.plotly_chart(fig4, use_container_width=True)

    with pb:
        st.markdown('<div class="sec-hdr">💡 Engagement vs Revenue</div>', unsafe_allow_html=True)
        if "Engagement_Score" in fdf.columns:
            fig5 = px.scatter(fdf, x="Engagement_Score", y="Revenue", size="Clicks",
                              color="Campaign_Type", template="plotly_dark",
                              color_discrete_sequence=COLOR_SEQ,
                              hover_data=["Channel_Used","ROAS"])
            fig5.update_layout(paper_bgcolor=PLOTLY_BG, plot_bgcolor=PLOTLY_BG, font_color="white", height=300)
            st.plotly_chart(fig5, use_container_width=True)

    # ── Top 10 Campaigns ──
    st.markdown('<div class="sec-hdr">🏆 Top 10 Campaigns by Profit</div>', unsafe_allow_html=True)
    top10_cols = ["Campaign_ID","Campaign_Type","Channel_Used","Revenue","Acquisition_Cost","Calculated_Profit","ROAS"]
    top10 = fdf.sort_values("Calculated_Profit", ascending=False)[top10_cols].head(10)
    st.dataframe(top10, use_container_width=True)

    # ── AI Insights ──
    st.markdown("---")
    st.markdown('<div class="sec-hdr">🤖 AI Insights</div>', unsafe_allow_html=True)
    best_ch  = fdf.groupby("Channel_Used")["ROAS"].mean().idxmax()
    worst_ch = fdf.groupby("Channel_Used")["CPA"].mean().idxmax()
    best_seg = fdf.groupby("Customer_Segment")["Revenue"].sum().idxmax()
    st.success(f"✅ Best ROAS Channel: **{best_ch}**")
    st.warning(f"⚠️ Highest CPA Channel: **{worst_ch}**")
    st.info(f"👥 Top Revenue Segment: **{best_seg}**")

    # ── Download ──
    st.markdown("---")
    st.download_button("⬇ Download Filtered Report", fdf.to_csv(index=False),
                       "performance_report.csv", "text/csv")


# ══════════════════════════════════════════════════════════════
# SECTION 2 — INTERNAL ANALYTICS  (analytics.py)
# ══════════════════════════════════════════════════════════════
def kpi_block_int(label, value_str, sub, by_camp, by_chan, by_seg):
    camp_tags = "".join(f'<span class="kpi-tag-ov">{n}: {v}</span>' for n,v in by_camp)
    chan_tags  = "".join(f'<span class="kpi-tag-ov kpi-tag-g">{n}: {v}</span>' for n,v in by_chan)
    seg_tags   = "".join(f'<span class="kpi-tag-ov kpi-tag-p">{n}: {v}</span>' for n,v in by_seg)
    return f"""
    <div class='kpi-ov'>
        <div class='kpi-label-ov'>{label}</div>
        <div class='kpi-value-ov'>{value_str}</div>
        <div class='kpi-sub-ov'>{sub}</div>
        <div style='margin-top:6px;'>{camp_tags}</div>
        <div>{chan_tags}</div><div>{seg_tags}</div>
    </div>"""

def top3_sum(col, fdf, fmt=lambda x: f"{x:,.0f}"):
    camp = [(n, fmt(v)) for n,v in fdf.groupby("Campaign_Type")[col].sum().sort_values(ascending=False).head(3).items()]
    chan = [(n, fmt(v)) for n,v in fdf.groupby("Channel_Used")[col].sum().sort_values(ascending=False).head(3).items()]
    seg  = [(n, fmt(v)) for n,v in fdf.groupby("Customer_Segment")[col].sum().sort_values(ascending=False).head(3).items()]
    return camp, chan, seg

def top3_mean(col, fdf, fmt=lambda x: f"{x:,.2f}"):
    camp = [(n, fmt(v)) for n,v in fdf.groupby("Campaign_Type")[col].mean().sort_values(ascending=False).head(3).items()]
    chan = [(n, fmt(v)) for n,v in fdf.groupby("Channel_Used")[col].mean().sort_values(ascending=False).head(3).items()]
    seg  = [(n, fmt(v)) for n,v in fdf.groupby("Customer_Segment")[col].mean().sort_values(ascending=False).head(3).items()]
    return camp, chan, seg

def int_metric_section(title, col, fdf, agg="sum", fmt=lambda x: f"{x:,.0f}", chart="bar"):
    st.markdown(f'<div class="sec-hdr">{title}</div>', unsafe_allow_html=True)
    if agg == "sum":
        val  = fdf[col].sum()
        sub  = f"Avg: {fmt(fdf[col].mean())}"
        bc, bch, bs = top3_sum(col, fdf, fmt)
    else:
        val  = fdf[col].mean()
        sub  = f"Std: {fmt(fdf[col].std())}"
        bc, bch, bs = top3_mean(col, fdf, fmt)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_block_int(col.replace("_"," ").title(), fmt(val), sub, bc, bch, bs),
                    unsafe_allow_html=True)
    with c2:
        gdf = (fdf.groupby("Campaign_Type")[col].sum() if agg=="sum"
               else fdf.groupby("Campaign_Type")[col].mean()).reset_index()
        fig = px.bar(gdf, x="Campaign_Type", y=col, color="Campaign_Type",
                     color_discrete_sequence=COLOR_SEQ, template="plotly_dark")
        st.plotly_chart(slim_fig(fig, "By Campaign"), use_container_width=True)
    with c3:
        gdf2 = (fdf.groupby("Channel_Used")[col].sum() if agg=="sum"
                else fdf.groupby("Channel_Used")[col].mean()).reset_index()
        fig2 = px.bar(gdf2, x="Channel_Used", y=col, color="Channel_Used",
                      color_discrete_sequence=COLOR_SEQ, template="plotly_dark")
        st.plotly_chart(slim_fig(fig2, "By Channel"), use_container_width=True)
    with c4:
        gdf3 = (fdf.groupby("Customer_Segment")[col].sum() if agg=="sum"
                else fdf.groupby("Customer_Segment")[col].mean()).reset_index()
        fig3 = px.pie(gdf3, names="Customer_Segment", values=col, hole=0.45,
                      color_discrete_sequence=COLOR_SEQ, template="plotly_dark")
        st.plotly_chart(slim_fig(fig3, "By Segment"), use_container_width=True)

def render_internal():
    if not DATA_OK:
        st.error("❌ CSV not found.")
        return

    fdf = get_filtered()

    st.markdown("""
    <div class='hero'>
        <div class='hero-title'>🔬 Internal Analytics Dashboard</div>
        <div class='hero-sub'>Analyst-Level Campaign Intelligence · Drill-Down KPI View</div>
    </div>""", unsafe_allow_html=True)

    ct_str = ", ".join(st.session_state.get("f_campaign",[])) if len(st.session_state.get("f_campaign",[])) < 5 else f"{len(st.session_state.get('f_campaign',[]))} types"
    st.markdown(f'<div class="filter-info">🎯 Records: <b>{len(fdf):,}</b> &nbsp;|&nbsp; Campaign: <b>{ct_str}</b></div>',
                unsafe_allow_html=True)

    # Section: Count KPIs
    st.markdown('<div class="sec-hdr">📌 Record & Dimension Counts</div>', unsafe_allow_html=True)
    cc1, cc2, cc3, cc4 = st.columns(4)
    for col_, label_, val_, sub_ in [
        (cc1, "Total Records",     len(fdf),                       f"across {fdf['Campaign_Type'].nunique()} campaigns"),
        (cc2, "Campaign Types",    fdf["Campaign_Type"].nunique(), f"{len(fdf):,} total records"),
        (cc3, "Channels Used",     fdf["Channel_Used"].nunique(),  f"{len(fdf):,} total records"),
        (cc4, "Customer Segments", fdf["Customer_Segment"].nunique(), f"{len(fdf):,} total records"),
    ]:
        with col_:
            st.markdown(f"""
            <div class='kpi-ov'>
                <div class='kpi-label-ov'>{label_}</div>
                <div class='kpi-value-ov'>{val_:,}</div>
                <div class='kpi-sub-ov'>{sub_}</div>
            </div>""", unsafe_allow_html=True)

    # Metric sections
    metrics = [
        ("👁️ Impressions Count",  "Impressions",       "sum",  lambda x: f"{x:,.0f}"),
        ("🖱️ Clicks Count",        "Clicks",            "sum",  lambda x: f"{x:,.0f}"),
        ("🔄 Conversions Count",   "Conversions",       "sum",  lambda x: f"{x:,.0f}"),
        ("🎯 Lead Count",          "Leads",             "sum",  lambda x: f"{x:,.0f}"),
        ("💰 Acquisition Cost",    "Acquisition_Cost",  "sum",  lambda x: f"₹{x:,.0f}"),
        ("⚡ Engagement Score",    "Engagement_Score",  "mean", lambda x: f"{x:.2f}"),
        ("📈 Revenue Values",      "Revenue",           "sum",  lambda x: f"₹{x:,.0f}"),
        ("💎 Profit Values",       "Profit",            "sum",  lambda x: f"₹{x:,.0f}"),
    ]
    for title_, col_, agg_, fmt_ in metrics:
        if col_ in fdf.columns:
            int_metric_section(title_, col_, fdf, agg=agg_, fmt=fmt_)

    # Optional columns if they exist
    optional_sections = [
        ("🔥 Actively Engaged Users", "Engage of interest(actively  user engaged)", "sum", lambda x: f"{x:,.0f}"),
        ("💸 CAC (₹)",                "CAC(rupees)",                                 "mean", lambda x: f"₹{x:.2f}"),
        ("📊 CTR (%)",                "CTR",                                         "mean", lambda x: f"{x:.2f}%"),
        ("🏆 RPC (₹)",               "RPC(people cR)",                              "mean", lambda x: f"₹{x:,.0f}"),
    ]
    for title_, col_, agg_, fmt_ in optional_sections:
        if col_ in fdf.columns:
            int_metric_section(title_, col_, fdf, agg=agg_, fmt=fmt_)

    # Current vs Previous month
    if fdf["Date"].notna().any():
        st.markdown('<div class="sec-hdr">📅 Current vs Previous Month</div>', unsafe_allow_html=True)
        max_date   = fdf["Date"].max()
        curr_month = max_date.to_period("M")
        prev_month = curr_month - 1
        curr = fdf[fdf["Month"] == curr_month]
        prev = fdf[fdf["Month"] == prev_month]
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown(f"**Current: {curr_month}** · {len(curr):,} records")
            for lbl, cv, pv in [
                ("Impressions",  curr["Impressions"].sum()  if "Impressions" in curr.columns else 0,  prev["Impressions"].sum()  if "Impressions" in prev.columns else 0),
                ("Clicks",       curr["Clicks"].sum()       if "Clicks" in curr.columns else 0,       prev["Clicks"].sum()       if "Clicks" in prev.columns else 0),
                ("Conversions",  curr["Conversions"].sum()  if "Conversions" in curr.columns else 0,  prev["Conversions"].sum()  if "Conversions" in prev.columns else 0),
                ("Revenue ₹",    curr["Revenue"].sum()      if "Revenue" in curr.columns else 0,      prev["Revenue"].sum()      if "Revenue" in prev.columns else 0),
                ("Profit ₹",     curr["Profit"].sum()       if "Profit" in curr.columns else 0,       prev["Profit"].sum()       if "Profit" in prev.columns else 0),
            ]:
                d = delta_pct(cv, pv)
                arrow, color = ("▲","#10b981") if d >= 0 else ("▼","#ef4444")
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;background:#0f1e35;padding:8px 12px;border-radius:6px;margin:3px 0;">
                    <span style="color:#64748b;font-size:12px;">{lbl}</span>
                    <span style="color:white;font-weight:700;">{cv:,.0f}</span>
                    <span style="color:{color};font-size:12px;">{arrow} {abs(d):.1f}%</span>
                </div>""", unsafe_allow_html=True)
        with mc2:
            camp_trend = fdf[fdf["Month"].isin([curr_month, prev_month])].groupby(["Month_str","Campaign_Type"])["Revenue"].sum().reset_index()
            fig = px.bar(camp_trend, x="Campaign_Type", y="Revenue", color="Month_str",
                         barmode="group", template="plotly_dark", color_discrete_sequence=COLOR_SEQ,
                         title="Revenue: Current vs Previous Month")
            fig.update_layout(height=300, margin=dict(t=40,b=4,l=4,r=4),
                               plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                               font=dict(color="#94a3b8", size=10))
            st.plotly_chart(fig, use_container_width=True)

    # Full data table
    st.markdown('<div class="sec-hdr">📋 Full Analyst Data Table</div>', unsafe_allow_html=True)
    display_cols = [c for c in ["Campaign_ID","Campaign_Type","Channel_Used","Customer_Segment",
                                 "Impressions","Clicks","Leads","Conversions","Revenue",
                                 "Profit","Acquisition_Cost","Engagement_Score","Date"] if c in fdf.columns]
    st.dataframe(fdf[display_cols].sort_values("Revenue", ascending=False) if "Revenue" in fdf.columns else fdf[display_cols],
                 use_container_width=True, height=380)

    st.download_button("⬇ Download Internal Report", fdf.to_csv(index=False),
                       "internal_analytics_report.csv", "text/csv")


# ══════════════════════════════════════════════════════════════
# SECTION 3 — MARKETING ANALYST  (Marketing_Analyst.py)
# ══════════════════════════════════════════════════════════════
def _ma_kpi_card(label, val_str, sub, bc, bch, bs, bd=None, glow="kcard-glow"):
    def tags(rows, cls):
        return "".join(f'<span class="ktag {cls}">{n}: {v}</span>' for n,v in rows)
    dur_html = f'<div class="krow-label">⏱ Duration</div>{tags(bd,"ktag-o")}' if bd else ""
    return f"""
    <div class="kcard {glow}">
        <div class="klabel">{label}</div>
        <div class="kval">{val_str}</div>
        <div class="ksub">{sub}</div>
        <div class="kdivider"></div>
        <div class="krow-label">📢 Campaign</div>{tags(bc,"ktag-b")}
        <div class="krow-label">📡 Channel</div>{tags(bch,"ktag-g")}
        <div class="krow-label">👥 Segment</div>{tags(bs,"ktag-p")}
        {dur_html}
    </div>"""

def _ma_top_rows(col, fdf, n=3, agg="sum", fmt_fn=fmt_ind):
    def _top(grp):
        s = fdf.groupby(grp)[col].sum() if agg=="sum" else fdf.groupby(grp)[col].mean()
        return [(nm, fmt_fn(v)) for nm,v in s.sort_values(ascending=False).head(n).items()]
    dur_col = "Duration_Bucket" if "Duration_Bucket" in fdf.columns else "Campaign_Type"
    return _top("Campaign_Type"), _top("Channel_Used"), _top("Customer_Segment"), _top(dur_col)

def _ma_render_section(title, col, fdf, agg="sum", fmt_fn=fmt_ind, glow="kcard-glow"):
    st.markdown(f'<div class="sec-hdr">{title}</div>', unsafe_allow_html=True)
    if col not in fdf.columns: st.info(f"Column `{col}` not in dataset."); return
    total = fdf[col].sum() if agg=="sum" else fdf[col].mean()
    avg   = fdf[col].mean() if agg=="sum" else fdf[col].std()
    bc, bch, bs, bd = _ma_top_rows(col, fdf, agg=agg, fmt_fn=fmt_fn)
    sub   = f"Avg: {fmt_fn(avg)}" if agg=="sum" else f"Std: {fmt_fn(avg)}"

    c1, c2, c3, c4 = st.columns([1.3, 1.1, 1.1, 1.1])
    with c1:
        st.markdown(_ma_kpi_card(col.replace("_"," ").title(), fmt_fn(total), sub, bc, bch, bs, bd, glow),
                    unsafe_allow_html=True)
        if fdf["Date"].notna().any():
            month_data = (fdf.dropna(subset=["Date"]).groupby("Month_sort")[col].sum()
                          if agg=="sum" else
                          fdf.dropna(subset=["Date"]).groupby("Month_sort")[col].mean())
            if len(month_data) >= 2:
                months = sorted(month_data.index)[-4:]
                rows = ""
                for i, m in enumerate(months):
                    v = month_data[m]; pv = month_data[months[i-1]] if i>0 else v
                    d = delta_pct(v, pv) if i>0 else 0
                    rows += f"""<div class="mrow">
                        <span class="mrow-label">📅 {m}</span>
                        <span class="mrow-val">{fmt_fn(v)}</span>
                        {delta_html(d) if i>0 else '<span style="color:#475569;font-size:10px;">base</span>'}
                    </div>"""
                st.markdown(f'<div style="margin-top:6px;">{rows}</div>', unsafe_allow_html=True)

    with c2:
        gdf = (fdf.groupby("Campaign_Type")[col].sum() if agg=="sum"
               else fdf.groupby("Campaign_Type")[col].mean()).reset_index()
        fig = px.bar(gdf, x="Campaign_Type", y=col, color="Campaign_Type",
                     color_discrete_sequence=COLOR_SEQ, template="plotly_dark")
        st.plotly_chart(slim_fig(fig, "By Campaign"), use_container_width=True)

    with c3:
        gdf2 = (fdf.groupby("Channel_Used")[col].sum() if agg=="sum"
                else fdf.groupby("Channel_Used")[col].mean()).reset_index()
        fig2 = px.bar(gdf2, x=col, y="Channel_Used", orientation="h",
                      color="Channel_Used", color_discrete_sequence=COLOR_SEQ, template="plotly_dark")
        fig2.update_layout(height=220, margin=dict(t=32,b=4,l=4,r=4), showlegend=False,
                           plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                           font=dict(color="#94a3b8", size=9),
                           title=dict(text="By Channel", font=dict(size=11, color="#94a3b8"), x=0.5))
        st.plotly_chart(fig2, use_container_width=True)

    with c4:
        dur_label_col = "Duration_Label" if "Duration_Label" in fdf.columns else "Campaign_Type"
        gdf3 = (fdf.groupby(["Customer_Segment", dur_label_col])[col].sum() if agg=="sum"
                else fdf.groupby(["Customer_Segment", dur_label_col])[col].mean()).reset_index()
        fig3 = px.bar(gdf3, x="Customer_Segment", y=col, color=dur_label_col,
                      barmode="group", color_discrete_sequence=["#3b82f6","#f59e0b"],
                      template="plotly_dark")
        st.plotly_chart(slim_fig(fig3, "Segment × Duration"), use_container_width=True)

def render_marketing():
    if not DATA_OK:
        st.error("❌ CSV not found.")
        return

    fdf = get_filtered()

    # Sub-page picker
    sub_nav = st.radio("📂 Marketing Analyst View", ["ROI Dashboard","Engagement Intelligence"],
                       horizontal=True, label_visibility="collapsed")

    if sub_nav == "ROI Dashboard":
        st.markdown(f"""<div class='hero'>
            <div class='hero-title'>💰 Investment ROI Dashboard</div>
            <div class='hero-sub'>Financial Performance · {len(fdf):,} records · ROI, CAC, RPC, Profit Analysis</div>
        </div>""", unsafe_allow_html=True)

        if fdf.empty:
            st.warning("No data with current filters.")
            return

        r1, r2, r3, r4, r5 = st.columns(5)
        kpis = [
            ("Total Revenue",      fdf["Revenue"].sum() if "Revenue" in fdf.columns else 0, "₹", "#3b82f6"),
            ("Total Profit",       fdf["Profit"].sum()  if "Profit"  in fdf.columns else 0, "₹", "#10b981"),
            ("Avg ROI",            fdf["ROI"].mean()    if "ROI"     in fdf.columns else 0, "%", "#8b5cf6"),
            ("Avg CAC",            fdf["CAC(rupees)"].mean() if "CAC(rupees)" in fdf.columns else 0, "₹", "#f59e0b"),
            ("Ret. Inv. Cost",     fdf["Return Of Investment Cost"].sum() if "Return Of Investment Cost" in fdf.columns else 0, "₹", "#ef4444"),
        ]
        for col_, (label, val, sym, color) in zip([r1,r2,r3,r4,r5], kpis):
            with col_:
                v_str = fmt_ind(val, "₹") if sym == "₹" else f"{val:.2f}%"
                st.markdown(f"""<div class="kcard" style="border-color:{color}30;box-shadow:0 0 16px {color}15;">
                    <div class="klabel">{label}</div>
                    <div class="kval" style="color:{color};">{v_str}</div>
                </div>""", unsafe_allow_html=True)

        for title_, col_, agg_, fmt_, glow_ in [
            ("💰 Acquisition Cost (₹)",         "Acquisition_Cost",             "sum",  lambda x: fmt_ind(x,"₹"), "kcard-glow"),
            ("📊 ROI (%)",                       "ROI",                          "mean", fmt_pct,                   "kcard-glow2"),
            ("💸 CAC — Customer Acq. Cost (₹)", "CAC(rupees)",                  "mean", lambda x: fmt_ind(x,"₹"), "kcard-glow3"),
            ("🏆 RPC — Revenue Per Click (₹)",  "RPC(people cR)",               "sum",  lambda x: fmt_ind(x,"₹"), "kcard-glow4"),
            ("📈 Revenue (₹)",                   "Revenue",                      "sum",  lambda x: fmt_ind(x,"₹"), "kcard-glow"),
            ("💎 Profit (₹)",                    "Profit",                       "sum",  lambda x: fmt_ind(x,"₹"), "kcard-glow2"),
            ("🔁 Return Investment Cost (₹)",    "Return Of Investment Cost",    "sum",  lambda x: fmt_ind(x,"₹"), "kcard-glow3"),
        ]:
            _ma_render_section(title_, col_, fdf, agg=agg_, fmt_fn=fmt_, glow=glow_)

        # Month-wise trend
        if fdf["Date"].notna().any():
            st.markdown('<div class="sec-hdr">📅 Month-Wise Financial Trend</div>', unsafe_allow_html=True)
            trend_cols = [c for c in ["Revenue","Profit","Acquisition_Cost","Return Of Investment Cost"] if c in fdf.columns]
            mdf = fdf.dropna(subset=["Date"]).groupby("Month_sort")[trend_cols].sum().reset_index()
            fig = go.Figure()
            for i, col_ in enumerate(trend_cols):
                fig.add_trace(go.Scatter(x=mdf["Month_sort"], y=mdf[col_], name=col_,
                                         mode="lines+markers",
                                         line=dict(color=COLOR_SEQ[i], width=2),
                                         marker=dict(size=5)))
            fig.update_layout(height=300, margin=dict(t=40,b=4,l=4,r=4),
                               plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                               font=dict(color="#94a3b8", size=10), showlegend=True,
                               title=dict(text="Monthly Trend", font=dict(size=12,color="#94a3b8"), x=0.5))
            fig.update_xaxes(gridcolor="#0f1e35"); fig.update_yaxes(gridcolor="#0f1e35")
            st.plotly_chart(fig, use_container_width=True)

    else:  # Engagement Intelligence
        st.markdown(f"""<div class='hero'>
            <div class='hero-title'>🎯 Engagement Intelligence Dashboard</div>
            <div class='hero-sub'>CTR · LCR · Engagement Score · Active Users · Duration Patterns · {len(fdf):,} records</div>
        </div>""", unsafe_allow_html=True)

        if fdf.empty:
            st.warning("No data with current filters.")
            return

        e1,e2,e3,e4,e5 = st.columns(5)
        ekpis = [
            ("Avg Engagement Score",  fdf["Engagement_Score"].mean()     if "Engagement_Score" in fdf.columns else 0, "%",  "#3b82f6"),
            ("Avg CTR",               fdf["CTR"].mean()                  if "CTR" in fdf.columns else 0,              "%",  "#8b5cf6"),
            ("Avg LCR",               fdf["LCR(people)"].mean()          if "LCR(people)" in fdf.columns else 0,      "%",  "#10b981"),
            ("Total Engaged Users",   fdf["Engage of interest(actively  user engaged)"].sum() if "Engage of interest(actively  user engaged)" in fdf.columns else 0, "", "#f59e0b"),
            ("Total Duration Earn",   fdf["Duration wise earn"].sum()    if "Duration wise earn" in fdf.columns else 0, "₹","#ef4444"),
        ]
        for col_, (label, val, sym, color) in zip([e1,e2,e3,e4,e5], ekpis):
            with col_:
                v_str = fmt_pct(val) if sym=="%" else fmt_ind(val, sym)
                st.markdown(f"""<div class="kcard" style="border-color:{color}30;box-shadow:0 0 16px {color}15;">
                    <div class="klabel">{label}</div>
                    <div class="kval" style="color:{color};">{v_str}</div>
                </div>""", unsafe_allow_html=True)

        for title_, col_, agg_, fmt_, glow_ in [
            ("⚡ Engagement Score",                                   "Engagement_Score",                             "mean", fmt_pct,                   "kcard-glow"),
            ("📊 CTR — Click Through Rate (%)",                      "CTR",                                          "mean", fmt_pct,                   "kcard-glow2"),
            ("🎯 LCR — Lead Conversion Rate (%)",                    "LCR(people)",                                  "mean", fmt_pct,                   "kcard-glow3"),
            ("🔥 Actively Engaged Users",                             "Engage of interest(actively  user engaged)",   "sum",  fmt_ind,                   "kcard-glow4"),
            ("⏱ Duration Wise Earn (₹)",                             "Duration wise earn",                           "sum",  lambda x: fmt_ind(x,"₹"), "kcard-glow"),
            ("💡 Ads Cost (₹)",                                       "Ads cost",                                     "sum",  lambda x: fmt_ind(x,"₹"), "kcard-glow2"),
        ]:
            _ma_render_section(title_, col_, fdf, agg=agg_, fmt_fn=fmt_, glow=glow_)

        # Heatmap
        if "Engagement_Score" in fdf.columns and fdf["Date"].notna().any():
            st.markdown('<div class="sec-hdr2">🗺 Engagement Heatmap: Segment × Campaign</div>', unsafe_allow_html=True)
            hm = fdf.groupby(["Customer_Segment","Campaign_Type"])["Engagement_Score"].mean().reset_index()
            hm_p = hm.pivot(index="Customer_Segment", columns="Campaign_Type", values="Engagement_Score")
            fig = go.Figure(data=go.Heatmap(
                z=hm_p.values, x=hm_p.columns.tolist(), y=hm_p.index.tolist(),
                colorscale="Blues",
                text=[[f"{v:.1f}" for v in row] for row in hm_p.values],
                texttemplate="%{text}", showscale=True
            ))
            fig.update_layout(height=300, margin=dict(t=40,b=4,l=4,r=4),
                               plot_bgcolor=PLOTLY_BG, paper_bgcolor=PLOTLY_BG,
                               font=dict(color="#94a3b8", size=10))
            st.plotly_chart(fig, use_container_width=True)

    st.download_button("⬇ Download Marketing Report", fdf.to_csv(index=False),
                       "marketing_analyst_report.csv", "text/csv")


# ══════════════════════════════════════════════════════════════
# SECTION 4 — AI CHATBOT  (PDF-based, Groq + FAISS)
# ══════════════════════════════════════════════════════════════
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"

CHATBOT_SYSTEM = """You are a helpful marketing campaign data analyst.
Answer ONLY from the PDF/data context provided. Be specific — use real names, numbers, and values.
If the data does not contain the answer, say "I couldn't find that in the provided document."
Format answers clearly with bullet points or short paragraphs."""

def render_chatbot():
    import requests

    st.markdown("""
    <div class='hero'>
        <div class='hero-title'>💬 AI Campaign Chatbot</div>
        <div class='hero-sub'>Upload a PDF campaign report · Ask anything · Powered by FAISS + Groq LLaMA</div>
    </div>""", unsafe_allow_html=True)

    # Config panel
    with st.expander("⚙️ Configuration", expanded="groq_key" not in st.session_state):
        groq_key = st.text_input("Groq API Key", type="password",
                                  value=st.session_state.get("groq_key",""),
                                  placeholder="gsk_…")
        if groq_key:
            st.session_state.groq_key = groq_key

    if "groq_key" not in st.session_state or not st.session_state.groq_key:
        st.info("🔑 Enter your Groq API key above to enable the chatbot. Get one free at https://console.groq.com")
        return

    # PDF upload
    pdf_file = st.file_uploader("📄 Upload PDF Campaign Report", type=["pdf"],
                                 key="pdf_upload")

    # Try to import PDF + FAISS libs
    try:
        import fitz          # PyMuPDF
        import faiss
        from sentence_transformers import SentenceTransformer
        LIBS_OK = True
    except ImportError as e:
        st.error(f"Missing library: {e}. Install with:\n\n"
                 "`pip install pymupdf faiss-cpu sentence-transformers`")
        LIBS_OK = False
        return

    @st.cache_resource
    def get_embedder():
        return SentenceTransformer("all-MiniLM-L6-v2")

    @st.cache_data
    def index_pdf(pdf_bytes):
        import fitz, faiss
        from sentence_transformers import SentenceTransformer
        doc    = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages  = [page.get_text() for page in doc]
        # Chunk by paragraph
        chunks = []
        for i, page_text in enumerate(pages):
            paras = [p.strip() for p in page_text.split("\n\n") if len(p.strip()) > 40]
            for p in paras:
                chunks.append(f"[Page {i+1}] {p}")
        if not chunks:
            return [], None, f"{len(pages)} pages (no extractable text)"

        model = get_embedder()
        embs  = model.encode(chunks, show_progress_bar=False).astype("float32")
        idx   = faiss.IndexFlatL2(embs.shape[1])
        idx.add(embs)
        summary = f"{len(pages)} pages · {len(chunks)} chunks indexed"
        return chunks, idx, summary

    def search_pdf(query, chunks, idx, k=5):
        model  = get_embedder()
        q_emb  = model.encode([query]).astype("float32")
        _, ids = idx.search(q_emb, k)
        return [chunks[i] for i in ids[0] if i < len(chunks)]

    def ask_groq(context, question, history):
        hist_text = ""
        for m in history[-6:]:
            role = "User" if m["role"]=="user" else "Assistant"
            hist_text += f"{role}: {m['text']}\n"
        payload = {
            "model": GROQ_MODEL,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": CHATBOT_SYSTEM},
                {"role": "user",   "content": f"PDF Context:\n{context}\n\nConversation:\n{hist_text}\nUser: {question}"},
            ],
        }
        headers = {"Authorization": f"Bearer {st.session_state.groq_key}",
                   "Content-Type": "application/json"}
        try:
            resp = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"⚠️ Groq error: {e}"

    # Index PDF
    if pdf_file:
        pdf_bytes = pdf_file.read()
        with st.spinner("🔍 Indexing PDF…"):
            chunks, idx, summary = index_pdf(pdf_bytes)

        if not chunks or idx is None:
            st.warning("⚠️ Could not extract text from the PDF (may be scanned/image-only).")
            return

        c1, c2, c3 = st.columns(3)
        c1.metric("File", pdf_file.name[:20] + "…" if len(pdf_file.name)>20 else pdf_file.name)
        c2.metric("Indexed", summary.split("·")[0].strip())
        c3.metric("Chunks",  summary.split("·")[1].strip() if "·" in summary else "—")
        st.divider()

        # Suggestions
        SUGGESTIONS = [
            "Summarise this document",
            "What are the key KPIs?",
            "Which campaign performed best?",
            "What is the total revenue?",
            "Top findings & recommendations",
            "What channels are discussed?",
        ]
        st.markdown('<p style="font-size:12px;color:#475569;margin-bottom:6px;">QUICK QUESTIONS</p>',
                    unsafe_allow_html=True)
        sq_cols = st.columns(3)
        for i, q in enumerate(SUGGESTIONS):
            if sq_cols[i % 3].button(q, key=f"sq_{i}", use_container_width=True):
                st.session_state["_pending_chat"] = q
                st.rerun()

        st.divider()

        # Chat history
        for msg in st.session_state.chat:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-bubble">🧑 {msg["text"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="ts ts-right">{msg["time"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-bubble">🤖 {msg["text"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="ts ts-left">{msg["time"]}</div>', unsafe_allow_html=True)
                if msg.get("sources"):
                    pills = "".join(f'<span class="pill">chunk {i+1}</span>'
                                    for i in range(len(msg["sources"])))
                    st.markdown(f"<div style='margin-bottom:4px'>{pills}</div>", unsafe_allow_html=True)
                    with st.expander("📄 View matched chunks"):
                        for j, s in enumerate(msg["sources"]):
                            st.text(f"{j+1}. {s[:300]}…" if len(s)>300 else f"{j+1}. {s}")

        # Input
        with st.form("chat_form", clear_on_submit=True):
            inp, btn = st.columns([5,1])
            query = inp.text_input("q", label_visibility="collapsed",
                                   placeholder="Ask anything about the PDF…")
            send  = btn.form_submit_button("Send ➤", use_container_width=True)

        if "_pending_chat" in st.session_state:
            query = st.session_state.pop("_pending_chat"); send = True

        if send and query and query.strip():
            q  = query.strip()
            ts = time.strftime("%H:%M")
            st.session_state.chat.append({"role":"user","text":q,"time":ts})
            with st.spinner("Thinking…"):
                top_chunks = search_pdf(q, chunks, idx, k=5)
                context    = "\n\n".join(top_chunks)
                answer     = ask_groq(context, q, st.session_state.chat)
            st.session_state.chat.append({
                "role":"bot","text":answer,"time":time.strftime("%H:%M"),"sources":top_chunks
            })
            st.rerun()

        if st.session_state.chat:
            if st.button("🗑️ Clear chat", use_container_width=True):
                st.session_state.chat = []
                st.rerun()
    else:
        st.markdown("""
        <div style='text-align:center; padding:60px 20px; color:#475569;'>
            <div style='font-size:48px;'>📄</div>
            <div style='font-size:18px; margin-top:12px; color:#64748b;'>Upload a PDF to start chatting</div>
            <div style='font-size:13px; margin-top:8px;'>Supports any campaign report, strategy doc, or analytics PDF</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════
sidebar_nav()

section = st.session_state.section
if   section == "home":        render_home()
elif section == "performance": render_performance()
elif section == "internal":    render_internal()
elif section == "marketing":   render_marketing()
elif section == "chatbot":     render_chatbot()