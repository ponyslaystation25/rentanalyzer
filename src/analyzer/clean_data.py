from csv_utils import read_csv, remove_rows_by_criteria
#from pandasgui import show
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

    # Convert all the "string" columns to an actual string type
    df['listing_type'] = df['listing_type'].astype(str)
    df['sale_rent'] = df['sale_rent'].astype(str)
    df['title'] = df['title'].astype(str)
    df['banner'] = df['banner'].astype(str)

    # Remove rows where the price is equal to 0
    df = remove_rows_by_criteria(df, lambda d: d['price'] == 0)
    # Remove row where both the land size and floor size are equal to 0
    df = remove_rows_by_criteria(df, lambda d: (d['land_size'] == 0) & (d['floor_size'] == 0))
    # Remove rows where the 'floor size' is more than 85 or the 'land size' is more than 85
    df = remove_rows_by_criteria(df, lambda d: (d['floor_size'] > 85)|(df['land_size'] > 85))
    # Remove rows where the listing type is 'Other' and 'House'
    df = remove_rows_by_criteria(df, lambda d: (d['listing_type'] == 'Other')|(d['listing_type'] == 'House'))
    # Remove rows where both land size and floor size are 'No land size found' and 'No floor size found'
    df = remove_rows_by_criteria(df, 
                                 lambda d: (d['land_size'] == 'No land size found') & 
                                            (d['floor_size'] == 'No floor size found'))
    # Remove rows where the banner is 'Under Offer' or 'Sold'
    df = remove_rows_by_criteria(df, lambda d: (d['banner'] == 'Under Offer') | 
                                            (d['banner'] == 'Sold'))
    # Remove rows where the sale_rent is 'Sale'
    df = remove_rows_by_criteria(df, lambda d: d['sale_rent'] == 'Sale')
    
    # Remove rows where the price is greater than 2,000,000
    # Remove rows where the price is greater than 25,000 
    df = remove_rows_by_criteria(df, lambda d: d['price'] > 2000000)
    df = remove_rows_by_criteria(df, lambda d: (d['price'] > 25000))
    
    return df

