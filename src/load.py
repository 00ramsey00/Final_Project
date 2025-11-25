#This code will pull data from 3 locations:
#Kaggle Housing Prices, Federal Reserve 30-Year Fixed Mortgage Rates, and Google Trends-Homes for sale
#Data will be saved as CSV files in "data" folder in the parent directory

import os
import time
import pandas as pd
import requests
from pytrends.request import TrendReq
from config import (
    DATA_DIR,
    KAGGLE_CONFIG_DIR,
    FRED_API_KEY,
    KAGGLE_DATASET,
    FRED_SERIES_ID,
    FRED_API_URL,
    KAGGLE_NAME, FRED_NAME, GOOGLE_NAME,
    START_DATE, END_DATE, time_sleep,
)

def clear_data_folder():
    # ----- CLEAN DATA FOLDER BEFORE STARTING -----
    for f in os.listdir(DATA_DIR):
        if f.endswith(".csv"):
            os.remove(DATA_DIR / f)
    #print("Cleaned old CSV files from data directory.")


#kaggle is also imported below but needs to be below path normalization because we're changing default location of kaggle API


def kaggle_housing(): #kaggle is a website with databases for public use
    #----------------------KAGGLE - Housing Prices Data Collection---------------------------
    os.environ["KAGGLE_CONFIG_DIR"] = KAGGLE_CONFIG_DIR  # Location of Kaggle API Key found from .env file
    #os.environ is a built-in Python dictionary that stores environment variables

    #print("Using Kaggle config dir:", kaggle_config_dir)

    import kaggle #This needs to be here after environment variable is set
    print("Fetching Housing Price data from Kaggle...")

    #Download dataset from Kaggle
    kaggle.api.dataset_download_files(KAGGLE_DATASET, path=DATA_DIR, unzip=True)  # connect to Kaggle using API key


    #and save to data directory created above. Unzip it automatically since its normally a zipped file

    #Find and load CSV file from the zip folder and put it into data folder
    #From this Kaggle dataset, there's only one CSV file so no need to tweak this code. It's good enough
    csv_file = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')][0]
    if not csv_file:
        raise FileNotFoundError("No CSV found after downloading Kaggle dataset")


    #df = pd.read_csv(csv_path)
    #print("Data loaded:", df.shape)
    #print(df.columns)
    original_csv_path = DATA_DIR / csv_file
    new_csv_path = DATA_DIR / KAGGLE_NAME

    # Rename/move the file to your chosen name
    os.rename(original_csv_path, new_csv_path)
    #-----------------------------------------------------------------------------------------------


def FRED_mortgage(): #FRED is the federal reserve database to pull mortgage rates from
    #----------------------FRED - 30-Year Fixed Mortgage Rates---------------------------

    #settings parameters before accessing FRED
    params = {
        "series_id": FRED_SERIES_ID,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }

    #Request data from FRED
    print(f"Fetching 30-Year Fixed Mortgage Rates ({FRED_SERIES_ID}) from FRED...")
    response = requests.get(FRED_API_URL, params=params)
    response.raise_for_status()  # Raises an error if request failed

    data = response.json()
    observations = data.get("observations", [])

    if not observations:
        raise ValueError("No data returned from FRED API")

    #Convert to pandas DataFrame
    df = pd.DataFrame(observations)
    #print(f"Data successfully loaded: {df.shape[0]} records")

    #Save raw data to CSV
    output_path = DATA_DIR / FRED_NAME
    df.to_csv(output_path, index=False)

    #print(f"Mortgage rate data saved to: {output_path}")
    #-----------------------------------------------------------------------------------------------




def GTrends_Homes_Selling(time_sleep): #Google Trends records trends in how people search on Google
    #------------------------------Google Trends - "Homes for sale"------------------------------

    #No API needed for this one but access is limited

    #Download Google Search Interest Data (via pytrends) ---
    print("Fetching Google Trends data for 'homes for sale'...")

    #Create a clean Trends session with explicit connection headers to avoid being banned as a bot similar to HW assignment
    pytrends = TrendReq(
        hl='en-US',
        tz=360,
        requests_args={
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/118.0.5993.90 Safari/537.36'
            }
        }
    )

    #Give Google a short pause between actions to prevent being blocked
    print(f"Please wait {time_sleep * 2} seconds . . .")
    time.sleep(time_sleep) #20 seconds is what we use as default 2 times for 40 seconds
    #time.sleep(20)

    #Pick data we want
    kw_list = ["homes for sale"] #search term we're working with
    pytrends.build_payload(kw_list, timeframe=f"{START_DATE} {END_DATE}", geo='US')  # set timeframe (20 years)

    #Pause again before fetch
    print(f"Please wait {time_sleep} seconds . . .")
    time.sleep(time_sleep)
    #time.sleep(20)
    df_trends = pytrends.interest_over_time()

    #Check
    if df_trends.empty:
        raise ValueError("No data returned from Google Trends for 'homes for sale'")

    #Save
    output_path = DATA_DIR / GOOGLE_NAME
    df_trends.to_csv(output_path)
    #print(f"Google Trends data saved to: {output_path}")
    #print("Data loaded:", df_trends.shape)
    #print(df_trends.head())
    #-----------------------------------------------------------------------------------------------



if __name__ == "__main__":
    print("----------------------Running Data Collection----------------------")
    clear_data_folder()
    kaggle_housing()
    FRED_mortgage()
    GTrends_Homes_Selling()
    print('All data successfully collected and saved to "Data" folder.')


