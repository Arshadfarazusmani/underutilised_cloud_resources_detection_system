import streamlit as st
import pandas as pd
import joblib

# ----------------------------------------
# Load model & scaler
# ----------------------------------------
model = joblib.load("idle_resource_rf_model_02 (1).joblib")
scaler = joblib.load("scaler_02 (1).joblib")

st.set_page_config(page_title="Idle Resource Detector", layout="wide")
st.title("🔍 Idle Resource Detection System")
st.write("Provide cloud resource metrics below to detect if the resource is **Idle or Active**.")

# ----------------------------------------
# Input Form
# ----------------------------------------
resource_id = st.text_input("Resource ID", "res-001")

resource_type = st.selectbox(
    "Resource Type",
    ["VM", "Storage", "Database", "Container"]
)

cpu_utilization = st.slider("CPU Utilization (%)", 0.0, 100.0, 10.0)
memory_utilization = st.slider("Memory Utilization (%)", 0.0, 100.0, 10.0)
disk_io = st.slider("Disk I/O (MB/s)", 0.0, 100.0, 5.0)
network_io = st.slider("Network I/O (MB/s)", 0.0, 100.0, 5.0)
last_access_days_ago = st.slider("Last Access Days Ago", 0, 60, 5)
provisioned_cpu_cores = st.slider("Provisioned CPU Cores", 1, 32, 4)
provisioned_capacity_gb = st.slider("Provisioned Storage (GB)", 10, 2000, 100)

# ----------------------------------------
# Predict Button
# ----------------------------------------
if st.button("Predict Resource Status"):

    # Create DataFrame for prediction
    df = pd.DataFrame([{
        "cpu_utilization": cpu_utilization,
        "memory_utilization": memory_utilization,
        "network_io": network_io,
        "disk_io": disk_io,
        "last_access_days_ago": last_access_days_ago,
        "provisioned_capacity_gb": provisioned_capacity_gb,
        "provisioned_cpu_cores": provisioned_cpu_cores,
        f"resource_type_{resource_type}": 1
    }])

    # Add missing one-hot columns
    for rt in ["VM", "Storage", "Database", "Container"]:
        col = f"resource_type_{rt}"
        if col not in df.columns:
            df[col] = 1 if rt == resource_type else 0

    # Ensure correct feature order
    expected_features = list(scaler.feature_names_in_)
    df = df.reindex(columns=expected_features, fill_value=0)

    # Scale
    X_scaled = scaler.transform(df)

    # Predict
    pred = model.predict(X_scaled)[0]
    status = "🟢 Idle" if pred == 1 else "🔴 Active"

    # Display Result
    st.success(f"### Resource Status: {status}")

    st.write("### Input Summary")
    st.dataframe(df)
