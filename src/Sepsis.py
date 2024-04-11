from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load trained models and label encoder
gb_model = joblib.load("Models/gb_model.pkl")
lr_model = joblib.load("Models/lr_model.pkl")
label_encoder = joblib.load("Models/label_encoder.pkl")
scaler = joblib.load("Models/robust_scaler.pkl")  # Assuming you have saved RobustScaler

class Features(BaseModel):
    PRG: int
    PL: int
    PR: int
    SK: int
    TS: int
    M11: float
    BD2: float
    Age: int
    Insurance: int

@app.get("/")
async def root():
    return {"message": "Wellcome to Sepsis Prediction Application"}


@app.post("/predict_sepsis")
async def predict_sepsis(features: Features):
    # Convert features to numpy array
    feature_values = np.array([[
        features.PRG, features.PL, features.PR, features.SK, features.TS,
        features.M11, features.BD2, features.Age, features.Insurance
    ]])

    # Normalize features using RobustScaler
    normalized_features = scaler.transform(feature_values)

    # Predict Sepsis using the gradient boosting model
    gb_prediction = gb_model.predict(normalized_features)[0]

    # Predict Sepsis using the Logistic Regression model
    lr_prediction = lr_model.predict(normalized_features)[0]

    # Decode Sepsis using LabelEncoder
    decoded_sepsis_gb = label_encoder.inverse_transform([gb_prediction])[0]
    decoded_sepsis_lr = label_encoder.inverse_transform([lr_prediction])[0]

    return {
        "Gradient Boosting Prediction": decoded_sepsis_gb,
        "Logistic Regression Prediction": decoded_sepsis_lr
    }