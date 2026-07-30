import plotly.express as px
import streamlit as st

from utils.data_loader import load_data
from utils.style import (
    CLUSTER_COLORS,
    PLOTLY_CONFIG,
    apply_page_style,
    format_currency,
    format_plotly_chart,
)


st.set_page_config(
    page_title="Iowa Liquor Sales Intelligence",
    page_icon="🥃",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_page_style()


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
try:
    df = load_data()

except Exception as error:
    st.error("The application could not load the dataset.")
    st.exception(error)
    st.stop()


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.title("Dashboard Filters")

selected_city = st.sidebar.selectbox(
    "Select City",
    ["All"] + sorted(
        df["City"]
        .dropna()
        .unique()
        .tolist()
    ),
)

selected_cluster = st.sidebar.selectbox(
    "Select Cluster",
    ["All"] + sorted(
        df["Cluster_Name"]
        .dropna()
        .unique()
        .tolist()
    ),
)


filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["City"] == selected_city
    ]

if selected_cluster != "All":
    filtered_df = filtered_df[
        filtered_df["Cluster_Name"] == selected_cluster
    ]


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("🥃 Iowa Liquor Sales Intelligence Dashboard")

st.caption(
    "Interactive business intelligence dashboard for analysing "
    "Iowa liquor store segments using K-Means clustering."
)

if filtered_df.empty:
    st.warning("No stores match the selected filters.")
    st.stop()


# ---------------------------------------------------------
# KPI calculations
# ---------------------------------------------------------
total_stores = filtered_df["Store Number"].nunique()
total_revenue = filtered_df["Total_Revenue"].sum()
total_bottles = filtered_df["Total_Bottles_Sold"].sum()

average_transaction = (
    filtered_df["Average_Transaction_Value"].mean()
)

average_premium_share = (
    filtered_df["Premium_Product_Share"].mean()
)

number_of_clusters = filtered_df["Cluster"].nunique()


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "Total Stores",
        f"{total_stores:,}",
    )

with kpi2:
    st.metric(
        "Total Revenue",
        format_currency(total_revenue),
    )

with kpi3:
    st.metric(
        "Total Bottles Sold",
        f"{total_bottles:,.0f}",
    )


kpi4, kpi5, kpi6 = st.columns(3)

with kpi4:
    st.metric(
        "Average Transaction Value",
        f"${average_transaction:,.2f}",
    )

with kpi5:
    st.metric(
        "Average Premium Share",
        f"{average_premium_share:.1%}",
    )

with kpi6:
    st.metric(
        "Active Clusters",
        f"{number_of_clusters}",
    )


st.divider()


# ---------------------------------------------------------
# Dashboard aggregations
# ---------------------------------------------------------
cluster_summary = (
    filtered_df
    .groupby(
        "Cluster_Name",
        as_index=False,
    )
    .agg(
        Total_Revenue=("Total_Revenue", "sum"),
        Store_Count=("Store Number", "nunique"),
    )
    .sort_values(
        "Total_Revenue",
        ascending=False,
    )
)


city_summary = (
    filtered_df
    .groupby(
        "City",
        as_index=False,
    )
    .agg(
        Total_Revenue=("Total_Revenue", "sum"),
        Store_Count=("Store Number", "nunique"),
    )
    .sort_values(
        "Total_Revenue",
        ascending=False,
    )
    .head(10)
)


# ---------------------------------------------------------
# Revenue and distribution charts
# ---------------------------------------------------------
left_chart, right_chart = st.columns(2)


with left_chart:
    st.subheader("Revenue by Store Segment")

    revenue_chart = px.bar(
        cluster_summary,
        x="Cluster_Name",
        y="Total_Revenue",
        color="Cluster_Name",
        color_discrete_map=CLUSTER_COLORS,
        labels={
            "Cluster_Name": "Store Segment",
            "Total_Revenue": "Total Revenue ($)",
        },
    )

    revenue_chart.update_layout(
        showlegend=False,
        xaxis_title=None,
    )

    revenue_chart.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: $%{y:,.2f}"
            "<extra></extra>"
        )
    )

    revenue_chart = format_plotly_chart(
        revenue_chart,
        height=450,
    )

    st.plotly_chart(
        revenue_chart,
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )


with right_chart:
    st.subheader("Store Distribution by Segment")

    distribution_chart = px.pie(
        cluster_summary,
        names="Cluster_Name",
        values="Store_Count",
        hole=0.52,
        color="Cluster_Name",
        color_discrete_map=CLUSTER_COLORS,
    )

    distribution_chart.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Stores: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),
    )

    distribution_chart = format_plotly_chart(
        distribution_chart,
        height=450,
    )

    st.plotly_chart(
        distribution_chart,
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )


# ---------------------------------------------------------
# Top cities
# ---------------------------------------------------------
st.subheader("Top 10 Cities by Revenue")

city_chart = px.bar(
    city_summary.sort_values("Total_Revenue"),
    x="Total_Revenue",
    y="City",
    orientation="h",
    labels={
        "Total_Revenue": "Total Revenue ($)",
        "City": "City",
    },
    hover_data=["Store_Count"],
)

city_chart.update_traces(
    marker_color="#2563EB",
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Revenue: $%{x:,.2f}"
        "<extra></extra>"
    ),
)

city_chart = format_plotly_chart(
    city_chart,
    height=500,
)

st.plotly_chart(
    city_chart,
    use_container_width=True,
    config=PLOTLY_CONFIG,
)


# ---------------------------------------------------------
# Data preview
# ---------------------------------------------------------
with st.expander("View filtered store data"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )