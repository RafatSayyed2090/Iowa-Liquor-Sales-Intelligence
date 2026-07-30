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
    page_title="Cluster Explorer",
    page_icon="📊",
    layout="wide",
)

apply_page_style()


try:
    df = load_data()

except Exception as error:
    st.error("The application could not load the dataset.")
    st.exception(error)
    st.stop()


cluster_details = {
    "Premium Retail Stores": {
        "description": (
            "Premium-oriented stores with higher average bottle prices "
            "and a stronger share of premium products."
        ),
        "recommendation": (
            "Expand premium assortments, promote exclusive brands and "
            "use targeted campaigns for customers willing to pay more."
        ),
    },

    "Standard Neighbourhood Stores": {
        "description": (
            "The largest segment, consisting mainly of regular local stores "
            "with moderate sales and comparatively lower premium-product share."
        ),
        "recommendation": (
            "Focus on value products, local promotions, reliable replenishment "
            "and customer-retention offers."
        ),
    },

    "Large High-Volume Stores": {
        "description": (
            "Large stores with high transactions, revenue, bottle sales, "
            "product diversity and category coverage."
        ),
        "recommendation": (
            "Prioritise inventory availability, bulk procurement, demand "
            "planning and stronger supplier negotiations."
        ),
    },

    "Balanced High-Performing Stores": {
        "description": (
            "Stores performing above average across several measures without "
            "being excessively dependent on one business characteristic."
        ),
        "recommendation": (
            "Use loyalty programmes, cross-selling and selective premium "
            "expansion to support sustainable growth."
        ),
    },

    "Specialized Wholesale Stores": {
        "description": (
            "A very small specialised segment with exceptionally large "
            "transactions and bulk purchasing behaviour."
        ),
        "recommendation": (
            "Use wholesale pricing, customised supply arrangements, "
            "bulk-order planning and key-account management."
        ),
    },
}


st.title("📊 Cluster Explorer")

st.caption(
    "Explore the characteristics, performance and recommended strategy "
    "for each K-Means store segment."
)


selected_cluster = st.selectbox(
    "Select store segment",
    sorted(
        df["Cluster_Name"]
        .dropna()
        .unique()
        .tolist()
    ),
)


cluster_df = df[
    df["Cluster_Name"] == selected_cluster
].copy()


if cluster_df.empty:
    st.warning("No stores were found for the selected segment.")
    st.stop()


segment_information = cluster_details[selected_cluster]


st.info(
    f"**Segment Profile:** "
    f"{segment_information['description']}"
)


store_count = cluster_df["Store Number"].nunique()
total_revenue = cluster_df["Total_Revenue"].sum()
total_bottles = cluster_df["Total_Bottles_Sold"].sum()

average_transaction = (
    cluster_df["Average_Transaction_Value"].mean()
)

average_premium_share = (
    cluster_df["Premium_Product_Share"].mean()
)

average_unique_products = (
    cluster_df["Unique_Products"].mean()
)


kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:
    st.metric(
        "Stores in Segment",
        f"{store_count:,}",
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
        "Average Unique Products",
        f"{average_unique_products:,.1f}",
    )


st.divider()

st.subheader("Recommended Business Action")

st.success(
    segment_information["recommendation"]
)


city_summary = (
    cluster_df
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


left_chart, right_chart = st.columns(2)


with left_chart:
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
        marker_color=CLUSTER_COLORS.get(
            selected_cluster,
            "#2563EB",
        ),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Revenue: $%{x:,.2f}"
            "<extra></extra>"
        ),
    )

    city_chart = format_plotly_chart(
        city_chart,
        height=450,
    )

    st.subheader("Top Cities in Selected Segment")

    st.plotly_chart(
        city_chart,
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )


with right_chart:
    products_chart = px.histogram(
        cluster_df,
        x="Unique_Products",
        nbins=20,
        labels={
            "Unique_Products": "Unique Products",
            "count": "Number of Stores",
        },
    )

    products_chart.update_traces(
        marker_color=CLUSTER_COLORS.get(
            selected_cluster,
            "#2563EB",
        )
    )

    products_chart = format_plotly_chart(
        products_chart,
        height=450,
    )

    st.subheader("Unique Products Distribution")

    st.plotly_chart(
        products_chart,
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )


comparison_summary = (
    cluster_df[
        [
            "Average_Transaction_Value",
            "Average_Bottle_Retail",
            "Premium_Product_Share",
            "Unique_Products",
            "Unique_Categories",
        ]
    ]
    .mean()
    .reset_index()
)


comparison_summary.columns = [
    "Metric",
    "Segment Average",
]


comparison_summary["Metric"] = (
    comparison_summary["Metric"]
    .str.replace("_", " ", regex=False)
)


premium_mask = (
    comparison_summary["Metric"]
    == "Premium Product Share"
)


comparison_summary.loc[
    premium_mask,
    "Segment Average",
] = (
    comparison_summary.loc[
        premium_mask,
        "Segment Average",
    ]
    * 100
)


comparison_summary.loc[
    premium_mask,
    "Metric",
] = "Premium Product Share (%)"


comparison_summary["Segment Average"] = (
    comparison_summary["Segment Average"]
    .round(2)
)


st.subheader("Average Business Profile")

st.dataframe(
    comparison_summary,
    use_container_width=True,
    hide_index=True,
)


with st.expander("View stores in this segment"):
    display_columns = [
        "Store Number",
        "City",
        "Total_Revenue",
        "Total_Bottles_Sold",
        "Transaction_Count",
        "Average_Transaction_Value",
        "Premium_Product_Share",
        "Unique_Products",
        "Unique_Categories",
    ]

    st.dataframe(
        cluster_df[display_columns]
        .sort_values(
            "Total_Revenue",
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )