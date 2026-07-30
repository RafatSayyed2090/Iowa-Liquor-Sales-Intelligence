from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "store_segmentation_results.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and validate the final store-level segmentation dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = {
        "Store Number",
        "City",
        "Transaction_Count",
        "Total_Revenue",
        "Total_Bottles_Sold",
        "Average_Transaction_Value",
        "Average_Bottles_Per_Transaction",
        "Average_Bottle_Retail",
        "Premium_Product_Share",
        "Unique_Products",
        "Unique_Categories",
        "Cluster",
        "Cluster_Name",
        "PCA1",
        "PCA2",
    }

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    df["City"] = df["City"].fillna("UNKNOWN")
    df["Cluster_Name"] = df["Cluster_Name"].fillna("Unclassified")

    return df