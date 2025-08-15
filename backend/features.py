# backend/features.py

import pandas as pd
from preprocess import load_and_preprocess

def add_time_features(df):
    df = df.copy()
    df['Date'] = df.index
    df['dayofweek'] = df['Date'].dt.dayofweek
    df['month'] = df['Date'].dt.month
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    return df

def add_lag_features(df, category, lags=[1, 7, 14]):
    df = df.copy()
    for lag in lags:
        df[f'{category}_lag_{lag}'] = df[category].shift(lag)
    return df

def add_rolling_features(df, category, windows=[7]):
    df = df.copy()
    for window in windows:
        df[f'{category}_roll_mean_{window}'] = df[category].shift(1).rolling(window).mean()
    return df

def generate_features(category):
    df = load_and_preprocess()
    df = add_time_features(df)
    df = add_lag_features(df, category)
    df = add_rolling_features(df, category)
    df = df.dropna()  # Drop rows with NaNs from lags/rolling
    return df

# Run this to preview
if __name__ == "__main__":
    top_category = load_and_preprocess().sum().sort_values(ascending=False).index[0]
    feature_df = generate_features(top_category)
    print(f"Sample engineered features for {top_category}:")
    print(feature_df.head())
