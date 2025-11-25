#This code will clean and process the 3 sets of data pulled from load.py
#Cleaned Data will be saved as CSV files in "data/processed" folder in the parent directory


import pandas as pd
import os
from config import (
    DATA_DIR, PROCESSED_DIR,
    KAGGLE_NAME, FRED_NAME, GOOGLE_NAME,
    KAGGLE_NAME_CLEAN, FRED_NAME_CLEAN, GOOGLE_NAME_CLEAN, MERGED_CLEAN,
    START_DATE, END_DATE,
)


def clear_processed_folder():
    # ----- CLEAN DATA/PROCESSED FOLDER BEFORE STARTING -----
    for f in os.listdir(PROCESSED_DIR):
        if f.endswith(".csv"):
            os.remove(PROCESSED_DIR / f)
    #print("Cleaned old CSV files from data/processed directory.")


# Process Realtor Data (using prev_sold_date as date)
def process_realtor_data(filename: str) -> pd.DataFrame: #This is the CSV from Kaggle Housing Data
    # Only keep: prev_sold_date (renamed to 'date'), price, state

    print("Cleaning Housing Price data from Kaggle...")

    # Get correct full path to data folder
    full_path = DATA_DIR / filename

    # Load CSV file into DataFrame
    df = pd.read_csv(full_path)

    # Keep only the columns we actually need
    df = df[["prev_sold_date", "price", "state"]]

    # Rename prev_sold_date to date
    df = df.rename(columns={"prev_sold_date": "date"})

    # Convert the date column into a real datetime type
    df["date"] = pd.to_datetime(df["date"], errors="coerce") #errors = coerce is the same as skip if error comes up, it prevents crashing

    # Convert price to a numeric column just in case
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Drop rows where date or price is missing
    df = df.dropna(subset=["date", "price"])

    # Filter to 20 year range
    df = df[(df["date"] >= START_DATE) & (df["date"] <= END_DATE)]

    # Sort by date from oldest to newest
    df = df.sort_values(by="date", ascending=True)

    # Convert to YYYY-MM format
    df["date"] = df["date"].dt.strftime("%m/%d/%Y")

    # Save the cleaned version in the new processed folder
    out_path = PROCESSED_DIR / KAGGLE_NAME_CLEAN
    df.to_csv(out_path, index=False)

    return df


# Process FRED mortgage data (convert from weekly to monthly using averages for the months)
def process_mortgage_data(filename: str) -> pd.DataFrame:
    print("Cleaning 30-Year Fixed Mortgage Rates from FRED...")

    # Get correct full path to data folder
    full_path = DATA_DIR / filename

    # Load the CSV
    df = pd.read_csv(full_path)

    # Convert date to datetime and value to numeric
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Drop nulls just in case and keep only needed columns
    df = df.dropna(subset=["date", "value"])

    # Filter by our date range of 20 years, get rid of older years
    df = df[(df["date"] >= START_DATE) & (df["date"] <= END_DATE)]

    #Create monthly period column (ex: 2020-05) since mortgage is given weekly
    df["month"] = df["date"].dt.to_period("M")

    # Group by month to get average mortgage rate for that month
    grouped = df.groupby("month") #Group everything by the month column
    monthly_values = grouped["value"] #From these groups, select only the "value" column (mortgage rate)
    monthly_average = monthly_values.mean() #Compute the average mortgage rate for each month
    df_monthly = monthly_average.reset_index() #Convert the result with month and value columns

    # Convert month period to first of the month timestamp
    df_monthly["month"] = df_monthly["month"].dt.to_timestamp()

    # Sort by date oldest to newest
    df_monthly = df_monthly.sort_values(by="month")

    # Save cleaned version
    out_path = PROCESSED_DIR / FRED_NAME_CLEAN
    df_monthly.to_csv(out_path, index=False)

    return df_monthly


# Process Google Trends data
def process_google_data(filename: str) -> pd.DataFrame:
    print("Cleaning Google Trends data...")

    # Get correct full path to data folder
    full_path = DATA_DIR / filename

    # Load the CSV
    df = pd.read_csv(full_path)

    # Convert date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Keep only the columns we need
    df = df[["date", "homes for sale"]]

    # Filter to 20 year range
    df = df[(df["date"] >= START_DATE) & (df["date"] <= END_DATE)]

    # Convert google score to numeric
    df["homes for sale"] = pd.to_numeric(df["homes for sale"], errors="coerce")

    # Sort oldest to newest
    df = df.sort_values(by="date")

    # Save the cleaned version in the new processed folder
    out_path = PROCESSED_DIR / GOOGLE_NAME_CLEAN
    df.to_csv(out_path, index=False)

    return df


def process_merge_data(): #This is what we use to merge the data we want from the 3 into 1 csv file
    #Merges the cleaned realtor, google trends, and mortgage datasets into one monthly dataset and saves as merged.csv
    print("Further processing and merging data...")

    # Load processed datasets
    realtor_path = PROCESSED_DIR / KAGGLE_NAME_CLEAN
    google_path = PROCESSED_DIR / GOOGLE_NAME_CLEAN
    mortgage_path = PROCESSED_DIR / FRED_NAME_CLEAN

    df_realtor = pd.read_csv(realtor_path)
    df_google = pd.read_csv(google_path)
    df_mortgage = pd.read_csv(mortgage_path)


    # Convert date columns back to datetime so Python can work with it
    df_realtor["date"] = pd.to_datetime(df_realtor["date"])
    df_google["date"] = pd.to_datetime(df_google["date"])
    df_mortgage["month"] = pd.to_datetime(df_mortgage["month"]) #column is already monthly


    # Realtor to Monthly Average Price
    df_realtor["month"] = df_realtor["date"].dt.to_period("M")  # YYYY-MM
    monthly_group = df_realtor.groupby("month")["price"].mean()
    df_prices = monthly_group.reset_index()
    df_prices["month"] = df_prices["month"].dt.to_timestamp()  # YYYY-MM-01
    df_prices = df_prices.rename(columns={"price": "avg_price"})


    # Google Trends to Monthly
    df_google = df_google.rename(columns={"date": "month", "homes for sale": "search_interest"})


    # Mortgage Rates to Monthly
    df_mortgage = df_mortgage.rename(columns={"month": "month", "value": "mortgage_rate"})


    # Merge all three on 'month'
    df_merged = df_prices.merge(df_google, on="month", how="inner")
    df_merged = df_merged.merge(df_mortgage, on="month", how="inner")


    # Sort
    df_merged = df_merged.sort_values(by="month")

    #--------------------------------For Future Analysis-------------------
    # This is here but not used for final project. May look into further for future analysis
    # Add % change in house prices (month-over-month) and mortgage %
    df_merged["price_pct_change"] = df_merged["avg_price"].pct_change() * 100
    df_merged["mortgage_pct_change"] = df_merged["mortgage_rate"].pct_change() * 100
    df_merged["search_pct_change"] = df_merged["search_interest"].pct_change() * 100

    # Round both to 1 decimal place
    df_merged["price_pct_change"] = df_merged["price_pct_change"].round(1)
    df_merged["mortgage_pct_change"] = df_merged["mortgage_pct_change"].round(1)
    df_merged["search_pct_change"] = df_merged["search_pct_change"].round(1)

    #This is here but not used for final project. May look into further for future analysis
    # Direction columns (-1, 0, 1) This is focusing simply on whether data went up or down, ignoring all the numbers
    df_merged["price_direction"] = df_merged["price_pct_change"].apply(
        lambda x: 1 if x > 0 else (0 if x == 0 else -1)
    )
    df_merged["mortgage_direction"] = df_merged["mortgage_pct_change"].apply(
        lambda x: 1 if x > 0 else (0 if x == 0 else -1)
    )
    df_merged["search_direction"] = df_merged["search_pct_change"].apply(
        lambda x: 1 if x > 0 else (0 if x == 0 else -1)
    )

    # ^^^^^^^^^^^^^^^^^^^^ For Future Analysis (but I still want it in the excel sheet for now) ^^^^^^^^^^^^^^^^^^^^


    #Convert month to MM/DD/YYYY (always 1st day of the month)
    df_merged["month"] = df_merged["month"].dt.strftime("%m/%d/%Y")


    # Save
    out_path = PROCESSED_DIR / MERGED_CLEAN
    df_merged.to_csv(out_path, index=False)

    return df_merged


if __name__ == "__main__":
    print("----------------------Running Data Cleaning/Processing----------------------")
    clear_processed_folder()
    process_realtor_data(KAGGLE_NAME)
    process_mortgage_data(FRED_NAME)
    process_google_data(GOOGLE_NAME)
    process_merge_data()
    print("All data successfully cleaned and saved to data/processed folder.")
