import os
import pandas as pd
from dotenv import load_dotenv
#os.environ["KAGGLE_CONFIG_DIR"] = r"C:\Users\rpbas\Desktop\Fall 2025 DSCI 510\Final Project\Final_Project_Ramsey_Basma\Final_Project\src"
import requests

# Load environment variables from .env file
load_dotenv()  # By default it loads from a file named .env in the same folder

# Set Kaggle config directory from the .env file
kaggle_config_dir = os.getenv("KAGGLE_CONFIG_DIR")
if not kaggle_config_dir:
    raise ValueError("KAGGLE_CONFIG_DIR is not set in the .env file")

# Set FRED config directory from the .env file
fred_api_key = os.getenv("FRED_API_KEY")
if not fred_api_key:
    raise ValueError("FRED_API_KEY is not set in the .env file")






# Normalize path for Windows/Mac/Linux
kaggle_config_dir = os.path.normpath(kaggle_config_dir)
os.environ["KAGGLE_CONFIG_DIR"] = kaggle_config_dir
print("Using Kaggle config dir:", kaggle_config_dir)

import kaggle



# --- Find parent 'data' folder ---
# Get the parent directory of the current script
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create the 'data' folder if it doesn’t exist
extract_dir = os.path.join(project_root, "data")
os.makedirs(extract_dir, exist_ok=True)




# --- 1. Download Zillow dataset from Kaggle ---
dataset = 'ahmedshahriarsakib/usa-real-estate-dataset'
#extract_dir = 'data'
#os.makedirs(extract_dir, exist_ok=True)

print("Downloading Zillow data from Kaggle...")
kaggle.api.dataset_download_files(dataset, path=extract_dir, unzip=True)

# --- 2. Find and load CSV file ---
csv_file = [f for f in os.listdir(extract_dir) if f.endswith('.csv')][0]
csv_path = os.path.join(extract_dir, csv_file)

df = pd.read_csv(csv_path)
print("Data loaded:", df.shape)
print(df.columns)




# --- 1. Define the FRED API details ---
FRED_SERIES_ID = "MORTGAGE30US"
FRED_API_URL = f"https://api.stlouisfed.org/fred/series/observations"

params = {
    "series_id": FRED_SERIES_ID,
    "api_key": fred_api_key,
    "file_type": "json"
}

# --- 2. Request data from FRED ---
print(f"Fetching 30-Year Fixed Mortgage Rates ({FRED_SERIES_ID}) from FRED...")
response = requests.get(FRED_API_URL, params=params)
response.raise_for_status()  # Raises an error if request failed

data = response.json()
observations = data.get("observations", [])

if not observations:
    raise ValueError("No data returned from FRED API")

# --- 3. Convert to pandas DataFrame ---
df = pd.DataFrame(observations)
print(f"Data successfully loaded: {df.shape[0]} records")

# --- 4. Save raw data to CSV ---
#save_dir = "data"
#os.makedirs(save_dir, exist_ok=True)

output_path = os.path.join(extract_dir, "mortgage_rates.csv")
df.to_csv(output_path, index=False)

print(f"Mortgage rate data saved to: {output_path}")