import re
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Marketing Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #0f1117;
}

h1, h2, h3 {
    color: white;
}

.stMetric {
    background: #1e2130;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #2e3349;
}

.stMetricValue {
    color: #00ffcc !important;
}

.stMetricLabel {
    color: #aab0c5 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("📊 AI Marketing Intelligence Dashboard")
st.caption("Real-Time Campaign Analytics Dashboard")

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

    # Clean column names
    df.columns = [re.sub(r"[^\w]", "_", col.strip()) for col in df.columns]

    # Convert date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # Derived Metrics
    df["Calculated_CTR"] = (
        df["Clicks"] / df["Impressions"].replace(0, 1)
    ) * 100

    df["Conversion_Rate"] = (
        df["Conversions"] / df["Clicks"].replace(0, 1)
    ) * 100

    df["CPA"] = (
        df["Acquisition_Cost"] / df["Conversions"].replace(0, 1)
    )

    df["Calculated_Profit"] = (
        df["Revenue"] - df["Acquisition_Cost"]
    )

    df["ROAS"] = (
        df["Revenue"] / df["Acquisition_Cost"].replace(0, 1)
    )

    return df


df = load_data()

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.header("🎛 Dashboard Filters")

channel_filter = st.sidebar.multiselect(
    "Select Channel",
    options=df["Channel_Used"].unique(),
    default=df["Channel_Used"].unique()
)

campaign_filter = st.sidebar.multiselect(
    "Campaign Type",
    options=df["Campaign_Type"].unique(),
    default=df["Campaign_Type"].unique()
)

segment_filter = st.sidebar.multiselect(
    "Customer Segment",
    options=df["Customer_Segment"].unique(),
    default=df["Customer_Segment"].unique()
)

# -------------------------------------------------
# FILTER DATA
# -------------------------------------------------
filtered_df = df[
    (df["Channel_Used"].isin(channel_filter)) &
    (df["Campaign_Type"].isin(campaign_filter)) &
    (df["Customer_Segment"].isin(segment_filter))
]

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("📌 KPI Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Revenue",
    f"₹{filtered_df['Revenue'].sum():,.0f}"
)

col2.metric(
    "💸 Cost",
    f"₹{filtered_df['Acquisition_Cost'].sum():,.0f}"
)

col3.metric(
    "📈 Profit",
    f"₹{filtered_df['Calculated_Profit'].sum():,.0f}"
)

col4.metric(
    "🎯 Avg ROAS",
    f"{filtered_df['ROAS'].mean():.2f}x"
)

col5.metric(
    "🔁 Avg CTR",
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
        template="plotly_dark",
        title="Revenue vs Cost by Channel"
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
        template="plotly_dark",
        title="Profit by Campaign"
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
    template="plotly_dark",
    title="Revenue Trend Over Time"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# CUSTOMER SEGMENT PIE CHART
# -------------------------------------------------
col_c, col_d = st.columns([2, 1])

with col_d:

    st.subheader("👥 Segment Revenue Share")

    fig4 = px.pie(
        filtered_df,
        names="Customer_Segment",
        values="Revenue",
        hole=0.4,
        template="plotly_dark"
    )

    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------
# ENGAGEMENT VS REVENUE
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
# DOWNLOAD REPORT
# -------------------------------------------------
st.markdown("---")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Report",
    data=csv,
    file_name="marketing_dashboard_report.csv",
    mime="text/csv"
)
