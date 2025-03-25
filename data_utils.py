# utils/data_utils.py
import pandas as pd

def load_data(filepath):
    """Load a CSV file into a DataFrame."""
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """Clean the DataFrame by dropping NA values (extend as needed)."""
    df.dropna(inplace=True)
    return df
