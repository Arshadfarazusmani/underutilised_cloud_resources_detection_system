# from fastapi import FastAPI
# from pydantic import BaseModel
# import joblib
# import pandas as pd

# # -------- Load model & scaler ----------
# model = joblib.load("idle_resource_rf_model_02 (1).joblib")
# scaler = joblib.load("scaler_02 (1).joblib")
# print("\n🔍 MODEL FEATURE ORDER:")
# print(list(scaler.feature_names_in_))
# print("------------------------------------------------------\n")


# app = FastAPI()

# # -------- Request body schema ----------
# class ResourceMetrics(BaseModel):
#     resource_id: str
#     resource_type: str       # e.g. "VM", "Storage", "Database", "Container"
#     cpu_utilization: float
#     memory_utilization: float
#     disk_io: float
#     network_io: float
#     last_access_days_ago: float
#     provisioned_cpu_cores:float
#     provisioned_capacity_gb:float
    

# @app.get("/")
# def root():
#     return {"message": "Idle Resource ML API is running"}

# @app.post("/predict")

# def predict_resource(data: ResourceMetrics):

   
#     # Convert input to DataFrame
#     df = pd.DataFrame([data.dict()])

#     # Build all columns the model expects
#     expected_features = [
#         'cpu_utilization',
#         'memory_utilization',
#         'network_io',
#         'disk_io',
#         'last_access_days_ago',
#         'provisioned_capacity_gb',
#         'provisioned_cpu_cores',
#         'resource_type_VM'
#     ]

#     # Handle one-hot manually (because your model only uses 1)
#     df["resource_type_VM"] = 1 if df["resource_type"].iloc[0] == "VM" else 0

#     # Make sure all expected columns exist
#     expected_cols = [
#         "resource_type_Container",
#         "resource_type_Database",
#         "resource_type_Storage",
#         "resource_type_VM",
#     ]

#     for col in expected_cols:
#         if col not in df.columns:
#             df[col] = 0



#     # Sort columns for consistency
#     df = df.reindex(sorted(df.columns), axis=1)

#     # Drop ID column before scaling & prediction
#     X = df.drop(columns=["resource_id"], errors="ignore")



#     # Fill missing numeric fields if needed
#     df["last_access_days_ago"] = df.get("last_access_days_ago", 0)
#     df["provisioned_cpu_cores"] = df.get("provisioned_cpu_cores", 0)
#     df["provisioned_capacity_gb"] = df.get("provisioned_capacity_gb", 0)

#     # Drop non-feature columns
#     df = df.drop(columns=["resource_type", "resource_id"], errors="ignore")

#     # Reorder the DataFrame EXACTLY as scaler expects
#     df = df[expected_features]

#     print("\n🟦 INPUT TO MODEL (before scaling):")
#     print(df)
#     print("------------------------------------------------------")

#     # Scale the features
#     X_scaled = scaler.transform(df)

#     print("\n🟩 INPUT TO MODEL (after scaling):")
#     print(X_scaled)
#     print("------------------------------------------------------")

#     # Predict
#     pred = model.predict(X_scaled)[0]
#     status = "Idle" if pred == 1 else "Active"

#     return {
#         "resource_id": data.resource_id,
#         "prediction": int(pred),
#         "status": status
#     }

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# -----------------------------------------------------------
# Load model & scaler
# -----------------------------------------------------------
model = joblib.load("idle_resource_rf_model_02 (1).joblib")
scaler = joblib.load("scaler_02 (1).joblib")

print("\n🔍 MODEL FEATURE ORDER:")
print(list(scaler.feature_names_in_))
print("------------------------------------------------------\n")

app = FastAPI(title="Idle Resource Detection API")

# -----------------------------------------------------------
# Request body schema
# -----------------------------------------------------------
class ResourceMetrics(BaseModel):
    resource_id: str
    resource_type: str         # VM, Storage, Database, Container
    cpu_utilization: float
    memory_utilization: float
    disk_io: float
    network_io: float
    last_access_days_ago: float
    provisioned_cpu_cores: float
    provisioned_capacity_gb: float


# -----------------------------------------------------------
# Root endpoint
# -----------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Idle Resource ML API is running"}


# -----------------------------------------------------------
# Prediction endpoint
# -----------------------------------------------------------
@app.post("/predict")
def predict_resource(data: ResourceMetrics):

    # Convert input to DataFrame
    df = pd.DataFrame([data.dict()])

    # -------------------------------------------------------
    # Expected features (in exact scaler/model order)
    # -------------------------------------------------------
    expected_features = list(scaler.feature_names_in_)

    # -------------------------------------------------------
    # One-hot encode resource_type (manual handling)
    # Your model includes these columns:
    #   resource_type_Container
    #   resource_type_Database
    #   resource_type_Storage
    #   resource_type_VM
    # -------------------------------------------------------
    resource_types = ["Container", "Database", "Storage", "VM"]
    for rt in resource_types:
        df[f"resource_type_{rt}"] = 1 if df["resource_type"].iloc[0] == rt else 0

    # Drop unused non-feature fields
    df = df.drop(columns=["resource_type", "resource_id"], errors="ignore")

    # -------------------------------------------------------
    # Ensure all expected model features exist
    # -------------------------------------------------------
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0

    # -------------------------------------------------------
    # Reorder columns to match model training order exactly
    # -------------------------------------------------------
    df = df[expected_features]

    # DEBUG prints (optional)
    print("\n🟦 INPUT TO MODEL (before scaling):")
    print(df)
    print("------------------------------------------------------")

    # -------------------------------------------------------
    # Apply scaling
    # -------------------------------------------------------
    X_scaled = scaler.transform(df)

    print("\n🟩 INPUT TO MODEL (after scaling):")
    print(X_scaled)
    print("------------------------------------------------------")

    # -------------------------------------------------------
    # Predict
    # -------------------------------------------------------
    prediction = model.predict(X_scaled)[0]
    status = "Idle" if prediction == 1 else "Active"

    return {
        "resource_id": data.resource_id,
        "prediction": int(prediction),
        "status": status
    }


# -----------------------------------------------------------
# Run with:
# uvicorn app:app --reload --port 8000
# -----------------------------------------------------------
