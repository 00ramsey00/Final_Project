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
    GOOGLE_SEARCH_TERM,
    KAGGLE_NAME, FRED_NAME, GOOGLE_NAME,
    START_DATE, END_DATE, time_sleep,
)

def clear_data_folder(data_dir=DATA_DIR):
    # ----- CLEAN DATA FOLDER BEFORE STARTING -----
    for f in os.listdir(data_dir):
        if f.endswith(".csv"):
            os.remove(data_dir / f)
    #print("Cleaned old CSV files from data directory.")


#kaggle is also imported below but needs to be below path normalization because we're changing default location of kaggle API


def kaggle_housing(data_dir=DATA_DIR, dataset=KAGGLE_DATASET, kaggle_config_dir = KAGGLE_CONFIG_DIR, KAGGLE_NAME = KAGGLE_NAME): #kaggle is a website with databases for public use
    #----------------------KAGGLE - Housing Prices Data Collection---------------------------
    #os.environ["KAGGLE_CONFIG_DIR"] = kaggle_config_dir  # Location of Kaggle API Key found from .env file
    # Validate Kaggle config directory
    try:
        if not kaggle_config_dir or not os.path.isdir(kaggle_config_dir):
            raise FileNotFoundError(
                f"Kaggle config directory not found: {kaggle_config_dir}"
            )

        # Apply it ONLY after confirming it exists
        os.environ["KAGGLE_CONFIG_DIR"] = kaggle_config_dir #os.environ is a built-in Python dictionary that stores environment variables

    except Exception as e:
        print("\nKAGGLE CONFIG ERROR: Kaggle configuration is invalid.")
        print("Reason:", e)
        print("Skipping Kaggle download...\n")
        return


    #print("Using Kaggle config dir:", kaggle_config_dir)


    try:
        import kaggle #This needs to be here after environment variable is set
    except Exception as e:
        print("KAGGLE IMPORT ERROR: This usually means your kaggle.json file is missing or invalid.")
        print(f"Expected kaggle.json in: {kaggle_config_dir}")
        print("Reason:", e)
        print("Skipping Kaggle download...")
        return #Stops kaggle_housing from continuing
    # -------------------------
    print(f"Fetching Kaggle Data: ({dataset})...")

    #Download dataset from Kaggle
    try:
        kaggle.api.dataset_download_files(dataset, path=data_dir, unzip=True)
    except Exception as e:
        print(f"KAGGLE DOWNLOAD ERROR: Dataset attempted: {dataset}")
        print("Reason:", e)
        print("Skipping Kaggle download...\n")
        return #Stops kaggle_housing from continuing


    #and save to data directory created above. Unzip it automatically since its normally a zipped file

    #Find and load CSV file from the zip folder and put it into data folder
    #From this Kaggle dataset, there's only one CSV file so no need to tweak this code. It's good enough

    csv_files = [f for f in os.listdir(data_dir) if f.lower().endswith(".csv")]
    # One final check if no CSV found -> dataset failed or was corrupt
    if not csv_files:
        print("KAGGLE DOWNLOAD ERROR: No CSV found in extracted files.")
        print("Skipping Kaggle download...\n")
        return

    # If multiple CSVs, warn but continue with the first
    if len(csv_files) > 1:
        print("KAGGLE DOWNLOAD WARNING: Multiple CSV files found from Kaggle dataset.")
        print("Using the first one:", csv_files[0])

    csv_file = csv_files[0]
    original_csv_path = data_dir / csv_file
    new_csv_path = data_dir / KAGGLE_NAME

    # Rename/move the file to your chosen name. I put an error check here just in case
    try:
        os.rename(original_csv_path, new_csv_path)
    except Exception as e:
        print("KAGGLE DOWNLOAD ERROR: Could not rename Kaggle CSV file.")
        print("Reason:", e)
        print("Skipping Kaggle renaming...\n")
        return
    #-----------------------------------------------------------------------------------------------


def FRED_mortgage(api_key=FRED_API_KEY, series_id=FRED_SERIES_ID, data_dir=DATA_DIR, FRED_NAME = FRED_NAME): #FRED is the federal reserve database to pull mortgage rates from
    #----------------------FRED - 30-Year Fixed Mortgage Rates---------------------------

    #settings parameters before accessing FRED
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }

    #Request data from FRED
    print(f"Fetching FRED Data: ({series_id})...")
    try:
        response = requests.get(FRED_API_URL, params=params)
        response.raise_for_status()   # this will error for bad API or series ID

    except Exception as e:
        print(f"\nFRED API request failed - Series attempted: {series_id}")
        print("Reason:", e)
        print("Skipping FRED download and continuing...\n")
        return

    data = response.json()
    observations = data.get("observations", [])

    if not observations:
        raise ValueError("No data returned from FRED API")

    #Convert to pandas DataFrame
    df = pd.DataFrame(observations)
    #print(f"Data successfully loaded: {df.shape[0]} records")

    #Save raw data to CSV
    output_path = data_dir / FRED_NAME
    df.to_csv(output_path, index=False)

    #print(f"Mortgage rate data saved to: {output_path}")
    #-----------------------------------------------------------------------------------------------




def GTrends_Homes_Selling(time_sleep=time_sleep, kw=GOOGLE_SEARCH_TERM, data_dir=DATA_DIR, GOOGLE_NAME = GOOGLE_NAME, START_DATE = START_DATE, END_DATE = END_DATE ): #Google Trends records trends in how people search on Google
    #------------------------------Google Trends - Default: "Homes for sale"------------------------------

    #No API needed for this one but access is limited

    #==========Before anything, check that the time_sleep is actually valid========
    #I decided to put this code here and not in tests.py or config.py because putting it here will prevent crashes regardless of run method
    # Must be an integer
    if not isinstance(time_sleep, int) or time_sleep < 1 or time_sleep > 40:
        print(f"Invalid sleep time '{time_sleep}' — must be an integer between 1 and 40. Defaulting to 20")
        time_sleep = 20
    #=========================================


    # ==========Now make sure the keyword is actually valid========
    if (not isinstance(kw, str)) or (kw.strip() == "") or (len(kw.split()) > 10):
        print(f"Invalid keyword '{kw}' — must be a non-empty string under 10 words. Defaulting to 'homes for sale'.")
        kw = "homes for sale"
    #=========================================

    #Download Google Search Interest Data (via pytrends) ---
    print(f'Fetching Google Trends data for "{kw}"...')

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
    kw_list = [kw] #search term we're working with

    try:
        pytrends.build_payload(kw_list, timeframe=f"{START_DATE} {END_DATE}", geo='US')  # set timeframe (20 years)
    except Exception as e:
        print("DATE FORMAT/RANGE ERROR: Your dates are invalid. Change the format and/or range.")
        print("Reverting to default 2004-12-31 to 2024-12-31.")
        print("Reason:", e)

        # Default fail-safe values
        START_DATE_default = "2004-12-31"
        END_DATE_default = "2024-12-31"
        pytrends.build_payload(kw_list, timeframe=f"{START_DATE_default} {END_DATE_default}", geo='US')  # set timeframe (20 years)

    #Pause again before fetch
    print(f"Please wait {time_sleep} seconds . . .")
    time.sleep(time_sleep)
    #time.sleep(20)
    df_trends = pytrends.interest_over_time()

    #Check
    if df_trends.empty:
        raise ValueError(f"No data returned from Google Trends for '{kw}'")

    #Save
    output_path = data_dir / GOOGLE_NAME
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
    print('Data Collection Complete: All successfully collected data will be saved to "data" folder.')


