# Iowa Liquor Sales Intelligence Dashboard

## Project Overview

An end-to-end Machine Learning and Business Intelligence project built
on the Iowa Liquor Sales dataset. The project segments liquor stores
using **K-Means Clustering** and presents interactive business insights
through a **Streamlit dashboard**.

## Objectives

-   Clean and preprocess sales data.
-   Engineer business features.
-   Segment stores using K-Means clustering.
-   Evaluate clusters using Elbow Method, Silhouette Score, PCA and
    business profiling.
-   Build an interactive Streamlit dashboard.

## Tech Stack

-   Python
-   Pandas
-   NumPy
-   Scikit-learn
-   Plotly
-   Streamlit
-   Joblib

## Project Structure

``` text
Dashboard.py
pages/
utils/
models/
data/
notebooks/
requirements.txt
README.md
```

## ML Workflow

1.  Data Cleaning
2.  Feature Engineering
3.  Scaling & Log Transformation
4.  K-Means Clustering
5.  Cluster Evaluation
6.  Cluster Profiling
7.  Business Insights
8.  Streamlit Dashboard

## Dashboard Features

-   Executive KPIs
-   Store Explorer
-   Cluster Explorer
-   Visual Analytics
-   Business Insights
-   Interactive Filters

## Installation

``` bash
pip install -r requirements.txt
streamlit run Dashboard.py
```

## Results

-   Five meaningful liquor store segments.
-   Interactive business dashboard.
-   Actionable recommendations for each cluster.

## Future Scope

-   Streamlit Community Cloud deployment
-   Live prediction page
-   Enhanced documentation
