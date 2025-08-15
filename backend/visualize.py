# backend/visualize.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess import load_and_preprocess

sns.set(style="whitegrid")

def plot_category_trends(ts_df):
    plt.figure(figsize=(14, 6))
    ts_df.plot(ax=plt.gca())
    plt.title("Daily Sales Quantity per Product Category")
    plt.xlabel("Date")
    plt.ylabel("Quantity Sold")
    plt.legend(title='Product Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_seasonality(ts_df, category_name):
    df_cat = ts_df[[category_name]].copy()
    df_cat['Month'] = df_cat.index.month
    df_cat['Year'] = df_cat.index.year
    df_cat['Day'] = df_cat.index.dayofweek

    plt.figure(figsize=(12, 4))
    sns.lineplot(x='Month', y=category_name, data=df_cat.reset_index(), ci=None)
    plt.title(f'Monthly Seasonality for {category_name}')
    plt.xlabel("Month")
    plt.ylabel("Avg Quantity Sold")
    plt.show()

def run_all_visuals():
    ts_df = load_and_preprocess()
    print("📈 Plotting sales trends...")
    plot_category_trends(ts_df)

    # Optional: plot for top category
    top_category = ts_df.sum().sort_values(ascending=False).index[0]
    print(f"🔍 Plotting seasonality for top category: {top_category}")
    plot_seasonality(ts_df, top_category)

# Run manually
if __name__ == "__main__":
    run_all_visuals()
