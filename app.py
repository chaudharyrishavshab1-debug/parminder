import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Parminder Singh Bhari | Cloud Analytics Dashboard", page_icon="📊", layout="wide")

DATA_DIR = Path(__file__).parent / "data"
FILES = {
    "DataServe India (Client)": DATA_DIR / "client_dataset.xlsx",
    "Competitor Alpha": DATA_DIR / "competitor_alpha.xlsx",
    "Competitor Beta": DATA_DIR / "competitor_beta.xlsx",
}

REQUIRED = [
    "Record_ID", "Month", "Region", "Business_Unit", "Customer_Segment",
    "Cloud_Service_Model", "Data_Volume_GB", "Query_Count",
    "Avg_Query_Time_Sec", "Cloud_Cost_INR", "Uptime_Pct",
    "Dashboard_Users", "Dashboard_Views", "Data_Quality_Score",
    "Mining_Segment", "Conversion_Rate_Pct", "Customer_Satisfaction_Score",
    "Optimization_Score", "Storage_Utilization_Pct",
    "Decision_Effectiveness_Score"
]

@st.cache_data
def load_data():
    frames = {}
    for company, path in FILES.items():
        df = pd.read_excel(path)
        missing = [c for c in REQUIRED if c not in df.columns]
        if missing:
            raise ValueError(f"{path.name} is missing columns: {', '.join(missing)}")
        frames[company] = df
    return frames

def metrics_table(frames):
    rows = []
    for company, df in frames.items():
        total_volume = df["Data_Volume_GB"].sum()
        total_cost = df["Cloud_Cost_INR"].sum()
        rows.append({
            "Company": company,
            "Records": len(df),
            "Avg. query time (sec)": df["Avg_Query_Time_Sec"].mean(),
            "Uptime (%)": df["Uptime_Pct"].mean(),
            "Cost per GB (₹)": total_cost / total_volume if total_volume else 0,
            "Data quality": df["Data_Quality_Score"].mean(),
            "Conversion (%)": df["Conversion_Rate_Pct"].mean(),
            "Optimization": df["Optimization_Score"].mean(),
            "Decision effectiveness": df["Decision_Effectiveness_Score"].mean(),
            "Customer satisfaction": df["Customer_Satisfaction_Score"].mean(),
        })
    return pd.DataFrame(rows)

try:
    frames = load_data()
except Exception as exc:
    st.error(f"Unable to load the supplied datasets: {exc}")
    st.stop()

benchmark = metrics_table(frames)
client = frames["DataServe India (Client)"]

st.title("Cloud-Based Business Data Analytics & Decision Support System")
st.caption("BCA Semester 5 Minor Project | Student: Parminder Singh Bhari | Enrolment: 024BCA110806")
st.markdown(
    "An interactive dashboard to examine cloud performance, compare the client with two competitors, "
    "identify operational gaps and support evidence-based improvement decisions."
)

with st.sidebar:
    st.header("Dashboard controls")
    section = st.radio(
        "Choose a section",
        ["Executive Overview", "Company Benchmarking", "Regional Analysis",
         "Cloud Service Models", "Data Quality & Segments", "Recommendations", "Dataset Explorer"]
    )
    st.divider()
    st.caption("All results are calculated from the three supplied Excel datasets.")

if section == "Executive Overview":
    st.subheader("Executive overview")
    client_row = benchmark[benchmark["Company"] == "DataServe India (Client)"].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Client records", f"{int(client_row['Records']):,}")
    c2.metric("Average query time", f"{client_row['Avg. query time (sec)']:.2f} sec")
    c3.metric("Average uptime", f"{client_row['Uptime (%)']:.2f}%")
    c4.metric("Cloud cost per GB", f"₹{client_row['Cost per GB (₹)']:.2f}")

    left, right = st.columns(2)
    with left:
        fig = px.bar(benchmark, x="Company", y="Avg. query time (sec)",
                     title="Average query time by company", text_auto=".2f")
        fig.update_layout(yaxis_title="Seconds", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.bar(benchmark, x="Company", y="Cost per GB (₹)",
                     title="Cloud cost per GB by company", text_auto=".2f")
        fig.update_layout(yaxis_title="₹ per GB", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### KPI snapshot")
    st.dataframe(benchmark.round(2), use_container_width=True, hide_index=True)
    st.info(
        "Initial reading: compare query speed, cost per GB, uptime and data quality together. "
        "A single KPI should not be used in isolation to judge overall cloud performance."
    )

elif section == "Company Benchmarking":
    st.subheader("Company benchmarking")
    selected = st.multiselect(
        "KPIs to compare",
        ["Avg. query time (sec)", "Uptime (%)", "Cost per GB (₹)", "Data quality",
         "Conversion (%)", "Optimization", "Decision effectiveness", "Customer satisfaction"],
        default=["Avg. query time (sec)", "Uptime (%)", "Cost per GB (₹)",
                 "Data quality", "Decision effectiveness"]
    )
    if selected:
        long_df = benchmark.melt(id_vars="Company", value_vars=selected,
                                 var_name="KPI", value_name="Value")
        fig = px.bar(long_df, x="KPI", y="Value", color="Company", barmode="group",
                     title="Selected KPI comparison")
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(benchmark.round(3), use_container_width=True, hide_index=True)
    st.caption("Cost per GB = total Cloud_Cost_INR ÷ total Data_Volume_GB for each company.")

elif section == "Regional Analysis":
    st.subheader("Client performance by region")
    regional = client.groupby("Region", as_index=False).agg(
        Records=("Record_ID", "count"),
        Query_Time=("Avg_Query_Time_Sec", "mean"),
        Uptime=("Uptime_Pct", "mean"),
        Data_Quality=("Data_Quality_Score", "mean"),
        Decision_Effectiveness=("Decision_Effectiveness_Score", "mean"),
        Total_Cost=("Cloud_Cost_INR", "sum"),
        Total_Volume=("Data_Volume_GB", "sum"),
    )
    regional["Cost_per_GB"] = regional["Total_Cost"] / regional["Total_Volume"]
    a, b = st.columns(2)
    with a:
        fig = px.bar(regional, x="Region", y="Decision_Effectiveness",
                     title="Decision effectiveness by region", text_auto=".2f")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.bar(regional, x="Region", y="Query_Time",
                     title="Average query time by region", text_auto=".2f")
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(regional.round(2), use_container_width=True, hide_index=True)

elif section == "Cloud Service Models":
    st.subheader("Cloud service model analysis")
    service = client.groupby("Cloud_Service_Model", as_index=False).agg(
        Records=("Record_ID", "count"),
        Avg_Cost=("Cloud_Cost_INR", "mean"),
        Avg_Uptime=("Uptime_Pct", "mean"),
        Avg_Query_Time=("Avg_Query_Time_Sec", "mean"),
        Avg_Storage_Utilization=("Storage_Utilization_Pct", "mean"),
        Avg_Optimization=("Optimization_Score", "mean"),
    )
    a, b = st.columns(2)
    with a:
        fig = px.bar(service, x="Cloud_Service_Model", y="Avg_Cost",
                     title="Average cloud cost by service model", text_auto=".2f")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.bar(service, x="Cloud_Service_Model", y="Avg_Uptime",
                     title="Average uptime by service model", text_auto=".2f")
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(service.round(2), use_container_width=True, hide_index=True)
    st.caption("Average record-level cloud cost is shown here; use cost per GB for volume-normalised company comparisons.")

elif section == "Data Quality & Segments":
    st.subheader("Data quality and customer segments")
    quality_checks = []
    for name, df in frames.items():
        quality_checks.append({
            "Company": name,
            "Rows": len(df),
            "Missing cells": int(df.isna().sum().sum()),
            "Duplicate rows": int(df.duplicated().sum()),
            "Duplicate Record_ID": int(df["Record_ID"].duplicated().sum()),
        })
    st.markdown("#### Dataset quality checks")
    st.dataframe(pd.DataFrame(quality_checks), use_container_width=True, hide_index=True)

    segment_field = st.selectbox("Segment field", ["Customer_Segment", "Mining_Segment", "Business_Unit"])
    segment = client.groupby(segment_field, as_index=False).agg(
        Records=("Record_ID", "count"),
        Conversion=("Conversion_Rate_Pct", "mean"),
        Data_Quality=("Data_Quality_Score", "mean"),
        Decision_Effectiveness=("Decision_Effectiveness_Score", "mean"),
    )
    fig = px.bar(segment, x=segment_field, y="Decision_Effectiveness",
                 color="Conversion", title=f"Decision effectiveness by {segment_field}")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(segment.round(2), use_container_width=True, hide_index=True)

elif section == "Recommendations":
    st.subheader("Evidence-based recommendations")
    c = benchmark.set_index("Company")
    client_m = c.loc["DataServe India (Client)"]
    alpha_m = c.loc["Competitor Alpha"]
    beta_m = c.loc["Competitor Beta"]

    recommendations = [
        ("1. Improve query performance",
         f"Client query time is {client_m['Avg. query time (sec)']:.2f} seconds. "
         f"Alpha records {alpha_m['Avg. query time (sec)']:.2f} seconds. "
         "Profile slow queries, review indexes and caching, and test workload scheduling."),
        ("2. Improve cloud cost efficiency",
         f"Client cost per GB is ₹{client_m['Cost per GB (₹)']:.2f}, compared with "
         f"₹{beta_m['Cost per GB (₹)']:.2f} for Beta. Review resource rightsizing, storage lifecycle "
         "policies and cost alerts while keeping workload differences in view."),
        ("3. Strengthen data quality",
         f"Client data-quality score is {client_m['Data quality']:.2f}, below "
         f"Alpha ({alpha_m['Data quality']:.2f}) and Beta ({beta_m['Data quality']:.2f}). "
         "Introduce field validation, duplicate checks, ownership and periodic quality reporting."),
        ("4. Monitor reliability and outcomes",
         "Track uptime, decision effectiveness and customer satisfaction together during every pilot. "
         "Avoid making platform changes based on cost or speed alone.")
    ]
    for title, body in recommendations:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(body)
    st.warning("These are proposed actions based on observed dataset differences; the data does not prove the causes of those differences.")

elif section == "Dataset Explorer":
    st.subheader("Dataset explorer")
    company = st.selectbox("Dataset", list(frames.keys()))
    df = frames[company]
    columns = st.multiselect("Columns to display", list(df.columns),
                             default=["Record_ID", "Month", "Region", "Avg_Query_Time_Sec",
                                      "Cloud_Cost_INR", "Uptime_Pct", "Data_Quality_Score"])
    search = st.text_input("Optional text filter (searches selected rows)")
    view = df[columns].copy() if columns else df.copy()
    if search and columns:
        mask = view.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
        view = view[mask]
    st.write(f"Showing {len(view):,} of {len(df):,} records")
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.download_button("Download displayed data as CSV",
                       data=view.to_csv(index=False).encode("utf-8"),
                       file_name=f"{company.lower().replace(' ', '_')}_filtered.csv",
                       mime="text/csv")

st.divider()
st.caption("Academic project demonstration | Data source: supplied client and competitor Excel datasets")
