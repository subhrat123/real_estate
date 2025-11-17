import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data/real_estate.xlsx")

def load_data():
    """
    Loads the real estate data from the excel file, handles missing values,
    and returns a cleaned DataFrame.
    """
    df = pd.read_excel(DATA_PATH)
    
    # Log original shape
    logger.info(f"Original data shape: {df.shape}")
    
    # Handle missing values
    # Drop rows with missing 'final location' or 'year'
    initial_rows = len(df)
    df.dropna(subset=['final location', 'year'], inplace=True)
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0:
        logger.info(f"Dropped {rows_dropped} rows with missing 'final location' or 'year'.")

    # Fill missing numerical columns with 0
    numerical_cols = ['flat - weighted average rate', 'total units']
    for col in numerical_cols:
        missing_before = df[col].isnull().sum()
        if missing_before > 0:
            df[col].fillna(0, inplace=True)
            logger.info(f"Filled {missing_before} missing values in '{col}' with 0.")
            
    # Log cleaned shape
    logger.info(f"Cleaned data shape: {df.shape}")
    
    return df
