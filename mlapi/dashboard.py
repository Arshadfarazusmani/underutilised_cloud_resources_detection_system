import streamlit as st
import pandas as pd
import joblib
import altair as alt
import numpy as np

# ----------------------------------------
# Load model & scaler
# ----------------------------------------
model = joblib.load("idle_resource_rf_model_02 (1).joblib")
scaler = joblib.load("scaler_02 (1).joblib")
expected_features = list(scaler.feature_names_in_)

# One-hot resource types
RESOURCE_TYPES = ["VM", "Storage", "Database", "Container"]

# ----------------------------------------
# Function: prepare row for prediction
# ----------------------------------------
def prepare_features(row):
    df = pd.DataFrame([row])

    # One-hot encoding
    for rt in RESOURCE_TYPES:
        df[f"resource_type_{rt}"] = 1 if row["resource_type"] == rt else 0

    df = df.drop(columns=["resource_type", "resource_id"], errors="ignore")

    # Add missing columns
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0

    # Reorder
    df = df[expected_features]

    # Scale
    scaled = scaler.transform(df)
    return scaled


# ----------------------------------------
# Streamlit UI
# ----------------------------------------
st.set_page_config(page_title="Idle Resource Dashboard", layout="wide")

st.title("📊 Idle Resource Detection Dashboard")
st.write("Analyze cloud resources and detect Idle vs Active using ML model.")

tabs = st.tabs(["🔍 Single Prediction", "📁 Batch Upload", "📊 Analytics Dashboard"])

# ==========================================================
# TAB 1 — SINGLE RESOURCE PREDICTION
# ==========================================================
with tabs[0]:

    st.subheader("🔍 Predict for a Single Resource")

    col1, col2 = st.columns(2)

    with col1:
        resource_id = st.text_input("Resource ID", "res-001")
        resource_type = st.selectbox("Resource Type", RESOURCE_TYPES)
        cpu_util = st.slider("CPU Utilization (%)", 0, 100, 10)
        mem_util = st.slider("Memory Utilization (%)", 0, 100, 10)
        disk_io = st.slider("Disk I/O (MB/s)", 0, 100, 5)

    with col2:
        net_io = st.slider("Network I/O (MB/s)", 0, 100, 5)
        last_access = st.slider("Last Access Days Ago", 0, 60, 5)
        cpu_cores = st.slider("Provisioned CPU Cores", 1, 32, 4)
        cap_gb = st.slider("Provisioned Capacity (GB)", 10, 2000, 100)

    if st.button("Predict Status"):

        row = {
            "resource_id": resource_id,
            "resource_type": resource_type,
            "cpu_utilization": cpu_util,
            "memory_utilization": mem_util,
            "disk_io": disk_io,
            "network_io": net_io,
            "last_access_days_ago": last_access,
            "provisioned_cpu_cores": cpu_cores,
            "provisioned_capacity_gb": cap_gb,
        }

        X = prepare_features(row)
        pred = model.predict(X)[0]

        status = "🟢 IDLE" if pred == 1 else "🔴 ACTIVE"
        st.success(f"### Resource Status: {status}")


# ==========================================================
# TAB 2 — BATCH CSV UPLOAD
# ==========================================================
with tabs[1]:

    st.subheader("📁 Batch Resource Prediction (Upload CSV)")

    uploaded = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### Preview")
        st.dataframe(df.head())

        predictions = []
        for _, r in df.iterrows():
            row = r.to_dict()
            X = prepare_features(row)
            pred = model.predict(X)[0]
            predictions.append(pred)

        df["prediction"] = predictions
        df["status"] = df["prediction"].apply(lambda x: "Idle" if x == 1 else "Active")

        st.success("Predictions completed!")

        st.write("### Results")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results CSV", csv, "predictions.csv")


# ==========================================================
# TAB 3 — ANALYTICS DASHBOARD
# ==========================================================
with tabs[2]:

    st.subheader("📊 Visual Analytics")

    st.write("Upload CSV to generate analytics")

    uploaded2 = st.file_uploader("Upload Resource Metrics CSV", type=["csv"], key="analytics")

    if uploaded2:
        df2 = pd.read_csv(uploaded2)

        # Generate predictions
        preds = []
        for _, r in df2.iterrows():
            X = prepare_features(r.to_dict())
            preds.append(model.predict(X)[0])

        df2["prediction"] = preds
        df2["status"] = df2["prediction"].apply(lambda x: "Idle" if x == 1 else "Active")

        # ------------------------------------------------------------------------------------
        # Summary Cards
        # ------------------------------------------------------------------------------------
        idle_count = (df2["status"] == "Idle").sum()
        active_count = (df2["status"] == "Active").sum()

        c1, c2 = st.columns(2)
        with c1:
            st.metric("🟢 Idle Resources", idle_count)
        with c2:
            st.metric("🔴 Active Resources", active_count)

        # ------------------------------------------------------------------------------------
        # Pie Chart
        # ------------------------------------------------------------------------------------
        # pie_df = df2["status"].value_counts().reset_index()
        # pie_chart = alt.Chart(pie_df).mark_arc().encode(
        #     theta=alt.Theta("status:Q", stack=True),
        #     color=alt.Color("index:N"),
        #     tooltip=["index", "status"]
        # )
        # st.altair_chart(pie_chart, use_container_width=True)

        # -------------------------
# # FIXED PIE CHART
# # -------------------------
# pie_df = df2["status"].value_counts().reset_index()
# pie_df.columns = ["status", "count"]

# pie_chart = (
#     alt.Chart(pie_df)
#     .mark_arc()
#     .encode(
#         theta=alt.Theta(field="count", type="quantitative"),
#         color=alt.Color(field="status", type="nominal"),
#         tooltip=["status", "count"]
#     )
# )

# st.altair_chart(pie_chart, use_container_width=True)


#         # ------------------------------------------------------------------------------------
#         # Bar Chart: CPU vs Memory
#         # ------------------------------------------------------------------------------------
#         st.write("### CPU vs Memory Utilization")
#         bar = alt.Chart(df2).mark_circle(size=80).encode(
#             x="cpu_utilization",
#             y="memory_utilization",
#             color="status",
#             tooltip=list(df2.columns)
#         )
#         st.altair_chart(bar, use_container_width=True)

        # ------------------------------------------------------------------------------------
        # Interactive Table
        # ------------------------------------------------------------------------------------
        st.write("### Detailed Resource Table")
        st.dataframe(df2, use_container_width=True)
