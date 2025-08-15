# backend/model.py

import matplotlib.pyplot as plt
from preprocess import load_and_preprocess
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error
from features import generate_features
from sklearn.preprocessing import StandardScaler
import os

def train_model(category, test_size=30):
    df = generate_features(category)

    # Define features and target
    feature_cols = [col for col in df.columns if col not in ['Date', category]]
    X = df[feature_cols]
    y = df[category]

    # Time-based train-test split
    X_train, X_test = X[:-test_size], X[-test_size:]
    y_train, y_test = y[:-test_size], y[-test_size:]

    # Scale and train
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
    model.fit(X_train_scaled, y_train)

    # Predict and evaluate
    y_pred = model.predict(X_test_scaled)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"✅ Model trained for {category}")
    print(f"📊 RMSE: {rmse:.2f}, MAE: {mae:.2f}")

    # Save model & scaler
    model_path = r"D:\Projects\Retail Sales Prediction\backend\models"
    os.makedirs(model_path, exist_ok=True)
    joblib.dump(model, os.path.join(model_path, f"{category}_xgb_model.pkl"))
    joblib.dump(scaler, os.path.join(model_path, f"{category}_scaler.pkl"))

    # Plot actual vs predicted
    plot_predictions(y_test, y_pred, category)

    return rmse, mae



def plot_predictions(y_test, y_pred, category):
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.index, y_test, label="Actual Sales", color='blue')
    plt.plot(y_test.index, y_pred, label="Predicted Sales", color='orange', linestyle='--')
    plt.title(f'Predicted vs Actual Sales for {category}')
    plt.xlabel('Date')
    plt.ylabel('Sales Quantity')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"backend/models/{category}_prediction_plot.png")
    plt.close()

# Run the training and visualization
if __name__ == "__main__":
    filepath = r"D:\Projects\Retail Sales Prediction\backend\data\retail_data.csv"
    df = load_and_preprocess()

    # Don't drop "Date" – it's not a column, it's the index
    category_columns = df.columns
    print(f"📦 Categories found: {list(category_columns)}\n")

    metrics = {}
    for category in category_columns:
        print(f"🚀 Training model for category: {category}")
        rmse, mae = train_model(category)
        metrics[category] = {"RMSE": rmse, "MAE": mae}

    print("\n📊 Final Evaluation Metrics:")
    for cat, scores in metrics.items():
        print(f"{cat}: RMSE={scores['RMSE']:.2f}, MAE={scores['MAE']:.2f}")
