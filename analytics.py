import re
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Internal Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>
.stApp { background-color: #0b1120; color: white; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }
h1 { color: white !important; font-size: 36px; font-weight: 800; }
h2, h3 { color: #e2e8f0 !important; }

[data-testid="stMetricLabel"] { color: #9ca3af !important; font-size: 12px; font-weight: 600; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: white !important; font-size: 22px; font-weight: bold; }
[data-testid="stMetricDelta"] { font-size: 12px; }

section[data-testid="stSidebar"] { background: #111827; }
[data-testid="stDataFrame"] { background: #111827; border-radius: 10px; }

.kpi-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    text-align: center;
}
.kpi-label { color: #9ca3af; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.kpi-value { color: white; font-size: 24px; font-weight: 900; margin: 4px 0; }
.kpi-sub { color: #6b7280; font-size: 10px; margin-top: 2px; }
.kpi-tag { display: inline-block; background: #1d4ed8; color: white; border-radius: 4px; padding: 1px 6px; font-size: 10px; margin: 2px 1px; }
.kpi-tag-green { background: #065f46; }
.kpi-tag-purple { background: #4c1d95; }
.kpi-tag-orange { background: #92400e; }

.section-header {
    background: linear-gradient(90deg, #1d4ed8, transparent);
    border-left: 4px solid #3b82f6;
    padding: 8px 16px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0 12px 0;
    color: white;
    font-size: 18px;
    font-weight: 700;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }

.filter-info { background: #1e293b; border-radius: 8px; padding: 8px 12px; font-size: 12px; color: #9ca3af; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/compaign_analyst.csv")
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M")
    df["Month_str"] = df["Date"].dt.strftime("%Y-%m")
    return df

df = load_data()

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.markdown("## 🔍 Filters")

campaign_filter = st.sidebar.multiselect(
    "Campaign Type",
    sorted(df["Campaign_Type"].dropna().unique()),
    sorted(df["Campaign_Type"].dropna().unique())
)
channel_filter = st.sidebar.multiselect(
    "Channel Used",
    sorted(df["Channel_Used"].dropna().unique()),
    sorted(df["Channel_Used"].dropna().unique())
)
segment_filter = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Customer_Segment"].dropna().unique()),
    sorted(df["Customer_Segment"].dropna().unique())
)

fdf = df[
    df["Campaign_Type"].isin(campaign_filter) &
    df["Channel_Used"].isin(channel_filter) &
    df["Customer_Segment"].isin(segment_filter)
].copy()

# -------------------------------------------------
# PAGE HEADER
# -------------------------------------------------
st.markdown("""
<h1 style='text-align:center;'>📊 Internal Analytics Dashboard</h1>
<p style='text-align:center; color:#9ca3af; margin-bottom:20px;'>
Analyst-Level Campaign Intelligence · Drill-Down KPI View
</p>
""", unsafe_allow_html=True)

# Active filter display
ct_str = ", ".join(campaign_filter) if len(campaign_filter) < 5 else f"{len(campaign_filter)} types"
ch_str = ", ".join(channel_filter) if len(channel_filter) < 4 else f"{len(channel_filter)} channels"
sg_str = ", ".join(segment_filter) if len(segment_filter) < 4 else f"{len(segment_filter)} segments"
st.markdown(f'<div class="filter-info">🎯 Active Filters — Campaign: <b>{ct_str}</b> &nbsp;|&nbsp; Channel: <b>{ch_str}</b> &nbsp;|&nbsp; Segment: <b>{sg_str}</b> &nbsp;|&nbsp; Records: <b>{len(fdf):,}</b></div>', unsafe_allow_html=True)

# =================================================
# HELPER: build breakdown tags HTML
# =================================================
def breakdown_tags(series: pd.Series, top_n=4):
    counts = series.value_counts().head(top_n)
    tags = ""
    for name, cnt in counts.items():
        tags += f'<span class="kpi-tag">{name}: {cnt:,}</span>'
    return tags

def breakdown_tags_sum(grp_col, val_col, top_n=4, fmt="count"):
    gb = fdf.groupby(grp_col)[val_col]
    if fmt == "sum":
        s = gb.sum().sort_values(ascending=False).head(top_n)
        tags = "".join(f'<span class="kpi-tag kpi-tag-green">{n}: ₹{v:,.0f}</span>' for n, v in s.items())
    elif fmt == "mean":
        s = gb.mean().sort_values(ascending=False).head(top_n)
        tags = "".join(f'<span class="kpi-tag kpi-tag-purple">{n}: {v:,.1f}</span>' for n, v in s.items())
    else:
        s = gb.count().sort_values(ascending=False).head(top_n)
        tags = "".join(f'<span class="kpi-tag">{n}: {v:,}</span>' for n, v in s.items())
    return tags

# =================================================
# SECTION 1 — TOP-LEVEL COUNTS
# =================================================
st.markdown('<div class="section-header">📌 KPI Overview — Count Metrics</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    ct_counts = fdf["Campaign_Type"].value_counts()
    tags_html = "".join(f'<span class="kpi-tag">{n}: {v:,}</span>' for n, v in ct_counts.head(4).items())
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Records (Count ID)</div>
        <div class="kpi-value">{len(fdf):,}</div>
        <div class="kpi-sub">Campaign IDs</div>
        {tags_html}
    </div>""", unsafe_allow_html=True)

with c2:
    ct_n = fdf["Campaign_Type"].nunique()
    tags_html = "".join(f'<span class="kpi-tag kpi-tag-purple">{n}: {v:,}</span>' for n, v in fdf["Campaign_Type"].value_counts().head(4).items())
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Campaign Types</div>
        <div class="kpi-value">{ct_n}</div>
        <div class="kpi-sub">Unique types · {len(fdf):,} total</div>
        {tags_html}
    </div>""", unsafe_allow_html=True)

with c3:
    ch_n = fdf["Channel_Used"].nunique()
    tags_html = "".join(f'<span class="kpi-tag kpi-tag-green">{n}: {v:,}</span>' for n, v in fdf["Channel_Used"].value_counts().head(4).items())
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Channels Used</div>
        <div class="kpi-value">{ch_n}</div>
        <div class="kpi-sub">Unique channels · {len(fdf):,} total</div>
        {tags_html}
    </div>""", unsafe_allow_html=True)

with c4:
    seg_n = fdf["Customer_Segment"].nunique()
    tags_html = "".join(f'<span class="kpi-tag kpi-tag-orange">{n}: {v:,}</span>' for n, v in fdf["Customer_Segment"].value_counts().head(4).items())
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Customer Segments</div>
        <div class="kpi-value">{seg_n}</div>
        <div class="kpi-sub">Unique segments · {len(fdf):,} total</div>
        {tags_html}
    </div>""", unsafe_allow_html=True)

# =================================================
# KPI METRIC CARDS (2–10 & 13–16)
# =================================================
def kpi_block(label, value_str, sub, by_camp, by_chan, by_seg):
    """Render a full KPI card with 4-dimension breakdown."""
    camp_tags = "".join(f'<span class="kpi-tag">{n}: {v}</span>' for n, v in by_camp)
    chan_tags  = "".join(f'<span class="kpi-tag kpi-tag-green">{n}: {v}</span>' for n, v in by_chan)
    seg_tags   = "".join(f'<span class="kpi-tag kpi-tag-purple">{n}: {v}</span>' for n, v in by_seg)
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value_str}</div>
        <div class="kpi-sub">{sub}</div>
        <div style="margin-top:6px;">{camp_tags}</div>
        <div>{chan_tags}</div>
        <div>{seg_tags}</div>
    </div>"""

def top4_count(col, fmt_fn=lambda x: f"{x:,}"):
    camp = [(n, fmt_fn(v)) for n, v in fdf.groupby("Campaign_Type")[col].sum().sort_values(ascending=False).head(3).items()]
    chan  = [(n, fmt_fn(v)) for n, v in fdf.groupby("Channel_Used")[col].sum().sort_values(ascending=False).head(3).items()]
    seg   = [(n, fmt_fn(v)) for n, v in fdf.groupby("Customer_Segment")[col].sum().sort_values(ascending=False).head(3).items()]
    return camp, chan, seg

def top4_mean(col, fmt_fn=lambda x: f"{x:,.1f}"):
    camp = [(n, fmt_fn(v)) for n, v in fdf.groupby("Campaign_Type")[col].mean().sort_values(ascending=False).head(3).items()]
    chan  = [(n, fmt_fn(v)) for n, v in fdf.groupby("Channel_Used")[col].mean().sort_values(ascending=False).head(3).items()]
    seg   = [(n, fmt_fn(v)) for n, v in fdf.groupby("Customer_Segment")[col].mean().sort_values(ascending=False).head(3).items()]
    return camp, chan, seg

# ---- IMPRESSIONS ----
st.markdown('<div class="section-header">👁️ Impressions Count</div>', unsafe_allow_html=True)
total_imp = fdf["Impressions"].sum()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_count("Impressions")
with c1:
    st.markdown(kpi_block("Total Impressions", f"{total_imp:,.0f}", f"Avg per record: {fdf['Impressions'].mean():,.0f}", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["Impressions"].sum().reset_index(),
                 x="Campaign_Type", y="Impressions", color="Campaign_Type",
                 template="plotly_dark", title="by Campaign Type")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["Impressions"].sum().reset_index(),
                 x="Channel_Used", y="Impressions", color="Channel_Used",
                 template="plotly_dark", title="by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values="Impressions", hole=0.5,
                 template="plotly_dark", title="by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=True, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# ---- CLICKS ----
st.markdown('<div class="section-header">🖱️ Clicks Count</div>', unsafe_allow_html=True)
total_clicks = fdf["Clicks"].sum()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_count("Clicks")
with c1:
    st.markdown(kpi_block("Total Clicks", f"{total_clicks:,.0f}", f"Avg per record: {fdf['Clicks'].mean():,.0f}", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["Clicks"].sum().reset_index(),
                 x="Campaign_Type", y="Clicks", color="Campaign_Type",
                 template="plotly_dark", title="by Campaign Type")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["Clicks"].sum().reset_index(),
                 x="Channel_Used", y="Clicks", color="Channel_Used",
                 template="plotly_dark", title="by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values="Clicks", hole=0.5,
                 template="plotly_dark", title="by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=True, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# ---- CONVERSIONS ----
st.markdown('<div class="section-header">🔄 Conversions Count</div>', unsafe_allow_html=True)
total_conv = fdf["Conversions"].sum()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_count("Conversions")
with c1:
    conv_rate = (fdf["Conversions"].sum() / fdf["Clicks"].replace(0,1).sum()) * 100
    st.markdown(kpi_block("Total Conversions", f"{total_conv:,.0f}", f"Conv. Rate: {conv_rate:.1f}%", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["Conversions"].sum().reset_index(),
                 x="Campaign_Type", y="Conversions", color="Campaign_Type",
                 template="plotly_dark", title="by Campaign Type")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["Conversions"].sum().reset_index(),
                 x="Channel_Used", y="Conversions", color="Channel_Used",
                 template="plotly_dark", title="by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values="Conversions", hole=0.5,
                 template="plotly_dark", title="by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=True, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# ---- LEADS ----
st.markdown('<div class="section-header">🎯 Lead Count</div>', unsafe_allow_html=True)
total_leads = fdf["Leads"].sum()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_count("Leads")
with c1:
    lcr = fdf["LCR(people)"].mean()
    st.markdown(kpi_block("Total Leads", f"{total_leads:,.0f}", f"Avg LCR: {lcr:.1f}%", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["Leads"].sum().reset_index(),
                 x="Campaign_Type", y="Leads", color="Campaign_Type",
                 template="plotly_dark", title="by Campaign Type")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["Leads"].sum().reset_index(),
                 x="Channel_Used", y="Leads", color="Channel_Used",
                 template="plotly_dark", title="by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values="Leads", hole=0.5,
                 template="plotly_dark", title="by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=True, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# ---- ACQUISITION COST ----
st.markdown('<div class="section-header">💰 Acquisition Cost</div>', unsafe_allow_html=True)
total_ac = fdf["Acquisition_Cost"].sum()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_count("Acquisition_Cost", fmt_fn=lambda x: f"₹{x:,.0f}")
with c1:
    st.markdown(kpi_block("Total Acquisition Cost", f"₹{total_ac:,.0f}", f"Avg: ₹{fdf['Acquisition_Cost'].mean():,.1f}", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["Acquisition_Cost"].sum().reset_index(),
                 x="Campaign_Type", y="Acquisition_Cost", color="Campaign_Type",
                 template="plotly_dark", title="by Campaign Type")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["Acquisition_Cost"].sum().reset_index(),
                 x="Channel_Used", y="Acquisition_Cost", color="Channel_Used",
                 template="plotly_dark", title="by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values="Acquisition_Cost", hole=0.5,
                 template="plotly_dark", title="by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=True, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# ---- ENGAGEMENT SCORE ----
st.markdown('<div class="section-header">⚡ Engagement Score</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_mean("Engagement_Score")
with c1:
    st.markdown(kpi_block("Avg Engagement Score", f"{fdf['Engagement_Score'].mean():.2f}",
                           f"Max: {fdf['Engagement_Score'].max():.1f} · Min: {fdf['Engagement_Score'].min():.1f}", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.box(fdf, x="Campaign_Type", y="Engagement_Score", color="Campaign_Type",
                 template="plotly_dark", title="Distribution by Campaign")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.box(fdf, x="Channel_Used", y="Engagement_Score", color="Channel_Used",
                 template="plotly_dark", title="Distribution by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.violin(fdf, x="Customer_Segment", y="Engagement_Score", color="Customer_Segment",
                    template="plotly_dark", title="Distribution by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# ---- REVENUE ----
st.markdown('<div class="section-header">📈 Revenue Values</div>', unsafe_allow_html=True)
total_rev = fdf["Revenue"].sum()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_count("Revenue", fmt_fn=lambda x: f"₹{x:,.0f}")
with c1:
    st.markdown(kpi_block("Total Revenue", f"₹{total_rev:,.0f}", f"Avg: ₹{fdf['Revenue'].mean():,.0f}", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["Revenue"].sum().reset_index(),
                 x="Campaign_Type", y="Revenue", color="Campaign_Type",
                 template="plotly_dark", title="by Campaign Type")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["Revenue"].sum().reset_index(),
                 x="Channel_Used", y="Revenue", color="Channel_Used",
                 template="plotly_dark", title="by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values="Revenue", hole=0.5,
                 template="plotly_dark", title="by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=True, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# ---- PROFIT ----
st.markdown('<div class="section-header">💎 Profit Values</div>', unsafe_allow_html=True)
total_profit = fdf["Profit"].sum()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_count("Profit", fmt_fn=lambda x: f"₹{x:,.0f}")
with c1:
    margin = (fdf["Profit"].sum() / fdf["Revenue"].replace(0,1).sum()) * 100
    st.markdown(kpi_block("Total Profit", f"₹{total_profit:,.0f}", f"Margin: {margin:.1f}%", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["Profit"].sum().reset_index(),
                 x="Campaign_Type", y="Profit", color="Campaign_Type",
                 template="plotly_dark", title="by Campaign Type")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["Profit"].sum().reset_index(),
                 x="Channel_Used", y="Profit", color="Channel_Used",
                 template="plotly_dark", title="by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values="Profit", hole=0.5,
                 template="plotly_dark", title="by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=True, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 11 — CURRENT vs PREVIOUS MONTH
# =================================================
st.markdown('<div class="section-header">📅 Current Month vs Previous Month</div>', unsafe_allow_html=True)

if fdf["Date"].notna().any():
    max_date = fdf["Date"].max()
    curr_month = max_date.to_period("M")
    prev_month = curr_month - 1

    curr = fdf[fdf["Month"] == curr_month]
    prev = fdf[fdf["Month"] == prev_month]

    def delta_pct(a, b):
        return ((a - b) / b * 100) if b != 0 else 0

    metrics_m = [
        ("Count (Records)", len(curr), len(prev), ""),
        ("Impressions", curr["Impressions"].sum(), prev["Impressions"].sum(), ""),
        ("Clicks", curr["Clicks"].sum(), prev["Clicks"].sum(), ""),
        ("Conversions", curr["Conversions"].sum(), prev["Conversions"].sum(), ""),
        ("Leads", curr["Leads"].sum(), prev["Leads"].sum(), ""),
        ("Revenue ₹", curr["Revenue"].sum(), prev["Revenue"].sum(), "₹"),
        ("Profit ₹", curr["Profit"].sum(), prev["Profit"].sum(), "₹"),
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Current Month: {curr_month}** · {len(curr):,} records")
        for label, cv, pv, sym in metrics_m:
            d = delta_pct(cv, pv)
            arrow = "▲" if d >= 0 else "▼"
            color = "#10b981" if d >= 0 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;background:#1e293b;padding:8px 12px;border-radius:6px;margin:3px 0;">
                <span style="color:#9ca3af;font-size:12px;">{label}</span>
                <span style="color:white;font-weight:700;">{sym}{cv:,.0f}</span>
                <span style="color:{color};font-size:12px;">{arrow} {abs(d):.1f}%</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        # Campaign type breakdown per month
        camp_trend = fdf[fdf["Month"].isin([curr_month, prev_month])].groupby(["Month_str", "Campaign_Type"])["Revenue"].sum().reset_index()
        fig = px.bar(camp_trend, x="Campaign_Type", y="Revenue", color="Month_str", barmode="group",
                     template="plotly_dark", title="Revenue: Current vs Previous Month by Campaign")
        fig.update_layout(height=300, margin=dict(t=40, b=0, l=0, r=0), plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
        st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 12 — ENGAGE OF INTEREST (ACTIVELY)
# =================================================
st.markdown('<div class="section-header">🔥 Engaged & Actively Interested Users</div>', unsafe_allow_html=True)
eng_col = "Engage of interest(actively  user engaged)"
total_eng = fdf[eng_col].sum()
avg_eng = fdf[eng_col].mean()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_count(eng_col, fmt_fn=lambda x: f"{x:,.1f}")
with c1:
    st.markdown(kpi_block("Actively Engaged Users", f"{total_eng:,.0f}", f"Avg: {avg_eng:.2f}", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")[eng_col].sum().reset_index(),
                 x="Campaign_Type", y=eng_col, color="Campaign_Type",
                 template="plotly_dark", title="by Campaign Type")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")[eng_col].sum().reset_index(),
                 x="Channel_Used", y=eng_col, color="Channel_Used",
                 template="plotly_dark", title="by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values=eng_col, hole=0.5,
                 template="plotly_dark", title="by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 13 — CAC (Customer Acquisition Cost)
# =================================================
st.markdown('<div class="section-header">💸 CAC — Customer Acquisition Cost (₹)</div>', unsafe_allow_html=True)
avg_cac = fdf["CAC(rupees)"].mean()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_mean("CAC(rupees)", fmt_fn=lambda x: f"₹{x:.1f}")
with c1:
    st.markdown(kpi_block("Avg CAC (₹)", f"₹{avg_cac:.2f}", f"Total spend: ₹{fdf['CAC(rupees)'].sum():,.0f}", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["CAC(rupees)"].mean().reset_index(),
                 x="Campaign_Type", y="CAC(rupees)", color="Campaign_Type",
                 template="plotly_dark", title="Avg CAC by Campaign")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["CAC(rupees)"].mean().reset_index(),
                 x="Channel_Used", y="CAC(rupees)", color="Channel_Used",
                 template="plotly_dark", title="Avg CAC by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.scatter(fdf, x="CAC(rupees)", y="Conversions", color="Customer_Segment",
                     template="plotly_dark", title="CAC vs Conversions")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 14 — CTR (Click-Through Rate)
# =================================================
st.markdown('<div class="section-header">📊 CTR — Click-Through Rate</div>', unsafe_allow_html=True)
avg_ctr = fdf["CTR"].mean()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_mean("CTR", fmt_fn=lambda x: f"{x:.1f}%")
with c1:
    st.markdown(kpi_block("Avg CTR", f"{avg_ctr:.2f}%", f"Max: {fdf['CTR'].max():.1f}% · Min: {fdf['CTR'].min():.1f}%", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["CTR"].mean().reset_index(),
                 x="Campaign_Type", y="CTR", color="Campaign_Type",
                 template="plotly_dark", title="Avg CTR by Campaign")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["CTR"].mean().reset_index(),
                 x="Channel_Used", y="CTR", color="Channel_Used",
                 template="plotly_dark", title="Avg CTR by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.box(fdf, x="Customer_Segment", y="CTR", color="Customer_Segment",
                 template="plotly_dark", title="CTR Distribution by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SECTION 15 — RPC (Revenue Per Click / People CR)
# =================================================
st.markdown('<div class="section-header">🏆 RPC — Revenue Per Click (People CR)</div>', unsafe_allow_html=True)
avg_rpc = fdf["RPC(people cR)"].mean()
c1, c2, c3, c4 = st.columns(4)
bc, bch, bs = top4_mean("RPC(people cR)", fmt_fn=lambda x: f"₹{x:,.0f}")
with c1:
    st.markdown(kpi_block("Avg RPC (₹)", f"₹{avg_rpc:,.0f}", f"Total: ₹{fdf['RPC(people cR)'].sum():,.0f}", bc, bch, bs), unsafe_allow_html=True)
with c2:
    fig = px.bar(fdf.groupby("Campaign_Type")["RPC(people cR)"].mean().reset_index(),
                 x="Campaign_Type", y="RPC(people cR)", color="Campaign_Type",
                 template="plotly_dark", title="Avg RPC by Campaign")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    fig = px.bar(fdf.groupby("Channel_Used")["RPC(people cR)"].mean().reset_index(),
                 x="Channel_Used", y="RPC(people cR)", color="Channel_Used",
                 template="plotly_dark", title="Avg RPC by Channel")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False, plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.pie(fdf, names="Customer_Segment", values="RPC(people cR)", hole=0.5,
                 template="plotly_dark", title="RPC Share by Segment")
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=0, r=0), plot_bgcolor="#0b1120", paper_bgcolor="#0b1120")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# SUMMARY TABLE
# =================================================
st.markdown('<div class="section-header">📋 Full Analyst Data Table</div>', unsafe_allow_html=True)

display_cols = ["Campaign_ID", "Campaign_Type", "Channel_Used", "Customer_Segment",
                "Impressions", "Clicks", "Leads", "Conversions", "Revenue",
                "Profit", "CAC(rupees)", "CTR", "RPC(people cR)",
                "Engage of interest(actively  user engaged)", "Date"]

st.dataframe(
    fdf[display_cols].sort_values("Profit", ascending=False),
    use_container_width=True,
    height=400
)

st.markdown(f"""
<div style="text-align:center;color:#4b5563;margin-top:20px;font-size:12px;">
    Internal Analytics Dashboard · {len(fdf):,} records loaded · All values in ₹ INR
</div>
""", unsafe_allow_html=True)