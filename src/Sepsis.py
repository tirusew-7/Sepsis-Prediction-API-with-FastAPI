import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.base import TransformerMixin
from notebook import SkewnessTransformer

app = FastAPI()

# Load trained models and label encoder
random_forest_model = joblib.load("Models/random_forest_model.pkl")
logistic_regression_model = joblib.load("Models/decision_tree_model.pkl")
label_encoder = joblib.load("Models/label_encoder.pkl")
scaler = joblib.load("Models/preprocessor.pkl")  # Assuming you have saved RobustScaler

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

@app.post("/predict_sepsis")
async def predict_sepsis(features: Features):
    # Convert features to numpy array
    feature_values = np.array([[
        features.PRG, features.PL, features.PR, features.SK, features.TS,
        features.M11, features.BD2, features.Age, features.Insurance
    ]])

    # Normalize features using RobustScaler
    normalized_features = scaler.transform(feature_values)

    # Predict Sepsis using the Random Forest model
    rf_prediction = random_forest_model.predict(normalized_features)[0]

    # Predict Sepsis using the Logistic Regression model
    dt_prediction = logistic_regression_model.predict(normalized_features)[0]

    # Decode Sepsis using LabelEncoder
    decoded_sepsis_rf = label_encoder.inverse_transform([rf_prediction])[0]
    decoded_sepsis_dt = label_encoder.inverse_transform([dt_prediction])[0]

    return {
        "Random Forest Prediction": decoded_sepsis_rf,
        "Random Tree Prediction": decoded_sepsis_dt
    }