import pandas as pd
import streamlit as st

from utils.data_loader import load_data
from utils.style import (
    apply_page_style,
    format_currency,
)


st.set_page_config(
    page_title="Store Explorer",
    page_icon="🔍",
    layout="wide",
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
# Cluster descriptions
# ---------------------------------------------------------
cluster_details = {
    "Premium Retail Stores": {
        "description": (
            "Stores with stronger premium-product preference and relatively "
            "higher average bottle prices, but lower product-category breadth."
        ),
        "recommendation": (
            "Expand premium assortments, promote exclusive brands and use "
            "targeted campaigns for customers willing to pay higher prices."
        ),
    },

    "Standard Neighbourhood Stores": {
        "description": (
            "The largest segment, consisting mainly of regular local stores "
            "with comparatively lower premium-product share and moderate sales."
        ),
        "recommendation": (
            "Focus on popular value products, local promotions, efficient "
            "replenishment and customer-retention offers."
        ),
    },

    "Large High-Volume Stores": {
        "description": (
            "Large stores with high transactions, revenue, bottle sales, "
            "product diversity and category coverage."
        ),
        "recommendation": (
            "Prioritise inventory availability, bulk procurement, demand "
            "planning and supplier negotiations."
        ),
    },

    "Balanced High-Performing Stores": {
        "description": (
            "Stores performing above average across several measures without "
            "being excessively concentrated in one business characteristic."
        ),
        "recommendation": (
            "Use loyalty programmes, cross-selling and selective premium "
            "expansion to strengthen sustainable growth."
        ),
    },

    "Specialized Wholesale Stores": {
        "description": (
            "A very small specialised segment with exceptionally high average "
            "transaction size and bottles sold per transaction."
        ),
        "recommendation": (
            "Manage these stores separately using wholesale pricing, bulk-order "
            "planning, key-account support and customised supply arrangements."
        ),
    },
}


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("🔍 Store Explorer")

st.caption(
    "Search for an individual store and review its performance, "
    "assigned segment and recommended business action."
)


# ---------------------------------------------------------
# Store selection
# ---------------------------------------------------------
search_col1, search_col2 = st.columns(2)


with search_col1:
    selected_city = st.selectbox(
        "Filter by city",
        ["All"] + sorted(
            df["City"]
            .dropna()
            .unique()
            .tolist()
        ),
    )


city_filtered_df = df.copy()

if selected_city != "All":
    city_filtered_df = city_filtered_df[
        city_filtered_df["City"] == selected_city
    ]


with search_col2:
    store_options = sorted(
        city_filtered_df["Store Number"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    selected_store = st.selectbox(
        "Select store number",
        store_options,
    )


# ---------------------------------------------------------
# Selected store
# ---------------------------------------------------------
store_record = city_filtered_df[
    city_filtered_df["Store Number"].astype(int)
    == selected_store
]


if store_record.empty:
    st.warning("No record was found for the selected store.")
    st.stop()


store = store_record.iloc[0]


# ---------------------------------------------------------
# Store identity
# ---------------------------------------------------------
st.subheader(
    f"Store {int(store['Store Number'])} — {store['City']}"
)

st.info(
    f"Assigned Segment: **{store['Cluster_Name']}**"
)


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------
row1_col1, row1_col2, row1_col3 = st.columns(3)


with row1_col1:
    st.metric(
        "Total Revenue",
        format_currency(store["Total_Revenue"]),
    )


with row1_col2:
    st.metric(
        "Total Bottles Sold",
        f"{store['Total_Bottles_Sold']:,.0f}",
    )


with row1_col3:
    st.metric(
        "Transactions",
        f"{store['Transaction_Count']:,.0f}",
    )


row2_col1, row2_col2, row2_col3 = st.columns(3)


with row2_col1:
    st.metric(
        "Average Transaction Value",
        f"${store['Average_Transaction_Value']:,.2f}",
    )


with row2_col2:
    st.metric(
        "Average Bottles per Transaction",
        f"{store['Average_Bottles_Per_Transaction']:,.2f}",
    )


with row2_col3:
    st.metric(
        "Average Bottle Retail",
        f"${store['Average_Bottle_Retail']:,.2f}",
    )


row3_col1, row3_col2, row3_col3 = st.columns(3)


with row3_col1:
    st.metric(
        "Premium Product Share",
        f"{store['Premium_Product_Share']:.1%}",
    )


with row3_col2:
    st.metric(
        "Unique Products",
        f"{store['Unique_Products']:,.0f}",
    )


with row3_col3:
    st.metric(
        "Unique Categories",
        f"{store['Unique_Categories']:,.0f}",
    )


st.divider()


# ---------------------------------------------------------
# Interpretation
# ---------------------------------------------------------
segment_name = store["Cluster_Name"]

segment_information = cluster_details.get(
    segment_name,
    {
        "description": "No description is currently available.",
        "recommendation": "No recommendation is currently available.",
    },
)


description_col, recommendation_col = st.columns(2)


with description_col:
    st.subheader("Segment Interpretation")
    st.write(segment_information["description"])


with recommendation_col:
    st.subheader("Recommended Business Action")
    st.success(segment_information["recommendation"])


# ---------------------------------------------------------
# Comparison against overall average
# ---------------------------------------------------------
st.subheader(
    "Store Performance Compared with Overall Average"
)


comparison_metrics = [
    ("Total_Revenue", "Total Revenue"),
    ("Total_Bottles_Sold", "Total Bottles Sold"),
    (
        "Average_Transaction_Value",
        "Average Transaction Value",
    ),
    (
        "Premium_Product_Share",
        "Premium Product Share",
    ),
    ("Unique_Products", "Unique Products"),
    ("Unique_Categories", "Unique Categories"),
]


comparison_data = []


for column, label in comparison_metrics:
    store_value = store[column]
    overall_average = df[column].mean()

    if overall_average != 0:
        difference_percentage = (
            (store_value - overall_average)
            / overall_average
        ) * 100

    else:
        difference_percentage = 0

    comparison_data.append(
        {
            "Metric": label,
            "Store Value": store_value,
            "Overall Average": overall_average,
            "Difference (%)": difference_percentage,
        }
    )


comparison_df = pd.DataFrame(comparison_data)


st.dataframe(
    comparison_df.style.format(
        {
            "Store Value": "{:,.2f}",
            "Overall Average": "{:,.2f}",
            "Difference (%)": "{:+.1f}%",
        }
    ),
    use_container_width=True,
    hide_index=True,
)


with st.expander("View complete selected-store record"):
    st.dataframe(
        store_record,
        use_container_width=True,
        hide_index=True,
    )