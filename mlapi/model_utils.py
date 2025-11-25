# model_utils.py
import pandas as pd
import joblib
import os

# load (make sure files are named exactly)
MODEL_FILE = "idle_resource_rf_model_02 (1).joblib"
SCALER_FILE = "scaler_02 (1).joblib"

if not os.path.exists(MODEL_FILE):
    raise FileNotFoundError(f"{MODEL_FILE} not found. Put model file in project root.")

if not os.path.exists(SCALER_FILE):
    raise FileNotFoundError(f"{SCALER_FILE} not found. Put scaler file in project root.")

model = joblib.load(MODEL_FILE)
scaler = joblib.load(SCALER_FILE)
expected_features = list(scaler.feature_names_in_)

RESOURCE_TYPES = ["VM", "Storage", "Database", "Container"]

def prepare_features(row: dict):
    df = pd.DataFrame([row])
    # one-hot
    for rt in RESOURCE_TYPES:
        df[f"resource_type_{rt}"] = 1 if row.get("resource_type") == rt else 0
    df = df.drop(columns=["resource_type", "resource_id"], errors="ignore")
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0
    df = df[expected_features]
    X_scaled = scaler.transform(df)
    return X_scaled

def predict_row(row: dict):
    X = prepare_features(row)
    pred = model.predict(X)[0]
    status = "Idle" if int(pred) == 1 else "Active"
    return int(pred), status
