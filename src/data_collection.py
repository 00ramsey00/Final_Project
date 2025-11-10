import os
os.environ["KAGGLE_CONFIG_DIR"] = r"C:\Users\rpbas\Desktop\Fall 2025 DSCI 510\Final Project\Final_Project_Ramsey_Basma\Final_Project"
import kaggle
import pandas as pd

# --- 1. Download Zillow dataset from Kaggle ---
dataset = 'zillow/zecon'
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