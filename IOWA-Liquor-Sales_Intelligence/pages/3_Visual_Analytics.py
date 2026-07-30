import plotly.express as px
import streamlit as st

from utils.data_loader import load_data
from utils.style import (
    CLUSTER_COLORS,
    PLOTLY_CONFIG,
    apply_page_style,
    format_plotly_chart,
)


st.set_page_config(
    page_title="Visual Analytics",
    page_icon="📈",
    layout="wide",
)

apply_page_style()


try:
    df = load_data()

except Exception as error:
    st.error("The application could not load the dataset.")
    st.exception(error)
    st.stop()


st.title("📈 Visual Analytics")

st.caption(
    "Explore store segments, revenue patterns and the two-dimensional "
    "PCA representation of the K-Means clustering results."
)


cluster_options = sorted(
    df["Cluster_Name"]
    .dropna()
    .unique()
    .tolist()
)


selected_clusters = st.multiselect(
    "Select store segments",
    options=cluster_options,
    default=cluster_options,
)


filtered_df = df[
    df["Cluster_Name"].isin(selected_clusters)
].copy()


if filtered_df.empty:
    st.warning("Select at least one store segment.")
    st.stop()


st.subheader("PCA Cluster Visualisation")


pca_chart = px.scatter(
    filtered_df,
    x="PCA1",
    y="PCA2",
    color="Cluster_Name",
    color_discrete_map=CLUSTER_COLORS,
    hover_data={
        "Store Number": True,
        "City": True,
        "Total_Revenue": ":,.2f",
        "Cluster_Name": False,
        "PCA1": ":.2f",
        "PCA2": ":.2f",
    },
    labels={
        "PCA1": "Principal Component 1",
        "PCA2": "Principal Component 2",
        "Cluster_Name": "Store Segment",
    },
)


pca_chart.update_traces(
    marker=dict(
        size=7,
        opacity=0.80,
        line=dict(
            width=0.4,
            color="white",
        ),
    )
)


pca_chart = format_plotly_chart(
    pca_chart,
    height=580,
)


st.plotly_chart(
    pca_chart,
    use_container_width=True,
    config=PLOTLY_CONFIG,
)


st.info(
    "The first two principal components retain approximately 74.78% "
    "of the total variation in the clustering features."
)


left, right = st.columns(2)


with left:
    st.subheader("Revenue Distribution by Segment")

    revenue_distribution = px.box(
        filtered_df,
        x="Cluster_Name",
        y="Total_Revenue",
        color="Cluster_Name",
        color_discrete_map=CLUSTER_COLORS,
        points=False,
        labels={
            "Cluster_Name": "Store Segment",
            "Total_Revenue": "Store Revenue ($)",
        },
    )

    revenue_distribution.update_layout(
        showlegend=False
    )

    revenue_distribution = format_plotly_chart(
        revenue_distribution,
        height=450,
    )

    st.plotly_chart(
        revenue_distribution,
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )


with right:
    st.subheader("Premium Product Share by Segment")

    premium_summary = (
        filtered_df
        .groupby(
            "Cluster_Name",
            as_index=False,
        )
        .agg(
            Average_Premium_Share=(
                "Premium_Product_Share",
                "mean",
            )
        )
        .sort_values(
            "Average_Premium_Share",
            ascending=False,
        )
    )

    premium_chart = px.bar(
        premium_summary,
        x="Cluster_Name",
        y="Average_Premium_Share",
        color="Cluster_Name",
        color_discrete_map=CLUSTER_COLORS,
        labels={
            "Cluster_Name": "Store Segment",
            "Average_Premium_Share": (
                "Average Premium Share"
            ),
        },
    )

    premium_chart.update_layout(
        showlegend=False,
        yaxis_tickformat=".0%",
    )

    premium_chart = format_plotly_chart(
        premium_chart,
        height=450,
    )

    st.plotly_chart(
        premium_chart,
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )


with st.expander("How to interpret the PCA chart"):
    st.markdown(
        """
        - Each point represents one liquor store.
        - Stores positioned close together have similar business profiles.
        - Colours represent the final K-Means store segments.
        - PCA reduces the nine clustering features to two dimensions.
        - The K-Means model was trained using the complete scaled feature set,
          not only PCA1 and PCA2.
        """
    )