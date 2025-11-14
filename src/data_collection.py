#This code will pull data from 3 locations:
#Kaggle Housing Prices, Federal Reserve 30-Year Fixed Mortgage Rates, and Google Trends-Homes for sale
#Data will be saved as CSV files in "data" folder in the parent directory

import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv
from pytrends.request import TrendReq

#kaggle is also imported below but needs to be below path normalization

def load_env():
    # Load environment variables from .env file
    load_dotenv()  # By default it loads from a file named .env in the same folder
    # this is used to protect API keys and to avoid having them directly in this code for security purposes

def set_directories_and_keys():
    #----------------------API INFORMATION---------------------------
    global kaggle_config_dir, FRED_API_KEY  # Needed so other functions can access

    # Set Kaggle config directory from the .env file instead of using the default location
    kaggle_config_dir = os.getenv("KAGGLE_CONFIG_DIR")
    if not kaggle_config_dir:
        raise ValueError("KAGGLE_CONFIG_DIR is not set in the .env file")

    # Set FRED API from the .env file
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    if not FRED_API_KEY:
        raise ValueError("FRED_API_KEY is not set in the .env file")

    #Google API not needed
    return kaggle_config_dir, FRED_API_KEY
    #-----------------------------------------------------------------


def create_data_folder():
    #------------Set up "data" folder location in parent folder------------------
    # Get the parent directory of the current script
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create the 'data' folder if it doesn’t exist
    extract_dir = os.path.join(project_root, "data")
    os.makedirs(extract_dir, exist_ok=True)

    return extract_dir
    #-----------------------------------------------------------------



def kaggle_housing(extract_dir):
    #----------------------KAGGLE - Housing Prices Data Collection---------------------------
    os.environ["KAGGLE_CONFIG_DIR"] = kaggle_config_dir  #Location of Kaggle API Key found from .env file
    #print("Using Kaggle config dir:", kaggle_config_dir)

    import kaggle #This needs to be here after environment variable is set


    #Download Zillow dataset from Kaggle
    dataset = 'ahmedshahriarsakib/usa-real-estate-dataset'

    print("Fetching Housing Price data from Kaggle...")
    kaggle.api.dataset_download_files(dataset, path=extract_dir, unzip=True)

    #Find and load CSV file from the zip folder and put it into data folder
    #From this Kaggle dataset, there's only one CSV file so no need to tweak this code. It's good enough
    csv_file = [f for f in os.listdir(extract_dir) if f.endswith('.csv')][0]
    csv_path = os.path.join(extract_dir, csv_file)

    df = pd.read_csv(csv_path)
    #print("Data loaded:", df.shape)
    #print(df.columns)
    #-----------------------------------------------------------------------------------------------


def FRED_mortgage(extract_dir):
    #----------------------FRED - 30-Year Fixed Mortgage Rates---------------------------
    FRED_SERIES_ID = "MORTGAGE30US"
    FRED_API_URL = f"https://api.stlouisfed.org/fred/series/observations"

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
    output_path = os.path.join(extract_dir, "mortgage_rates.csv")
    df.to_csv(output_path, index=False)

    #print(f"Mortgage rate data saved to: {output_path}")
    #-----------------------------------------------------------------------------------------------




def GTrends_Homes_Selling(extract_dir, time_sleep: int):
    #------------------------------Google Trends - "Homes for sale"------------------------------

    #Download Google Search Interest Data (via pytrends) ---
    print("Fetching Google Trends data for 'homes for sale'...")

    #Create a clean Trends session with explicit connection headers to avoid being banned as a bot
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
    time.sleep(time_sleep)
    #time.sleep(20)

    #Pick data we want
    kw_list = ["homes for sale"]
    pytrends.build_payload(kw_list, timeframe='2014-01-01 2024-12-31', geo='US')

    #Pause again before fetch
    time.sleep(time_sleep)
    #time.sleep(20)
    df_trends = pytrends.interest_over_time()

    #Check
    if df_trends.empty:
        raise ValueError("No data returned from Google Trends for 'homes for sale'")

    #Save
    output_path = os.path.join(extract_dir, "google_trends_homes_for_sale.csv")
    df_trends.to_csv(output_path)
    #print(f"Google Trends data saved to: {output_path}")
    #print("Data loaded:", df_trends.shape)
    #print(df_trends.head())
    #-----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    load_env()
    set_directories_and_keys()
    extract_dir = create_data_folder()
    kaggle_housing(extract_dir)
    FRED_mortgage(extract_dir)

    time_sleep = 20 #Wait time between google requests. This is here so you can speed it up if it works for you.
    #Default is 20 seconds which is what worked for me. This is used two times so 40 seconds total.
    GTrends_Homes_Selling(extract_dir, time_sleep)

    print("All data successfully collected and saved.")