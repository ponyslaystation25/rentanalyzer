import pandas as pd

def read_csv(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        pd.DataFrame: The DataFrame containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    
def remove_rows_by_criteria(df: pd.DataFrame, criteria) -> pd.DataFrame:
    """
    Removes rows from a DataFrame based on specified criteria.
    
    Args:
        df (pd.DataFrame): The DataFrame to filter.
        criteria (dict): A dictionary where keys are column names and values are the values to remove.
    
    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    mask = criteria(df)
    return df[~mask]