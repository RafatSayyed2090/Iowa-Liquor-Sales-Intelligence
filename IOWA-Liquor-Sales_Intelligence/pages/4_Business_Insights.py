import streamlit as st

from utils.data_loader import load_data
from utils.style import apply_page_style


st.set_page_config(
    page_title="Business Insights",
    page_icon="💡",
    layout="wide",
)

apply_page_style()


try:
    df = load_data()

except Exception as error:
    st.error("The application could not load the dataset.")
    st.exception(error)
    st.stop()


st.title("💡 Business Insights and Recommendations")

st.caption(
    "Business interpretation of the five store segments identified "
    "through K-Means clustering."
)


st.info(
    """
    This project segments Iowa liquor stores into five meaningful business
    groups using K-Means clustering. The resulting segmentation supports
    store-level performance analysis, inventory planning, premium-product
    strategy and targeted marketing decisions through an interactive
    Streamlit dashboard.
    """
)


cluster_insights = {
    "Premium Retail Stores": {
        "profile": (
            "Premium-oriented stores with higher bottle prices and a "
            "stronger share of premium products."
        ),
        "actions": [
            "Expand premium and limited-edition product ranges.",
            "Use targeted promotions rather than broad discounting.",
            "Develop exclusive supplier and brand partnerships.",
        ],
    },

    "Standard Neighbourhood Stores": {
        "profile": (
            "The largest store segment, serving regular local demand "
            "with comparatively modest premium-product adoption."
        ),
        "actions": [
            "Maintain reliable availability of popular value products.",
            "Use local promotions and repeat-purchase offers.",
            "Improve replenishment for frequently purchased items.",
        ],
    },

    "Large High-Volume Stores": {
        "profile": (
            "Large stores with high transactions, revenue, bottle sales "
            "and extensive product and category coverage."
        ),
        "actions": [
            "Prioritise demand forecasting and inventory availability.",
            "Negotiate bulk purchasing and supplier terms.",
            "Use the segment for major product launches and promotions.",
        ],
    },

    "Balanced High-Performing Stores": {
        "profile": (
            "Stores performing above average across several measures "
            "without being overly dependent on one characteristic."
        ),
        "actions": [
            "Use loyalty and cross-selling programmes.",
            "Expand selected premium categories gradually.",
            "Replicate successful practices across average stores.",
        ],
    },

    "Specialized Wholesale Stores": {
        "profile": (
            "A rare specialised segment with unusually large orders, "
            "high transaction values and bulk purchasing behaviour."
        ),
        "actions": [
            "Apply wholesale pricing and key-account management.",
            "Plan dedicated bulk-order inventory.",
            "Review these stores separately because the segment has "
            "only a small number of members.",
        ],
    },
}


cluster_sizes = (
    df["Cluster_Name"]
    .value_counts()
)


largest_segment = cluster_sizes.index[0]
largest_segment_size = int(cluster_sizes.iloc[0])


highest_revenue_segment = (
    df.groupby("Cluster_Name")["Total_Revenue"]
    .sum()
    .idxmax()
)


highest_premium_segment = (
    df.groupby("Cluster_Name")["Premium_Product_Share"]
    .mean()
    .idxmax()
)


k1, k2, k3 = st.columns(3)


with k1:
    st.markdown("##### Largest Segment")
    st.markdown(
        f"### {largest_segment}"
    )
    st.caption(
        f"{largest_segment_size:,} stores"
    )


with k2:
    st.markdown("##### Highest Revenue Segment")
    st.markdown(
        f"### {highest_revenue_segment}"
    )


with k3:
    st.markdown("##### Highest Premium Share")
    st.markdown(
        f"### {highest_premium_segment}"
    )


st.divider()


for cluster_name, information in cluster_insights.items():

    with st.expander(
        cluster_name,
        expanded=False,
    ):
        cluster_count = int(
            (
                df["Cluster_Name"]
                == cluster_name
            ).sum()
        )

        cluster_revenue = (
            df.loc[
                df["Cluster_Name"] == cluster_name,
                "Total_Revenue",
            ]
            .sum()
        )

        st.write(
            information["profile"]
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Stores",
            f"{cluster_count:,}",
        )

        c2.metric(
            "Sample Revenue",
            f"${cluster_revenue:,.2f}",
        )

        st.markdown(
            "**Recommended actions**"
        )

        for action in information["actions"]:
            st.markdown(
                f"- {action}"
            )


st.warning(
    """
    Note: This dashboard is built using a 100,000-row sample of the Iowa
    Liquor Sales dataset covering 2012–2026. Results represent the analysed
    project sample and should not be interpreted as complete statewide totals.
    """
)