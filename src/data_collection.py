import os
import pandas as pd
from dotenv import load_dotenv
#os.environ["KAGGLE_CONFIG_DIR"] = r"C:\Users\rpbas\Desktop\Fall 2025 DSCI 510\Final Project\Final_Project_Ramsey_Basma\Final_Project\src"

# Load environment variables from .env file
load_dotenv()  # By default it loads from a file named .env in the same folder

# Set Kaggle config directory from the .env file
kaggle_config_dir = os.getenv("KAGGLE_CONFIG_DIR")
if not kaggle_config_dir:
    raise ValueError("KAGGLE_CONFIG_DIR is not set in the .env file")

# Normalize path for Windows/Mac/Linux
kaggle_config_dir = os.path.normpath(kaggle_config_dir)
os.environ["KAGGLE_CONFIG_DIR"] = kaggle_config_dir

print("Using Kaggle config dir:", kaggle_config_dir)

import kaggle


# --- 1. Download Zillow dataset from Kaggle ---
dataset = 'ahmedshahriarsakib/usa-real-estate-dataset'
extract_dir = 'zillow_data'
os.makedirs(extract_dir, exist_ok=True)

print("Downloading Zillow data from Kaggle...")
kaggle.api.dataset_download_files(dataset, path=extract_dir, unzip=True)

# --- 2. Find and load CSV file ---
csv_file = [f for f in os.listdir(extract_dir) if f.endswith('.csv')][0]
csv_path = os.path.join(extract_dir, csv_file)

df = pd.read_csv(csv_path)
print("Data loaded:", df.shape)
print(df.columns)