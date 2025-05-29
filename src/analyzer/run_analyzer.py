from clean_data import clean_data, filter_data
from csv_utils import read_csv, remove_rows_by_criteria
import pandas as pd
import math
import numpy as np
from pandasgui import show

# Read in the CSV file and clean the data
def read_and_clean_data():
    df = read_csv('C:\\Users\\zanes\\OneDrive\\Desktop\\Application_data\\listings.csv')
    df = clean_data(df)
    df = filter_data(df)
    return df

# Calculates the price per square meter
# If the floor size is greater than 0, use the floor size to calculate price per square meter
# Otherwise, use the land size to calculate price per square meter
def calculate_price_per_m2(df): 
    df['price per m2'] = np.where(
        df['floor_size'] > 0,
        df['price'] / df['floor_size'],
        df['price'] / df['land_size'],
    )
    return df

# Count the number of listings for each title and sale type
# Group by title and sale type, and count the number of listings
# title_type_counts = df.groupby(['title', 'sale_rent']).size().reset_index(name='count')
def get_rent_per_m2_stats(df):
    
    # Filter only the listings that are to rent
    rent_df = df[df['sale_rent'] == 'Rent']
    # Calculate the mean and stddev of rent per m2 per title
    rent_per_m2_stats = rent_df.groupby('title')['price per m2'].agg(['mean', 'max', 'min', 'std']).reset_index()
    # Rename the columns
    rent_per_m2_stats.rename(columns={'mean': 'mean rent per m2', 'max': 'max rent per m2', 'min': 'min rent per m2', 'std': 'stddev rent per m2'}, inplace=True)
    # Sort values by mean rent per m2
    rent_per_m2_stats = rent_per_m2_stats.sort_values(by='mean rent per m2', ascending=False)
    # Remove entries where stddev rent per m2 is NaN
    rent_per_m2_stats = rent_per_m2_stats.dropna(subset=['stddev rent per m2'])
    # Calculate the count of rental listings per title
    rent_counts = rent_df['title'].value_counts().reset_index(name='rental_count')
    # Merge the rental counts with the rent per m2 stats
    rent_per_m2_stats = rent_per_m2_stats.merge(rent_counts, on='title', how='left')
    return rent_per_m2_stats


#-------------------------------------------------------------------------
# ---- Identify outliers and stability ---
# High max rate signals premium locations but also higher risk --> High vacancy rate and maintanance costs
# Low min rate can signal undervalues properties but also dangerous locations
# High stddev rate signals high volatility in the market
# Low stddev rate signals stability in the market and less risk
def top_15_mean_rent_per_m2(df):
    top_15_mean_rent_per_m2 = df.nlargest(15, 'mean rent per m2')[['title', 'mean rent per m2', 'rental_count']]
    return top_15_mean_rent_per_m2

def top_15_rent_per_m2(df):
    top_15_max_rent_per_m2 = df.nlargest(15, 'max rent per m2')[['title', 'max rent per m2', 'rental_count']]
    return top_15_max_rent_per_m2

def low_15_mean_rent_per_m2(df):
    low_15_mean_rent_per_m2 = df.nsmallest(15, 'mean rent per m2')[['title', 'min rent per m2', 'rental_count']]
    return low_15_mean_rent_per_m2

def low_15_min_rent_per_m2(df):
    low_15_min_rent_per_m2 = df.nsmallest(15, 'min rent per m2')[['title', 'min rent per m2', 'rental_count']]
    return low_15_min_rent_per_m2

def top_15_stddev_rent_per_m2(df):
    top_15_stddev_rent_per_m2 = df.nlargest(15, 'stddev rent per m2')[['title', 'stddev rent per m2', 'rental_count']]
    return top_15_stddev_rent_per_m2

def low_15_stddev_rent_per_m2(df):
    low_15_stddev_rent_per_m2 = df.nsmallest(15, 'stddev rent per m2')[['title', 'stddev rent per m2', 'rental_count']]
    return low_15_stddev_rent_per_m2

#-------------------------------------------------------------------------
# top_15_rent_per_m2()
# low_15_min_rent_per_m2()
# top_15_stddev_rent_per_m2()
# low_15_stddev_rent_per_m2()

# ------------------------------------------------------------------------
# ---- Income Approach ----
# Annual gross rent income: mean rent per m2 * [floor size] *12
# Capitalization rate: annual gross rent income / [price] * 100
# Aim for a cap rate exceeding the risk free rate (8-12%), the higher the better
def calculate_income_approach(title, price, floor_size, rent_per_m2_stats):
    # Get the mean rent per m2 for the title
    mean_rent_per_m2 = rent_per_m2_stats.loc[rent_per_m2_stats['title'] == title, 'mean rent per m2'].values[0]
    # Get the stddev rent per m2 for the title
    stddev_rent_per_m2 = rent_per_m2_stats.loc[rent_per_m2_stats['title'] == title, 'stddev rent per m2'].values[0]
    # Calculate the monthly gross rent income spread
    monthly_gross_rent_income = mean_rent_per_m2 * floor_size
    stddev_monthly_gross_rent_income = stddev_rent_per_m2 * floor_size
    # Calculate the annual gross rent income spread
    annual_gross_rent_income = monthly_gross_rent_income * 12
    stddev_annual_gross_rent_income = stddev_monthly_gross_rent_income * 12
    # Calculate the capitalization rate
    cap_rate = (annual_gross_rent_income / price) * 100
    stddev_cap_rate = (stddev_annual_gross_rent_income / price) * 100
    return monthly_gross_rent_income, stddev_monthly_gross_rent_income, annual_gross_rent_income,stddev_annual_gross_rent_income, cap_rate, stddev_cap_rate

# # Call the function and unpack the results
# (
#     monthly_gross_rent_income,
#     stddev_monthly_gross_rent_income,
#     annual_gross_rent_income,
#     stddev_annual_gross_rent_income,
#     cap_rate,
#     stddev_cap_rate
# ) = calculate_income_approach('De Velde', 1750000, 82)

# print(f"Monthly Gross Rent Income: {monthly_gross_rent_income:,.2f}")
# print(f"Monthly Gross Rent Income Stddev: {stddev_monthly_gross_rent_income:,.2f}")
# print(f"Annual Gross Rent Income: {annual_gross_rent_income:,.2f}")
# print(f"Annual Gross Rent Income Stddev: {stddev_annual_gross_rent_income:,.2f}")
# print(f"Capitalization Rate: {cap_rate:.2f}%")
# print(f"Capitalization Rate Stddev: {stddev_cap_rate:.2f}%")
# ------------------------------------------------------------------------    

# ---- Gross rent multiplier ----
# Gross rent multiplier: [price] / annual gross rent income
# Aim for a GRM below 10, the lower the better. Compare with the average GRM in the area and/or other similar properties
def calculate_gross_rent_multiplier(price, annual_gross_rent_income):
    gross_rent_multiplier = price / annual_gross_rent_income
    return gross_rent_multiplier

# ---- Risk Assessment with Z-Score ----
# Z-Score: (value - mean) / stddev
# A Z-Score above 2 or below -2 is considered an outlier
def calculate_z_score(title, price):
    # Get the mean rent per m2 for the title
    mean_rent_per_m2 = rent_per_m2_stats.loc[rent_per_m2_stats['title'] == title, 'mean rent per m2'].values[0]
    # Get the stddev rent per m2 for the title
    stddev_rent_per_m2 = rent_per_m2_stats.loc[rent_per_m2_stats['title'] == title, 'stddev rent per m2'].values[0]
    # Calculate the Z-Score
    z_score = (price - mean_rent_per_m2) / stddev_rent_per_m2
    return z_score

# ---- Risk Assessment with CAPM ----
# CAPM: Expected return = Risk-free rate + Beta * (Market return - Risk-free rate)
# Beta: A measure of the volatility, or systematic risk, of a security or portfolio in comparison to the market as a whole


# ---- Price to Earnings Ratio ----
# Price to earnings ratio: [price] / [annual gross rent income]
# Aim for a P/E ratio below 20, the lower the better. Compare with the average P/E ratio in the area and/or other similar properties
def calculate_price_to_earnings_ratio(price, annual_gross_rent_income):
    price_to_earnings_ratio = price / annual_gross_rent_income
    return price_to_earnings_ratio

def analyze(csv_path = 'C:\\Users\\zanes\\OneDrive\\Desktop\\Application_data\\listings.csv'):
    # Read and clean the data
    df = read_and_clean_data()
    # Calculate price per m2
    df = calculate_price_per_m2(df)
    # Get rent per m2 stats
    rent_per_m2_stats = get_rent_per_m2_stats(df)
    
    return df, rent_per_m2_stats
#show(rent_per_m2_stats)

if __name__ == "__main__":
    df, rent_per_m2_stats = analyze()
    show(rent_per_m2_stats)
