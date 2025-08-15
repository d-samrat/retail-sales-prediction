# backend/preprocess.py

import pandas as pd

def load_and_preprocess():
    filepath=r"D:\Projects\Retail Sales Prediction\backend\data\retail_data.csv"
    df = pd.read_csv(filepath)
    
    # Convert date column
    df['Date'] = pd.to_datetime(df['Date'])

    # Drop rows with missing essential values
    df.dropna(subset=['Date', 'Product Category', 'Quantity'], inplace=True)

    # Ensure correct types
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df = df.dropna(subset=['Quantity'])

    # Aggregate daily demand per product category
    ts_df = df.groupby(['Date', 'Product Category'])['Quantity'].sum().reset_index()

    # Pivot to get each category as a column (optional, for multivariate models)
    pivot_df = ts_df.pivot(index='Date', columns='Product Category', values='Quantity').fillna(0)

    return pivot_df
