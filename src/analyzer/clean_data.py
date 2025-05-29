from csv_utils import read_csv, remove_rows_by_criteria
from pandasgui import show
import pandas as pd
 
def clean_data(df):
    """
    Cleans the DataFrame by removing rows based on specific criteria.
    Also converts certain columns to numeric types and handles errors.
    
    Args:
        df (pd.DataFrame): The DataFrame to clean.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Convert 'price' column to numeric, forcing errors to NaN
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

    # Convert the "floor_size" and "land_size" columns to numeric, forcing errors to NaN
    df['floor_size'] = pd.to_numeric(df['floor_size'], errors='coerce').fillna(0)
    df['land_size'] = pd.to_numeric(df['land_size'], errors='coerce').fillna(0)

    # Convert the "bathrooms" and "bedrooms" columns to numeric, forcing errors to NaN
    df['bathrooms'] = pd.to_numeric(df['bathrooms'], errors='coerce').fillna(0)
    df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce').fillna(0)

    # Remove rows where the price is equal to 0
    df = remove_rows_by_criteria(df, lambda d: d['price'] == 0)
    # Remove row where both the land size and floor size are equal to 0
    df = remove_rows_by_criteria(df, lambda d: (d['land_size'] == 0) & (d['floor_size'] == 0))
    # Remove rows where the listing type is 'Other'
    df = remove_rows_by_criteria(df, lambda d: d['listing_type'] == 'Other')
    # Remove rows where both land size and floor size are 'No land size found' and 'No floor size found'
    df = remove_rows_by_criteria(df, 
                                 lambda d: (d['land_size'] == 'No land size found') & 
                                            (d['floor_size'] == 'No floor size found'))
    # Remove rows where the banner is 'Under Offer' or 'Sold'
    df = remove_rows_by_criteria(df, lambda d: (d['banner'] == 'Under Offer') | 
                                            (d['banner'] == 'Sold'))
    
    # Remove rows where the price is greater than 2,000,000
    # Remove rows where the price is greater than 25,000 and the sale type is 'Rent'
    df = remove_rows_by_criteria(df, lambda d: d['price'] > 2000000)
    df = remove_rows_by_criteria(df, lambda d: (d['price'] > 25000)&(d['sale_rent'] == 'Rent'))
    
    return df

def filter_data(df):
    """
    Filters the DataFrame based on specific criteria.
    
    Args:
        df (pd.DataFrame): The DataFrame to filter.
    
    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    # Filters out based on specific criteria (Hard coded for my needs)
    # Filter out rows where the price is greater than 2,000,000
    df = remove_rows_by_criteria(df, lambda d: d['price'] > 2000000)
    # Filter out rows where the price is greater than 25,000 and the sale type is 'Rent'
    df = remove_rows_by_criteria(df, lambda d: (d['price'] > 25000)&(d['sale_rent'] == 'Rent'))

    
    return df

#show(df())