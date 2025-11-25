import os
from pathlib import Path
from dotenv import load_dotenv


# ---------------------------------------------------
# Load environment variables from .env
# ---------------------------------------------------
load_dotenv() # By default it loads from a file named .env in the same folder

# ---------------------------------------------------
# Project folder paths
# ---------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

# Ensure folders exist
DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# API KEYS from .env
# ---------------------------------------------------
KAGGLE_CONFIG_DIR = os.getenv("KAGGLE_CONFIG_DIR")
FRED_API_KEY = os.getenv("FRED_API_KEY")

# ---------------------------------------------------
# Data Sources Configuration
# ---------------------------------------------------
KAGGLE_DATASET = 'ahmedshahriarsakib/usa-real-estate-dataset'
FRED_SERIES_ID = "MORTGAGE30US"
FRED_API_URL = f"https://api.stlouisfed.org/fred/series/observations"

# ---------------------------------------------------
# Data File Names
# ---------------------------------------------------
#Downloaded CSV Files
KAGGLE_NAME = "realtor-data.zip.csv"
FRED_NAME = "mortgage_rates.csv"
GOOGLE_NAME = "google_trends_homes_for_sale.csv"

#Processed/Clean CSV Files
KAGGLE_NAME_CLEAN = "realtor_clean.csv"
FRED_NAME_CLEAN = "mortgage_clean.csv"
GOOGLE_NAME_CLEAN = "google_clean.csv"
MERGED_CLEAN = "merged_clean.csv"

#Plots
TIME_SERIES_NAME = "time_series.png"
SMOOTH_SERIES_NAME = "time_series_smoothed.png"
GOOGLE_FRED_NAME = "search_vs_mortgage.png"
GOOGLE_KAGGLE_NAME = "search_vs_price.png"
HEATMAP_NAME = "correlation_heatmap.png"
PAIRPLOT_NAME = "pairplot.png"


# ---------------------------------------------------
# Other project constants
# ---------------------------------------------------
START_DATE = "2004-12-31"
END_DATE   = "2024-12-31"
time_sleep = 20 #Wait time between google requests. This is here so you can speed it up if it works for you.
    #Default is 20 seconds which is what worked for me. This is used two times so 40 seconds total.
