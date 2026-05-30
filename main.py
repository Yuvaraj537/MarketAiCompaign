import re
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Marketing Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #0b1120;
    color: white;
}

/* Padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* Main Title */
h1 {
    color: #ffffff !important;
    font-size: 42px !important;
    font-weight: 800 !important;
}

/* Subtitles */
h2, h3 {
    color: #f3f4f6 !important;
    font-weight: 700 !important;
}

/* KPI Cards */
div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #111827, #1f2937);
    border: 1px solid #374151;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    transition: 0.3s ease-in-out;
}

/* KPI Hover */
div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    border: 1px solid #10b981;
    box-shadow: 0 0 15px rgba(16,185,129,0.4);
}

/* KPI LABEL */
[data-testid="stMetricLabel"] {
    color: white !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* KPI VALUE */
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 32px !important;
    font-weight: bold !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #0f172a);
    border-right: 1px solid #1f2937;
}

/* Sidebar Text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: white !important;
}

/* Multiselect */
.stMultiSelect div[data-baseweb="select"] {
    background-color: #1f2937 !important;
    border-radius: 10px;
    border: 1px solid #374151;
}

/* Selected Tags */
[data-baseweb="tag"] {
    background-color: #10b981 !important;
    color: white !important;
}

/* Chart Container */
.element-container:has(.js-plotly-plot) {
    background: #111827;
    padding: 15px;
    border-radius: 18px;
    border: 1px solid #1f2937;
    margin-bottom: 20px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: #111827;
    border-radius: 15px;
    border: 1px solid #374151;
    padding: 10px;
}

/* Download Button */
.stDownloadButton button {
    background: linear-gradient(90deg, #10b981, #059669);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: bold;
}

/* Download Button Hover */
.stDownloadButton button:hover {
    background: linear-gradient(90deg, #059669, #047857);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #111827;
}

::-webkit-scrollbar-thumb {
    background: #10b981;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.markdown("""
<h1 style='text-align:center;'>
🚀 AI Marketing Intelligence Dashboard
</h1>

<p style='text-align:center; color:#9ca3af; font-size:18px;'>
Real-Time Campaign Analytics & AI Insights
</p>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv("data/compaign_analyst.csv")

    except FileNotFoundError:
        st.error("❌ CSV File Not Found")
        st.stop()

    # Clean Columns
    df.columns = [
        re.sub(r"[^\w]", "_", col.strip())
        for col in df.columns
    ]

    # Categories
    campaign_categories = [
        "Social Media",
        "Paid Ads",
        "Influencer",
        "Email",
        "CEO"
    ]

    channel_categories = [
        "WhatsApp",
        "YouTube",
        "Instagram",
        "Email",
        "Facebook",
        "Google"
    ]

    customer_categories = [
        "College Student",
        "Tier 2 City Customers",
        "Youth",
        "Working Women",
        "Premium Shoppers"
    ]

    # Assign Values
    df["Campaign_Type"] = [
        campaign_categories[i % len(campaign_categories)]
        for i in range(len(df))
    ]

    df["Channel_Used"] = [
        channel_categories[i % len(channel_categories)]
        for i in range(len(df))
    ]

    df["Customer_Segment"] = [
        customer_categories[i % len(customer_categories)]
        for i in range(len(df))
    ]

    # Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # Metrics
    df["Calculated_CTR"] = (
        df["Clicks"] / df["Impressions"].replace(0, 1)
    ) * 100

    df["Conversion_Rate"] = (
        df["Conversions"] / df["Clicks"].replace(0, 1)
    ) * 100

    df["CPA"] = (
        df["Acquisition_Cost"] /
        df["Conversions"].replace(0, 1)
    )

    df["Calculated_Profit"] = (
        df["Revenue"] - df["Acquisition_Cost"]
    )

    df["ROAS"] = (
        df["Revenue"] /
        df["Acquisition_Cost"].replace(0, 1)
    )

    return df

df = load_data()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("🎛 Dashboard Filters")

campaign_filter = st.sidebar.multiselect(
    "📢 Campaign Type",
    options=df["Campaign_Type"].unique(),
    default=df["Campaign_Type"].unique()
)

channel_filter = st.sidebar.multiselect(
    "📡 Select Channel",
    options=df["Channel_Used"].unique(),
    default=df["Channel_Used"].unique()
)

segment_filter = st.sidebar.multiselect(
    "👥 Customer Segment",
    options=df["Customer_Segment"].unique(),
    default=df["Customer_Segment"].unique()
)

# -------------------------------------------------
# FILTER DATA
# -------------------------------------------------
filtered_df = df[
    (df["Campaign_Type"].isin(campaign_filter)) &
    (df["Channel_Used"].isin(channel_filter)) &
    (df["Customer_Segment"].isin(segment_filter))
]

# -------------------------------------------------
# FORMAT FUNCTION
# -------------------------------------------------
def format_indian_currency(value):

    if value >= 10000000:
        return f"₹{value/10000000:.2f} Cr"

    elif value >= 100000:
        return f"₹{value/100000:.2f} L"

    elif value >= 1000:
        return f"₹{value/1000:.2f} K"

    else:
        return f"₹{value:.0f}"

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("📌 KPI Overview")

total_revenue = filtered_df["Revenue"].sum()
total_cost = filtered_df["Acquisition_Cost"].sum()
total_profit = filtered_df["Calculated_Profit"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Revenue",
    format_indian_currency(total_revenue)
)

col2.metric(
    "Cost",
    format_indian_currency(total_cost)
)

col3.metric(
    "Profit",
    format_indian_currency(total_profit)
)

col4.metric(
    "ROAS",
    f"{filtered_df['ROAS'].mean():.2f}x"
)

col5.metric(
    "CTR",
    f"{filtered_df['Calculated_CTR'].mean():.2f}%"
)

st.markdown("---")

# -------------------------------------------------
# CHANNEL PERFORMANCE
# -------------------------------------------------
col_a, col_b = st.columns(2)

with col_a:

    st.subheader("📡 Channel Performance")

    channel_data = (
        filtered_df.groupby("Channel_Used")
        [["Revenue", "Acquisition_Cost"]]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        channel_data,
        x="Channel_Used",
        y=["Revenue", "Acquisition_Cost"],
        barmode="group",
        template="plotly_dark"
    )

    fig1.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col_b:

    st.subheader("🎯 Campaign Profit")

    campaign_data = (
        filtered_df.groupby("Campaign_Type")
        ["Calculated_Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        campaign_data,
        x="Campaign_Type",
        y="Calculated_Profit",
        color="Calculated_Profit",
        template="plotly_dark"
    )

    fig2.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# REVENUE TREND
# -------------------------------------------------
st.subheader("📅 Revenue Trend")

trend_data = (
    filtered_df.groupby("Date")["Revenue"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    trend_data,
    x="Date",
    y="Revenue",
    template="plotly_dark"
)

fig3.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# PIE CHART
# -------------------------------------------------
st.subheader("👥 Segment Revenue Share")

fig4 = px.pie(
    filtered_df,
    names="Customer_Segment",
    values="Revenue",
    hole=0.4,
    template="plotly_dark"
)

fig4.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white"
)

st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------
# SCATTER PLOT
# -------------------------------------------------
st.subheader("💡 Engagement vs Revenue")

fig5 = px.scatter(
    filtered_df,
    x="Engagement_Score",
    y="Revenue",
    size="Clicks",
    color="Campaign_Type",
    template="plotly_dark",
    hover_data=["Channel_Used", "ROAS"]
)

fig5.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white"
)

st.plotly_chart(fig5, use_container_width=True)

# -------------------------------------------------
# TOP CAMPAIGNS
# -------------------------------------------------
st.subheader("🏆 Top 10 Campaigns")

top_campaigns = (
    filtered_df.sort_values(
        by="Calculated_Profit",
        ascending=False
    )
    [
        [
            "Campaign_ID",
            "Campaign_Type",
            "Channel_Used",
            "Revenue",
            "Acquisition_Cost",
            "Calculated_Profit",
            "ROAS"
        ]
    ]
    .head(10)
)

st.dataframe(
    top_campaigns,
    use_container_width=True
)

# -------------------------------------------------
# AI INSIGHTS
# -------------------------------------------------
st.markdown("---")
st.subheader("🤖 AI Insights")

best_channel = (
    filtered_df.groupby("Channel_Used")["ROAS"]
    .mean()
    .idxmax()
)

worst_channel = (
    filtered_df.groupby("Channel_Used")["CPA"]
    .mean()
    .idxmax()
)

best_segment = (
    filtered_df.groupby("Customer_Segment")["Revenue"]
    .sum()
    .idxmax()
)

st.success(f"✅ Best ROAS Channel: {best_channel}")
st.warning(f"⚠ Highest CPA Channel: {worst_channel}")
st.info(f"👥 Top Revenue Segment: {best_segment}")

# -------------------------------------------------
# DOWNLOAD BUTTON
# -------------------------------------------------
st.markdown("---")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Report",
    data=csv,
    file_name="marketing_dashboard_report.csv",
    mime="text/csv"
)
