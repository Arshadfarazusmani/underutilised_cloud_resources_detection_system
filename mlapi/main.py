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
