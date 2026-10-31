from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(
    page_title="Afficionado Coffee | Sales Analytics",
    page_icon="☕",
    layout="wide"
)

# -------------------- Styling --------------------
st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    div[data-testid="stMetric"] {
        background: #0f0f0f;
        border: 1px solid #e0e8e4;
        padding: 15px;
        border-radius: 12px;
    }
    div[data-testid="stMetriclabel"] {
        cloor: #ffffff !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 700 !important;

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] label *,
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] *,
    div[data-testid="stMetricDelta"] {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("☕ Afficionado Coffee Roasters")
st.subheader("Sales Trend & Time-Based Performance Analysis")
st.caption(
    "Interactive sales analytics | Hourly demand | Store comparisons"
)

# -------------------- Data upload --------------------
DATA_DIR = Path(__file__).parent.parent / "Data"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_DIR / "Afficionado Coffee Roasters.xlsx - Transactions.csv")


df = load_data()

# -------------------- Validate columns --------------------
required = [
    "transaction_qty", "unit_price", "store_location"
]
missing = [col for col in required if col not in df.columns]

if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

df = df.copy()

# Numeric conversion
for col in ["transaction_qty", "unit_price", "year"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Determine hour from existing hour column or transaction_time
if "hour" in df.columns:
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
elif "transaction_time" in df.columns:
    parsed_time = pd.to_datetime(
        df["transaction_time"].astype(str),
        errors="coerce"
    )
    df["hour"] = parsed_time.dt.hour
else:
    st.error("The CSV must contain 'hour' or 'transaction_time'.")
    st.stop()

# Revenue
if "revenue" not in df.columns:
    df["revenue"] = df["transaction_qty"] * df["unit_price"]
else:
    df["revenue"] = pd.to_numeric(
        df["revenue"], errors="coerce"
    )

# Remove invalid analytical rows
df = df.dropna(subset=[
    "transaction_qty", "unit_price", "store_location",
    "hour", "revenue"
])

df = df[
    df["transaction_qty"].gt(0)
    & df["unit_price"].gt(0)
    & df["hour"].between(0, 23)
].copy()

if df.empty:
    st.error("No valid records remain after validation.")
    st.stop()

df["hour"] = df["hour"].astype(int)
df["store_location"] = df["store_location"].astype(str)

# Create labels for chart axes
df["hour_label"] = df["hour"].map(
    lambda h: f"{h:02d}:00"
)

# -------------------- Sidebar filters --------------------
st.sidebar.header("2. Filter the analysis")

stores = sorted(df["store_location"].unique().tolist())
selected_stores = st.sidebar.multiselect(
    "Store location",
    options=stores,
    default=stores
)

if not selected_stores:
    st.warning("Select at least one store location.")
    st.stop()

hour_min = int(df["hour"].min())
hour_max = int(df["hour"].max())

hour_range = st.sidebar.slider(
    "Hour range",
    min_value=hour_min,
    max_value=hour_max,
    value=(hour_min, hour_max),
    format="%d:00"
)

metric_label = st.sidebar.radio(
    "Chart metric",
    ["Revenue", "Quantity sold", "Transaction records"],
    horizontal=False
)

metric_map = {
    "Revenue": "revenue",
    "Quantity sold": "transaction_qty",
    "Transaction records": "transaction_id"
}
metric_col = metric_map[metric_label]

filtered = df[
    df["store_location"].isin(selected_stores)
    & df["hour"].between(hour_range[0], hour_range[1])
].copy()

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# -------------------- Executive overview --------------------
total_revenue = filtered["revenue"].sum()
total_quantity = filtered["transaction_qty"].sum()
record_count = len(filtered)
average_revenue = total_revenue / record_count if record_count else 0

st.header("Executive Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"{total_revenue:,.2f}")
c2.metric("Transaction Records", f"{record_count:,}")
c3.metric("Quantity Sold", f"{total_quantity:,.0f}")
c4.metric("Average Revenue / Record", f"{average_revenue:,.2f}")

st.caption(
    "Revenue is quantity multiplied by unit price. "
    "Transaction records are row counts, not unique customers."
)

# -------------------- Hourly performance --------------------
st.header("Hourly Demand Analysis")

hourly = (
    filtered.groupby("hour", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        quantity_sold=("transaction_qty", "sum"),
        transaction_records=("transaction_qty", "size")
    )
    .sort_values("hour")
)

if metric_label == "Revenue":
    y_col = "revenue"
elif metric_label == "Quantity sold":
    y_col = "quantity_sold"
else:
    y_col = "transaction_records"

fig_hour = px.bar(
    hourly,
    x="hour",
    y=y_col,
    title=f"{metric_label} by Hour",
    labels={
        "hour": "Hour of Day",
        y_col: metric_label
    },
    text_auto=".3s"
)
fig_hour.update_xaxes(
    tickmode="linear", dtick=1, tickformat="02d"
)
fig_hour.update_layout(
    template="plotly_white",
    hovermode="x unified"
)
st.plotly_chart(fig_hour, use_container_width=True)

fig_line = px.line(
    hourly,
    x="hour",
    y=y_col,
    markers=True,
    title=f"Hourly {metric_label} Trend",
    labels={"hour": "Hour of Day", y_col: metric_label}
)
fig_line.update_xaxes(tickmode="linear", dtick=1)
fig_line.update_layout(template="plotly_white")
st.plotly_chart(fig_line, use_container_width=True)

# Report the peak hour within the selected filters
peak_row = hourly.loc[hourly[y_col].idxmax()]
st.success(
    f"Peak hour in the current selection: "
    f"{int(peak_row['hour']):02d}:00 "
    f"({peak_row[y_col]:,.2f} {metric_label.lower()})."
)

# -------------------- Store comparison --------------------
st.header("Store Location Comparison")

store_summary = (
    filtered.groupby("store_location", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        quantity_sold=("transaction_qty", "sum"),
        transaction_records=("transaction_qty", "size")
    )
)

st.dataframe(
    store_summary.sort_values("revenue", ascending=False),
    use_container_width=True,
    hide_index=True
)

fig_store = px.bar(
    store_summary,
    x="store_location",
    y=y_col,
    color="store_location",
    title=f"{metric_label} by Store",
    labels={
        "store_location": "Store Location",
        y_col: metric_label
    }
)
fig_store.update_layout(
    template="plotly_white",
    showlegend=False
)
st.plotly_chart(fig_store, use_container_width=True)

# -------------------- Store-hour heatmap --------------------
st.header("Store-by-Hour Heatmap")

heatmap_source = filtered.copy()

heatmap = heatmap_source.pivot_table(
    index="store_location",
    columns="hour",
    values="transaction_id" if metric_label == "Transaction records"
          and "transaction_id" in heatmap_source.columns
          else ("revenue" if metric_label == "Revenue"
                else "transaction_qty"),
    aggfunc="count" if metric_label == "Transaction records"
            else "sum",
    fill_value=0
)

# Ensure heatmap metric is consistent with selected metric
if metric_label == "Transaction records":
    heatmap = heatmap_source.pivot_table(
        index="store_location",
        columns="hour",
        values="transaction_qty",
        aggfunc="size",
        fill_value=0
    )
elif metric_label == "Revenue":
    heatmap = heatmap_source.pivot_table(
        index="store_location",
        columns="hour",
        values="revenue",
        aggfunc="sum",
        fill_value=0
    )
else:
    heatmap = heatmap_source.pivot_table(
        index="store_location",
        columns="hour",
        values="transaction_qty",
        aggfunc="sum",
        fill_value=0
    )

heatmap = heatmap.reindex(
    columns=list(range(hour_range[0], hour_range[1] + 1)),
    fill_value=0
)

fig_heat = px.imshow(
    heatmap,
    aspect="auto",
    color_continuous_scale="YlOrBr",
    labels={
        "x": "Hour of Day",
        "y": "Store Location",
        "color": metric_label
    },
    title=f"{metric_label} by Store and Hour"
)
fig_heat.update_xaxes(
    tickmode="array",
    tickvals=list(range(len(heatmap.columns))),
    ticktext=[f"{int(h):02d}:00" for h in heatmap.columns]
)
st.plotly_chart(fig_heat, use_container_width=True)

# -------------------- Time buckets --------------------
st.header("Time-of-Day Performance")

def time_bucket(hour):
    if 6 <= hour <= 11:
        return "Morning"
    elif 12 <= hour <= 16:
        return "Afternoon"
    elif 17 <= hour <= 21:
        return "Evening"
    return "Late hours"

filtered["time_bucket"] = filtered["hour"].apply(time_bucket)

bucket_summary = (
    filtered.groupby("time_bucket", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        quantity_sold=("transaction_qty", "sum"),
        transaction_records=("transaction_qty", "size")
    )
)

bucket_order = ["Morning", "Afternoon", "Evening", "Late hours"]
bucket_summary["time_bucket"] = pd.Categorical(
    bucket_summary["time_bucket"],
    categories=bucket_order,
    ordered=True
)
bucket_summary = bucket_summary.sort_values("time_bucket")

st.dataframe(bucket_summary, use_container_width=True, hide_index=True)

fig_bucket = px.bar(
    bucket_summary,
    x="time_bucket",
    y=y_col,
    title=f"{metric_label} by Time Bucket",
    labels={"time_bucket": "Time of Day", y_col: metric_label}
)
fig_bucket.update_layout(template="plotly_white")
st.plotly_chart(fig_bucket, use_container_width=True)

# -------------------- Product category --------------------
if "product_category" in filtered.columns:
    st.header("Product Category Performance")

    product_summary = (
        filtered.groupby("product_category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            quantity_sold=("transaction_qty", "sum"),
            transaction_records=("transaction_qty", "size")
        )
        .sort_values("revenue", ascending=False)
    )

    st.dataframe(
        product_summary,
        use_container_width=True,
        hide_index=True
    )

    fig_product = px.bar(
        product_summary.head(10),
        x="product_category",
        y=y_col,
        title=f"Top Product Categories by {metric_label}",
        labels={
            "product_category": "Product Category",
            y_col: metric_label
        }
    )
    fig_product.update_layout(
        template="plotly_white",
        xaxis_tickangle=-30
    )
    st.plotly_chart(fig_product, use_container_width=True)

# -------------------- Download filtered data --------------------
st.header("Export Results")

csv_bytes = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered transactions (CSV)",
    data=csv_bytes,
    file_name="afficionado_filtered_transactions.csv",
    mime="text/csv"
)

st.caption(
    "Date limitation: the source dataset has no transaction_date. "
    "Daily trends, weekday comparisons and weekend analysis are "
    "not displayed. No dates have been fabricated."
)

st.caption("Afficionado Coffee Roasters | Sales Analytics Project")
