import streamlit as st


CLUSTER_COLORS = {
    "Premium Retail Stores": "#F59E0B",
    "Standard Neighbourhood Stores": "#2563EB",
    "Large High-Volume Stores": "#DC2626",
    "Balanced High-Performing Stores": "#10B981",
    "Specialized Wholesale Stores": "#7C3AED",
}


PLOTLY_CONFIG = {
    "displaylogo": False,
    "displayModeBar": False,
    "responsive": True,
}


def apply_page_style() -> None:
    """Apply a consistent visual theme across all application pages."""

    st.markdown(
        """
        <style>
        /* Main page container */
        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #F6F8FC;
            border-right: 1px solid #E5E7EB;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 8px;
            margin-bottom: 3px;
        }

        /* Typography */
        h1 {
            color: #172033;
            font-weight: 750;
            letter-spacing: -0.5px;
        }

        h2,
        h3 {
            color: #27344D;
            font-weight: 700;
        }

        p,
        label {
            color: #4B5563;
        }

        /* KPI cards */
        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 16px;
            min-height: 110px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
        }

        [data-testid="stMetricLabel"] {
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: #172033;
        }

        /* Inputs */
        [data-baseweb="select"] > div {
            border-radius: 10px;
        }

        /* Alert boxes */
        [data-testid="stAlert"] {
            border-radius: 12px;
        }

        /* Dataframes and expanders */
        [data-testid="stDataFrame"],
        [data-testid="stExpander"] {
            border-radius: 12px;
            overflow: hidden;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
        }

        /* Footer */
        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_currency(value: float) -> str:
    """Format revenue values using K/M notation when appropriate."""

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f} M"

    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f} K"

    return f"${value:,.2f}"


def format_plotly_chart(fig, height: int = 430):
    """Apply consistent professional formatting to Plotly figures."""

    existing_title = fig.layout.title.text

    if not isinstance(existing_title, str):
        existing_title = ""

    if existing_title.strip().lower() == "undefined":
        existing_title = ""

    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(
            l=30,
            r=30,
            t=60 if existing_title else 20,
            b=45,
        ),
        font=dict(
            family="Arial",
            size=13,
            color="#374151",
        ),
        title_text=existing_title,
        legend=dict(
            title=None,
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    if existing_title:
        fig.update_layout(
            title=dict(
                text=existing_title,
                font=dict(
                    size=19,
                    color="#172033",
                ),
                x=0.02,
                xanchor="left",
            )
        )
    else:
        fig.update_layout(
            title_text=""
        )

    fig.update_xaxes(
        gridcolor="#E5E7EB",
        zerolinecolor="#D1D5DB",
        title_font=dict(color="#6B7280"),
        tickfont=dict(color="#6B7280"),
    )

    fig.update_yaxes(
        gridcolor="#E5E7EB",
        zerolinecolor="#D1D5DB",
        title_font=dict(color="#6B7280"),
        tickfont=dict(color="#6B7280"),
    )

    return fig