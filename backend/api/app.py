# backend/api/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.middleware.cors import CORSMiddleware
from preprocess import load_and_preprocess
from features import generate_features

# Initialize FastAPI
app = FastAPI()

def get_features_for_date(category: str, target_date: str):
    df = generate_features(category)
    
    # Ensure the date exists in the dataframe
    if target_date not in df.index:
        raise ValueError("Selected date is not available in the dataset or lacks enough history.")
    
    row = df.loc[target_date]

    # Extract the required features from the row
    feature_cols = [col for col in df.columns if col not in ['Date', category]]
    features = row[feature_cols]

    # Add dummy 0.0 for base product columns (used during training)
    features["Beauty"] = 0.0
    features["Electronics"] = 0.0
    return features

# Allow CORS (for React or frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to ['http://localhost:3000'] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input schema using Pydantic
class SalesRequest(BaseModel):
    category: str
    date: str  # format: YYYY-MM-DD



# Load model + scaler from disk
def load_model_and_scaler(category):
    base_path = r"D:\Projects\Retail Sales Prediction\backend\models"
    try:
        model = joblib.load(os.path.join(base_path, f"{category}_xgb_model.pkl"))
        scaler = joblib.load(os.path.join(base_path, f"{category}_scaler.pkl"))
        return model, scaler
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model/scaler: {str(e)}")

# Prediction endpoint
@app.post("/predict_sales/")
def predict_sales(request: SalesRequest):
    try:
        model, scaler = load_model_and_scaler(request.category)

        features = get_features_for_date(request.category, request.date)

        input_df = pd.DataFrame([features])

        # Match the order of columns
        input_df = input_df[scaler.feature_names_in_]

        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)

        return {"predicted_sales": float(prediction[0])}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")




