# import streamlit as st
# import pandas as pd
# import joblib
# import altair as alt
# import numpy as np

# import streamlit as st
# from login_page import login_page
# from auth import save_prediction, save_resource, get_history

# # Ensure session state
# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False
#     st.session_state["user"] = None

# if not st.session_state["logged_in"]:
#     login_page()
#     st.stop()


# # ----------------------------------------
# # Load model & scaler
# # ----------------------------------------
# model = joblib.load("idle_resource_rf_model_02 (1).joblib")
# scaler = joblib.load("scaler_02 (1).joblib")
# expected_features = list(scaler.feature_names_in_)

# # One-hot resource types
# RESOURCE_TYPES = ["VM", "Storage", "Database", "Container"]

# # ----------------------------------------
# # Function: prepare row for prediction
# # ----------------------------------------
# def prepare_features(row):
#     df = pd.DataFrame([row])

#     # One-hot encoding
#     for rt in RESOURCE_TYPES:
#         df[f"resource_type_{rt}"] = 1 if row["resource_type"] == rt else 0

#     df = df.drop(columns=["resource_type", "resource_id"], errors="ignore")

#     # Add missing columns
#     for col in expected_features:
#         if col not in df.columns:
#             df[col] = 0

#     # Reorder
#     df = df[expected_features]

#     # Scale
#     scaled = scaler.transform(df)
#     return scaled


# # ----------------------------------------
# # Streamlit UI
# # ----------------------------------------
# st.set_page_config(page_title="Idle Resource Dashboard", layout="wide")

# st.title("📊 Idle Resource Detection Dashboard")
# st.write("Analyze cloud resources and detect Idle vs Active using ML model.")

# tabs = st.tabs(["🔍 Single Prediction", "📁 Batch Upload", "📊 Analytics Dashboard"])

# # ==========================================================
# # TAB 1 — SINGLE RESOURCE PREDICTION
# # ==========================================================
# with tabs[0]:

#     st.subheader("🔍 Predict for a Single Resource")

#     col1, col2 = st.columns(2)

#     with col1:
#         resource_id = st.text_input("Resource ID", "res-001")
#         resource_type = st.selectbox("Resource Type", RESOURCE_TYPES)
#         cpu_util = st.slider("CPU Utilization (%)", 0, 100, 10)
#         mem_util = st.slider("Memory Utilization (%)", 0, 100, 10)
#         disk_io = st.slider("Disk I/O (MB/s)", 0, 100, 5)

#     with col2:
#         net_io = st.slider("Network I/O (MB/s)", 0, 100, 5)
#         last_access = st.slider("Last Access Days Ago", 0, 60, 5)
#         cpu_cores = st.slider("Provisioned CPU Cores", 1, 32, 4)
#         cap_gb = st.slider("Provisioned Capacity (GB)", 10, 2000, 100)

#     if st.button("Predict Status"):

#         row = {
#             "resource_id": resource_id,
#             "resource_type": resource_type,
#             "cpu_utilization": cpu_util,
#             "memory_utilization": mem_util,
#             "disk_io": disk_io,
#             "network_io": net_io,
#             "last_access_days_ago": last_access,
#             "provisioned_cpu_cores": cpu_cores,
#             "provisioned_capacity_gb": cap_gb,
#         }

#         X = prepare_features(row)
#         pred = model.predict(X)[0]

#         status = "🟢 IDLE" if pred == 1 else "🔴 ACTIVE"
#         st.success(f"### Resource Status: {status}")


# # ==========================================================
# # TAB 2 — BATCH CSV UPLOAD
# # ==========================================================
# with tabs[1]:

#     st.subheader("📁 Batch Resource Prediction (Upload CSV)")

#     uploaded = st.file_uploader("Upload CSV file", type=["csv"])

#     if uploaded:
#         df = pd.read_csv(uploaded)
#         st.write("### Preview")
#         st.dataframe(df.head())

#         predictions = []
#         for _, r in df.iterrows():
#             row = r.to_dict()
#             X = prepare_features(row)
#             pred = model.predict(X)[0]
#             predictions.append(pred)

#         df["prediction"] = predictions
#         df["status"] = df["prediction"].apply(lambda x: "Idle" if x == 1 else "Active")

#         st.success("Predictions completed!")

#         st.write("### Results")
#         st.dataframe(df)

#         csv = df.to_csv(index=False).encode("utf-8")
#         st.download_button("Download Results CSV", csv, "predictions.csv")


# # ==========================================================
# # TAB 3 — ANALYTICS DASHBOARD
# # ==========================================================
# with tabs[2]:

#     st.subheader("📊 Visual Analytics")

#     st.write("Upload CSV to generate analytics")

#     uploaded2 = st.file_uploader("Upload Resource Metrics CSV", type=["csv"], key="analytics")

#     if uploaded2:
#         df2 = pd.read_csv(uploaded2)

#         # Generate predictions
#         preds = []
#         for _, r in df2.iterrows():
#             X = prepare_features(r.to_dict())
#             preds.append(model.predict(X)[0])

#         df2["prediction"] = preds
#         df2["status"] = df2["prediction"].apply(lambda x: "Idle" if x == 1 else "Active")

#         # ------------------------------------------------------------------------------------
#         # Summary Cards
#         # ------------------------------------------------------------------------------------
#         idle_count = (df2["status"] == "Idle").sum()
#         active_count = (df2["status"] == "Active").sum()

#         c1, c2 = st.columns(2)
#         with c1:
#             st.metric("🟢 Idle Resources", idle_count)
#         with c2:
#             st.metric("🔴 Active Resources", active_count)

#         # ------------------------------------------------------------------------------------
#         # Pie Chart
#         # ------------------------------------------------------------------------------------
#         # pie_df = df2["status"].value_counts().reset_index()
#         # pie_chart = alt.Chart(pie_df).mark_arc().encode(
#         #     theta=alt.Theta("status:Q", stack=True),
#         #     color=alt.Color("index:N"),
#         #     tooltip=["index", "status"]
#         # )
#         # st.altair_chart(pie_chart, use_container_width=True)

#         # -------------------------
# # # FIXED PIE CHART
# # # -------------------------
# # pie_df = df2["status"].value_counts().reset_index()
# # pie_df.columns = ["status", "count"]

# # pie_chart = (
# #     alt.Chart(pie_df)
# #     .mark_arc()
# #     .encode(
# #         theta=alt.Theta(field="count", type="quantitative"),
# #         color=alt.Color(field="status", type="nominal"),
# #         tooltip=["status", "count"]
# #     )
# # )

# # st.altair_chart(pie_chart, use_container_width=True)


# #         # ------------------------------------------------------------------------------------
# #         # Bar Chart: CPU vs Memory
# #         # ------------------------------------------------------------------------------------
# #         st.write("### CPU vs Memory Utilization")
# #         bar = alt.Chart(df2).mark_circle(size=80).encode(
# #             x="cpu_utilization",
# #             y="memory_utilization",
# #             color="status",
# #             tooltip=list(df2.columns)
# #         )
# #         st.altair_chart(bar, use_container_width=True)

#         # ------------------------------------------------------------------------------------
#         # Interactive Table
#         # ------------------------------------------------------------------------------------
#         st.write("### Detailed Resource Table")
#         st.dataframe(df2, use_container_width=True)



# # dashboard.py
# import streamlit as st
# import pandas as pd
# import altair as alt
# from login_page import login_page
# from db import insert_resource, insert_prediction, find_predictions_by_user_email
# from model_utils import predict_row, prepare_features
# import os

# # show logo (optional)
# logo_path = "/mnt/data/2668e390-a503-4152-9cd8-9de675a78139.png"
# if os.path.exists(logo_path):
#     st.image(logo_path, width=150)

# st.set_page_config(page_title="Idle Resource Dashboard", layout="wide")
# st.title("📊 Idle Resource Detection Dashboard")
# st.write("Analyze cloud resources and detect Idle vs Active using ML model.")

# # ---- session state for auth ----
# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False
#     st.session_state["user"] = None

# # show login page if not logged in
# if not st.session_state["logged_in"]:
#     login_page()
#     st.stop()

# # logged in UI
# st.sidebar.write(f"Logged in as: {st.session_state['user'].get('email')}")
# if st.sidebar.button("Logout"):
#     st.session_state["logged_in"] = False
#     st.session_state["user"] = None
#     st.experimental_rerun()

# tabs = st.tabs(["🔍 Single Prediction", "📁 Batch Upload", "📊 Analytics Dashboard", "🕘 History"])

# # ==========================================================
# # TAB 1 — SINGLE RESOURCE PREDICTION
# # ==========================================================
# with tabs[0]:
#     st.subheader("🔍 Predict for a Single Resource (and save)")

#     col1, col2 = st.columns(2)

#     with col1:
#         resource_id = st.text_input("Resource ID", "res-001")
#         resource_type = st.selectbox("Resource Type", ["VM", "Storage", "Database", "Container"])
#         cpu_util = st.slider("CPU Utilization (%)", 0, 100, 10)
#         mem_util = st.slider("Memory Utilization (%)", 0, 100, 10)
#         disk_io = st.slider("Disk I/O (MB/s)", 0, 100, 5)

#     with col2:
#         net_io = st.slider("Network I/O (MB/s)", 0, 100, 5)
#         last_access = st.slider("Last Access Days Ago", 0, 365, 5)
#         cpu_cores = st.slider("Provisioned CPU Cores", 1, 64, 4)
#         cap_gb = st.slider("Provisioned Capacity (GB)", 1, 2000, 100)

#     if st.button("Predict Status"):
#         row = {
#             "resource_id": resource_id,
#             "resource_type": resource_type,
#             "cpu_utilization": float(cpu_util),
#             "memory_utilization": float(mem_util),
#             "disk_io": float(disk_io),
#             "network_io": float(net_io),
#             "last_access_days_ago": float(last_access),
#             "provisioned_cpu_cores": float(cpu_cores),
#             "provisioned_capacity_gb": float(cap_gb),
#         }

#         pred_val, status = predict_row(row)
#         st.success(f"### Resource Status: {'🟢 IDLE' if status=='Idle' else '🔴 ACTIVE'}")

#         # Save resource snapshot and prediction to MongoDB
#         user_email = st.session_state["user"].get("email")
#         try:
#             rid = insert_resource({**row, "user_email": user_email})
#             pid = insert_prediction({
#                 "user_email": user_email,
#                 "resource_id": resource_id,
#                 "resource_snapshot": row,
#                 "prediction": int(pred_val),
#                 "status": status
#             })
#             st.info(f"Saved prediction id: {pid}")
#         except Exception as e:
#             st.error(f"Error saving to DB: {e}")

# # ==========================================================
# # TAB 2 — BATCH CSV UPLOAD
# # ==========================================================
# with tabs[1]:
#     st.subheader("📁 Batch Resource Prediction (Upload CSV)")

#     uploaded = st.file_uploader("Upload CSV file", type=["csv"])
#     if uploaded:
#         df = pd.read_csv(uploaded)
#         st.write("### Preview")
#         st.dataframe(df.head())

#         predictions = []
#         statuses = []
#         ids = []
#         user_email = st.session_state["user"].get("email")

#         for _, r in df.iterrows():
#             row = r.to_dict()
#             # ensure numeric types
#             for k in ["cpu_utilization","memory_utilization","disk_io","network_io","last_access_days_ago","provisioned_cpu_cores","provisioned_capacity_gb"]:
#                 if k in row:
#                     try:
#                         row[k] = float(row[k])
#                     except:
#                         row[k] = 0.0

#             pred_val, status = predict_row(row)
#             predictions.append(pred_val)
#             statuses.append(status)

#             # save
#             try:
#                 rid = insert_resource({**row, "user_email": user_email})
#                 pid = insert_prediction({
#                     "user_email": user_email,
#                     "resource_id": row.get("resource_id",""),
#                     "resource_snapshot": row,
#                     "prediction": int(pred_val),
#                     "status": status
#                 })
#                 ids.append(pid)
#             except Exception as e:
#                 ids.append(None)

#         df["prediction"] = predictions
#         df["status"] = statuses
#         df["prediction_id"] = ids

#         st.success("Predictions completed!")
#         st.dataframe(df)
#         csv = df.to_csv(index=False).encode("utf-8")
#         st.download_button("Download Results CSV", csv, "predictions.csv")

# # ==========================================================
# # TAB 3 — ANALYTICS DASHBOARD
# # ==========================================================
# with tabs[2]:
#     st.subheader("📊 Visual Analytics")
#     st.write("Upload CSV to generate analytics")
#     uploaded2 = st.file_uploader("Upload Resource Metrics CSV (for analytics)", type=["csv"], key="analytics")
#     if uploaded2:
#         df2 = pd.read_csv(uploaded2)
#         # generate predictions
#         preds = []
#         statuses = []
#         for _, r in df2.iterrows():
#             row = r.to_dict()
#             pred_val, status = predict_row(row)
#             preds.append(pred_val)
#             statuses.append(status)
#         df2["prediction"] = preds
#         df2["status"] = statuses

#         idle_count = (df2["status"] == "Idle").sum()
#         active_count = (df2["status"] == "Active").sum()

#         c1, c2 = st.columns(2)
#         with c1:
#             st.metric("🔴 Idle Resources", idle_count)
#         with c2:
#             st.metric(" 🟢 Active Resources", active_count)

#         pie_df = df2["status"].value_counts().reset_index()
#         pie_df.columns = ["status", "count"]
#         pie_chart = (
#             alt.Chart(pie_df)
#             .mark_arc()
#             .encode(
#                 theta=alt.Theta(field="count", type="quantitative"),
#                 color=alt.Color(field="status", type="nominal"),
#                 tooltip=["status", "count"]
#             )
#         )
#         st.altair_chart(pie_chart, use_container_width=True)

#         st.write("### CPU vs Memory Utilization")
#         scatter = alt.Chart(df2).mark_circle(size=80).encode(
#             x="cpu_utilization",
#             y="memory_utilization",
#             color="status",
#             tooltip=list(df2.columns)
#         )
#         st.altair_chart(scatter, use_container_width=True)

#         st.write("### Detailed Resource Table")
#         st.dataframe(df2, use_container_width=True)

# # ==========================================================
# # TAB 4 — HISTORY
# # ==========================================================
# with tabs[3]:
#     st.subheader("🕘 Your Prediction History")
#     user_email = st.session_state["user"].get("email")
#     try:
#         hist = find_predictions_by_user_email(user_email, limit=500)
#         if hist:
#             df_hist = pd.DataFrame(hist)
#             st.dataframe(df_hist)
#         else:
#             st.write("No history yet.")
#     except Exception as e:
#         st.error(f"Error fetching history: {e}")

# dashboard.py

# from style import inject_tailwind_style

# import streamlit as st
# import pandas as pd
# import altair as alt
# from login_page import login_page
# from db import insert_resource, insert_prediction, find_predictions_by_user_email
# from model_utils import predict_row, prepare_features
# import os

# # show logo (optional)
# logo_path = "/mnt/data/2668e390-a503-4152-9cd8-9de675a78139.png"
# if os.path.exists(logo_path):
#     st.image(logo_path, width=150)

# st.set_page_config(page_title="Idle Resource Dashboard", layout="wide")
# inject_tailwind_style()

# st.title("📊 Idle Resource Detection Dashboard")
# st.write("Analyze cloud resources and detect Idle vs Active using ML model.")

# # ---- session state for auth ----
# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False
#     st.session_state["user"] = None

# # show login page if not logged in
# if not st.session_state["logged_in"]:
#     login_page()
#     st.stop()

# # logged in UI
# st.sidebar.write(f"Logged in as: {st.session_state['user'].get('email')}")
# if st.sidebar.button("Logout"):
#     st.session_state["logged_in"] = False
#     st.session_state["user"] = None
#     st.experimental_rerun()

# tabs = st.tabs(["🔍 Single Prediction", "📁 Batch Upload", "📊 Analytics Dashboard", "🕘 History"])

# # ==========================================================
# # TAB 1 — SINGLE RESOURCE PREDICTION
# # ==========================================================
# with tabs[0]:
#     st.subheader("🔍 Predict for a Single Resource (and save)")

#     col1, col2 = st.columns(2)

#     with col1:
#         resource_id = st.text_input("Resource ID", "res-001")
#         resource_type = st.selectbox("Resource Type", ["VM", "Storage", "Database", "Container"])
#         cpu_util = st.slider("CPU Utilization (%)", 0, 100, 10)
#         mem_util = st.slider("Memory Utilization (%)", 0, 100, 10)
#         disk_io = st.slider("Disk I/O (MB/s)", 0, 100, 5)

#     with col2:
#         net_io = st.slider("Network I/O (MB/s)", 0, 100, 5)
#         last_access = st.slider("Last Access Days Ago", 0, 365, 5)
#         cpu_cores = st.slider("Provisioned CPU Cores", 1, 64, 4)
#         cap_gb = st.slider("Provisioned Capacity (GB)", 1, 2000, 100)

#     if st.button("Predict Status"):
#         row = {
#             "resource_id": resource_id,
#             "resource_type": resource_type,
#             "cpu_utilization": float(cpu_util),
#             "memory_utilization": float(mem_util),
#             "disk_io": float(disk_io),
#             "network_io": float(net_io),
#             "last_access_days_ago": float(last_access),
#             "provisioned_cpu_cores": float(cpu_cores),
#             "provisioned_capacity_gb": float(cap_gb),
#         }

#         pred_val, status = predict_row(row)
#         st.success(f"### Resource Status: {'🟢 IDLE' if status=='Idle' else '🔴 ACTIVE'}")

#         # Save resource snapshot and prediction to MongoDB
#         user_email = st.session_state["user"].get("email")
#         try:
#             rid = insert_resource({**row, "user_email": user_email})
#             pid = insert_prediction({
#                 "user_email": user_email,
#                 "resource_id": resource_id,
#                 "resource_snapshot": row,
#                 "prediction": int(pred_val),
#                 "status": status
#             })
#             st.info(f"Saved prediction id: {pid}")
#         except Exception as e:
#             st.error(f"Error saving to DB: {e}")

# # ==========================================================
# # TAB 2 — BATCH CSV UPLOAD
# # ==========================================================
# with tabs[1]:
#     st.subheader("📁 Batch Resource Prediction (Upload CSV)")

#     uploaded = st.file_uploader("Upload CSV file", type=["csv"])
#     if uploaded:
#         df = pd.read_csv(uploaded)
#         st.write("### Preview")
#         st.dataframe(df.head())

#         predictions = []
#         statuses = []
#         ids = []
#         user_email = st.session_state["user"].get("email")

#         for _, r in df.iterrows():
#             row = r.to_dict()
#             # ensure numeric types
#             for k in ["cpu_utilization","memory_utilization","disk_io","network_io","last_access_days_ago","provisioned_cpu_cores","provisioned_capacity_gb"]:
#                 if k in row:
#                     try:
#                         row[k] = float(row[k])
#                     except:
#                         row[k] = 0.0

#             pred_val, status = predict_row(row)
#             predictions.append(pred_val)
#             statuses.append(status)

#             # save
#             try:
#                 rid = insert_resource({**row, "user_email": user_email})
#                 pid = insert_prediction({
#                     "user_email": user_email,
#                     "resource_id": row.get("resource_id",""),
#                     "resource_snapshot": row,
#                     "prediction": int(pred_val),
#                     "status": status
#                 })
#                 ids.append(pid)
#             except Exception as e:
#                 ids.append(None)

#         df["prediction"] = predictions
#         df["status"] = statuses
#         df["prediction_id"] = ids

#         st.success("Predictions completed!")
#         st.dataframe(df)
#         csv = df.to_csv(index=False).encode("utf-8")
#         st.download_button("Download Results CSV", csv, "predictions.csv")

# # ==========================================================
# # TAB 3 — ANALYTICS DASHBOARD
# # ==========================================================
# with tabs[2]:
#     st.subheader("📊 Visual Analytics")
#     st.write("Upload CSV to generate analytics")
#     uploaded2 = st.file_uploader("Upload Resource Metrics CSV (for analytics)", type=["csv"], key="analytics")
#     if uploaded2:
#         df2 = pd.read_csv(uploaded2)
#         # generate predictions
#         preds = []
#         statuses = []
#         for _, r in df2.iterrows():
#             row = r.to_dict()
#             pred_val, status = predict_row(row)
#             preds.append(pred_val)
#             statuses.append(status)
#         df2["prediction"] = preds
#         df2["status"] = statuses

#         idle_count = (df2["status"] == "Idle").sum()
#         active_count = (df2["status"] == "Active").sum()

#         c1, c2 = st.columns(2)
#         with c1:
#             st.metric("🟢 Idle Resources", idle_count)
#         with c2:
#             st.metric("🔴 Active Resources", active_count)

#         pie_df = df2["status"].value_counts().reset_index()
#         pie_df.columns = ["status", "count"]
#         pie_chart = (
#             alt.Chart(pie_df)
#             .mark_arc()
#             .encode(
#                 theta=alt.Theta(field="count", type="quantitative"),
#                 color=alt.Color(field="status", type="nominal"),
#                 tooltip=["status", "count"]
#             )
#         )
#         st.altair_chart(pie_chart, use_container_width=True)

#         st.write("### CPU vs Memory Utilization")
#         scatter = alt.Chart(df2).mark_circle(size=80).encode(
#             x="cpu_utilization",
#             y="memory_utilization",
#             color="status",
#             tooltip=list(df2.columns)
#         )
#         st.altair_chart(scatter, use_container_width=True)

#         st.write("### Detailed Resource Table")
#         st.dataframe(df2, use_container_width=True)

# # ==========================================================
# # TAB 4 — HISTORY
# # ==========================================================
# with tabs[3]:
#     st.subheader("🕘 Your Prediction History")
#     user_email = st.session_state["user"].get("email")
#     try:
#         hist = find_predictions_by_user_email(user_email, limit=500)
#         if hist:
#             df_hist = pd.DataFrame(hist)
#             st.dataframe(df_hist)
#         else:
#             st.write("No history yet.")
#     except Exception as e:
#         st.error(f"Error fetching history: {e}")


# dashboard.py
"""
Final styled Streamlit dashboard with:
- Tailwind-like styling via style.inject_tailwind_style()
- Professional SVG icons (icons.py)
- Auth guard (login_page.py)
- MongoDB saves (db.py: insert_resource, insert_prediction, find_predictions_by_user_email)
- Model utils (model_utils.predict_row)
- Tabs: Single Prediction, Batch Upload, Analytics, History
- Uses uploaded logo at: /mnt/data/2668e390-a503-4152-9cd8-9de675a78139.png
Paste this file as `dashboard.py` in the same folder as:
  - style.py
  - icons.py
  - login_page.py
  - db.py
  - model_utils.py
  - idle_resource_rf_model_02.joblib
  - scaler_02.joblib
"""

from style import inject_tailwind_style
from icons import (
    CPU_ICON,
    MEMORY_ICON,
    DISK_ICON,
    NETWORK_ICON,
    USER_ICON,
    IDLE_ICON,
    ACTIVE_ICON,
)
import streamlit as st
import pandas as pd
import altair as alt
import os

# auth + db + model helpers (assumes these exist and were created earlier)
from login_page import login_page
from db import insert_resource, insert_prediction, find_predictions_by_user_email
from model_utils import predict_row

# -----------------------------
# Page config and custom style
# -----------------------------
st.set_page_config(page_title="Idle Resource Dashboard", layout="wide")
inject_tailwind_style()

# -----------------------------
# Optional logo (uploaded file)
# -----------------------------
LOGO_PATH = "/mnt/data/2668e390-a503-4152-9cd8-9de675a78139.png"  # provided file path
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=140)

# Header
st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:12px;">
      <div style="font-size:22px; font-weight:700;">{USER_ICON}</div>
      <div>
        <h1 style="margin:0">📊 Idle Resource Detection Dashboard</h1>
        <div style="color:#475569">Analyze cloud resources and detect Idle vs Active using ML</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(" ")  # small spacing

# -----------------------------
# Session / Auth guard
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user"] = None

if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# Sidebar: user info + logout
with st.sidebar:
    st.markdown(f"<div style='display:flex;align-items:center;gap:10px'>{USER_ICON} <b>{st.session_state['user'].get('username','User')}</b></div>", unsafe_allow_html=True)
    st.write(st.session_state["user"].get("email"))
    st.markdown("---")
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.experimental_rerun()
    st.markdown("---")
    st.write("Quick actions")
    st.button("Open Predict Tab")  # placeholder for future actions

# Tabs
tabs = st.tabs(
    ["🔍 Predict (Single)", "📁 Batch Upload", "📊 Analytics", "🕘 History"]
)

# -----------------------------
# TAB 1 — SINGLE PREDICTION
# -----------------------------
with tabs[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='display:flex;align-items:center;gap:10px'>{CPU_ICON} Predict a single resource</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"{USER_ICON} **Resource ID**", unsafe_allow_html=True)
        resource_id = st.text_input("resource_id_input", "res-001", key="resource_id_input")
        st.markdown(f"{USER_ICON} **Resource Type**", unsafe_allow_html=True)
        resource_type = st.selectbox("", ["VM", "Storage", "Database", "Container"], key="resource_type_select")

        st.markdown(f"{CPU_ICON} **CPU Utilization (%)**", unsafe_allow_html=True)
        cpu_util = st.slider("", 0, 100, 10, key="cpu_util_slider")
        st.markdown(f"{MEMORY_ICON} **Memory Utilization (%)**", unsafe_allow_html=True)
        mem_util = st.slider("", 0, 100, 10, key="mem_util_slider")

    with col2:
        st.markdown(f"{DISK_ICON} **Disk I/O (MB/s)**", unsafe_allow_html=True)
        disk_io = st.slider("", 0, 100, 5, key="disk_io_slider")
        st.markdown(f"{NETWORK_ICON} **Network I/O (MB/s)**", unsafe_allow_html=True)
        net_io = st.slider("", 0, 100, 5, key="net_io_slider")

        st.markdown("**Additional Info**")
        last_access = st.number_input("Last Access Days Ago", min_value=0, max_value=3650, value=5, key="last_access")
        cpu_cores = st.number_input("Provisioned CPU Cores", min_value=1, max_value=128, value=4, key="cpu_cores")
        cap_gb = st.number_input("Provisioned Capacity (GB)", min_value=1, max_value=10000, value=100, key="cap_gb")

    st.write("")  # small gap
    if st.button("Predict Status", key="single_predict_btn"):
        # build row
        row = {
            "resource_id": resource_id,
            "resource_type": resource_type,
            "cpu_utilization": float(cpu_util),
            "memory_utilization": float(mem_util),
            "disk_io": float(disk_io),
            "network_io": float(net_io),
            "last_access_days_ago": float(last_access),
            "provisioned_cpu_cores": float(cpu_cores),
            "provisioned_capacity_gb": float(cap_gb),
        }

        pred_val, status = predict_row(row)

        # show result with icon
        if status == "Idle":
            st.markdown(f"{IDLE_ICON} <span style='font-weight:700; font-size:18px; color:red'>Resource Status: IDLE</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"{ACTIVE_ICON} <span style='font-weight:700; font-size:18px; color:green'>Resource Status: ACTIVE</span>", unsafe_allow_html=True)

        # persist to DB
        try:
            user_email = st.session_state["user"].get("email")
            insert_resource({**row, "user_email": user_email})
            pid = insert_prediction({
                "user_email": user_email,
                "resource_id": resource_id,
                "resource_snapshot": row,
                "prediction": int(pred_val),
                "status": status
            })
            st.info(f"Saved prediction id: {pid}")
        except Exception as e:
            st.error(f"Failed to save prediction: {e}")

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# TAB 2 — BATCH UPLOAD
# -----------------------------
with tabs[1]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='display:flex;align-items:center;gap:10px'>{DISK_ICON} Batch CSV Prediction</h3>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload CSV (columns should include resource_id, resource_type, cpu_utilization, memory_utilization, disk_io, network_io, last_access_days_ago, provisioned_cpu_cores, provisioned_capacity_gb)", type=["csv"], key="batch_uploader")
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        st.write("### Preview")
        st.dataframe(df.head(), use_container_width=True)

        if st.button("Run Batch Predictions", key="run_batch"):
            user_email = st.session_state["user"].get("email")
            preds, statuses, pids = [], [], []
            for _, r in df.iterrows():
                row = r.to_dict()
                # safe numeric conversion
                for k in ["cpu_utilization","memory_utilization","disk_io","network_io","last_access_days_ago","provisioned_cpu_cores","provisioned_capacity_gb"]:
                    if k in row:
                        try:
                            row[k] = float(row[k])
                        except:
                            row[k] = 0.0
                pred_val, status = predict_row(row)
                preds.append(pred_val)
                statuses.append(status)

                try:
                    insert_resource({**row, "user_email": user_email})
                    pid = insert_prediction({
                        "user_email": user_email,
                        "resource_id": row.get("resource_id", ""),
                        "resource_snapshot": row,
                        "prediction": int(pred_val),
                        "status": status
                    })
                    pids.append(pid)
                except Exception:
                    pids.append(None)

            df["prediction"] = preds
            df["status"] = statuses
            df["prediction_id"] = pids

            st.success("Batch predictions finished")
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Results CSV", data=csv, file_name="predictions.csv", mime="text/csv")

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# TAB 3 — ANALYTICS
# -----------------------------
# with tabs[2]:
#     st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#     st.markdown(f"<h3 style='display:flex;align-items:center;gap:10px'>{NETWORK_ICON} Analytics & Charts</h3>", unsafe_allow_html=True)

#     uploaded2 = st.file_uploader("Upload CSV to analyze (same format as batch)", type=["csv"], key="analytics_uploader")
#     if uploaded2 is not None:
#         df2 = pd.read_csv(uploaded2)

#         # get preds
#         preds, statuses = [], []
#         for _, r in df2.iterrows():
#             row = r.to_dict()
#             try:
#                 pred_val, status = predict_row(row)
#             except Exception:
#                 pred_val, status = 0, "Active"
#             preds.append(pred_val)
#             statuses.append(status)

#         df2["prediction"] = preds
#         df2["status"] = statuses

#         idle_c = (df2["status"] == "Idle").sum()
#         active_c = (df2["status"] == "Active").sum()

#         c1, c2 = st.columns(2)
#         with c1:
#             st.metric(label=f"{IDLE_ICON} Idle Resources", value=int(idle_c))
#         with c2:
#             st.metric(label=f"{ACTIVE_ICON} Active Resources", value=int(active_c))

#         # pie chart
#         pie_df = df2["status"].value_counts().reset_index()
#         pie_df.columns = ["status", "count"]
#         pie_chart = alt.Chart(pie_df).mark_arc().encode(
#             theta=alt.Theta(field="count", type="quantitative"),
#             color=alt.Color(field="status", type="nominal"),
#             tooltip=["status", "count"]
#         )
#         st.altair_chart(pie_chart, use_container_width=True)

#         # CPU vs Memory scatter
#         st.write("### CPU vs Memory")
#         scatter = alt.Chart(df2).mark_circle(size=80).encode(
#             x="cpu_utilization",
#             y="memory_utilization",
#             color="status",
#             tooltip=list(df2.columns)
#         )
#         st.altair_chart(scatter, use_container_width=True)

#         st.write("### Full Table")
#         st.dataframe(df2, use_container_width=True)

#     st.markdown('</div>', unsafe_allow_html=True)
# 

with tabs[2]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='display:flex;align-items:center;gap:10px'>{NETWORK_ICON} Analytics & Charts</h3>",
        unsafe_allow_html=True
    )

    st.info("Upload a CSV file with cloud resource utilization data to generate predictions, charts, and insights.")

    uploaded2 = st.file_uploader(
        "Upload CSV to analyze (same format as batch)", 
        type=["csv"], 
        key="analytics_uploader"
    )

    if uploaded2 is not None:

        with st.spinner("Processing uploaded CSV..."):
            try:
                df2 = pd.read_csv(uploaded2)

                required_cols = [
                    "cpu_utilization", "memory_utilization", "disk_io", "network_io",
                    "last_access_days_ago", "provisioned_cpu_cores", "provisioned_capacity_gb"
                ]

                missing = [c for c in required_cols if c not in df2.columns]

                if missing:
                    st.error(f"❌ Missing required columns in CSV: {', '.join(missing)}")
                    st.stop()

            except Exception as e:
                st.error(f"❌ Error reading CSV: {e}")
                st.stop()

            # -----------------------------------------
            # Run Model Predictions
            # -----------------------------------------
            preds, statuses = [], []

            for _, r in df2.iterrows():
                row = r.to_dict()
                try:
                    pred_val, status = predict_row(row)
                except Exception:
                    pred_val, status = 0, "Active"

                preds.append(pred_val)
                statuses.append(status)

            df2["prediction"] = preds
            df2["status"] = statuses

            # -----------------------------------------
            # KPI Summary Metrics + Custom White Boxes
            # -----------------------------------------
            idle_c = (df2["status"] == "Idle").sum()
            active_c = (df2["status"] == "Active").sum()

            st.markdown("""
            <style>
            .count-card {
                background: white;
                padding: 22px;
                border-radius: 14px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
                text-align: center;
                font-size: 32px;
                font-weight: 700;
                color: black;
            }
            .label-text {
                font-size: 15px;
                color: #444;
                margin-top: 8px;
            }
            </style>
            """, unsafe_allow_html=True)

            cA, cB = st.columns(2)
            with cA:
                st.markdown(f"""
                <div class="count-card">
                    {idle_c}
                    <div class="label-text">{IDLE_ICON} Idle Resources</div>
                </div>
                """, unsafe_allow_html=True)

            with cB:
                st.markdown(f"""
                <div class="count-card">
                    {active_c}
                    <div class="label-text">{ACTIVE_ICON} Active Resources</div>
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # -----------------------------------------
            # Pie Chart
            # -----------------------------------------
            if len(df2["status"].unique()) > 0:
                pie_df = df2["status"].value_counts().reset_index()
                pie_df.columns = ["status", "count"]

                pie_chart = (
                    alt.Chart(pie_df)
                    .mark_arc()
                    .encode(
                        theta=alt.Theta(field="count", type="quantitative"),
                        color=alt.Color(field="status", type="nominal"),
                        tooltip=["status", "count"]
                    )
                )

                st.subheader("Status Distribution")
                st.altair_chart(pie_chart, use_container_width=True)
            else:
                st.warning("⚠ No valid status information available for generating pie chart.")

            st.divider()

            # -----------------------------------------
            # Scatter Plot
            # -----------------------------------------
            st.subheader("CPU vs Memory Utilization")

            if "cpu_utilization" in df2.columns and "memory_utilization" in df2.columns:
                scatter = (
                    alt.Chart(df2)
                    .mark_circle(size=80)
                    .encode(
                        x="cpu_utilization",
                        y="memory_utilization",
                        color="status",
                        tooltip=list(df2.columns),
                    )
                )
                st.altair_chart(scatter, use_container_width=True)
            else:
                st.warning("⚠ Unable to generate scatter plot. Missing columns.")

            st.divider()

            # -----------------------------------------
            # Data Table
            # -----------------------------------------
            st.subheader("Full Analyzed Table")
            st.dataframe(df2, use_container_width=True, height=500)

            # -----------------------------------------
            # Download Button
            # -----------------------------------------
            csv_download = df2.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇ Download Processed CSV",
                data=csv_download,
                file_name="processed_cloud_resources.csv",
                mime="text/csv"
            )

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# TAB 4 — HISTORY
# -----------------------------
with tabs[3]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='display:flex;align-items:center;gap:10px'>{USER_ICON} Your Prediction History</h3>", unsafe_allow_html=True)

    user_email = st.session_state["user"].get("email")
    try:
        history = find_predictions_by_user_email(user_email, limit=500)
        if history:
            df_hist = pd.DataFrame(history)
            # present a nicer table (flatten a bit)
            if "resource_snapshot" in df_hist.columns:
                df_hist["resource_id"] = df_hist["resource_snapshot"].apply(lambda x: x.get("resource_id") if isinstance(x, dict) else "")
            st.dataframe(df_hist.sort_values("_id", ascending=False).reset_index(drop=True), use_container_width=True)
        else:
            st.info("No prediction history yet. Run a prediction to start saving history.")
    except Exception as e:
        st.error(f"Error retrieving history: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
