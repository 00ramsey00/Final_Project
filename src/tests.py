#Simple functional tests for load.py without modifying config.py or .env.
#Feel free to change any of the variables that have "***************" at the end of the line

import os
from pathlib import Path

from load import (
    clear_data_folder,
    kaggle_housing,
    FRED_mortgage,
    GTrends_Homes_Selling
)

from process import (
    clear_processed_folder,
    process_realtor_data,
    process_mortgage_data,
    process_google_data,
    process_merge_data,
)

from analyze import (
    clear_results_folder,
    load_merged_data,
    plot_time_series,
    plot_time_series_smoothed,
    plot_scatter_search_vs_mortgage,
    plot_scatter_search_vs_price,
    plot_correlation_heatmap,
    plot_pairplot,
)
# ============================================================
# TEST CONFIG (HARD-CODED)
# ============================================================

# A sandbox folder where test files will be created.
# IMPORTANT: This will be created in the SRC directory
# IMPORTANT: Gitignore will ignore test_data/ specifically but needs to be updated if you change the test_data folder name below

TEST_DATA_DIR = Path("test_data") #Feel free to change this but read the notes above ***************
TEST_DATA_DIR.mkdir(exist_ok=True)

# Subfolders
TEST_LOADED_DIR = TEST_DATA_DIR / "test_loaded" #Feel free to change this ***************
TEST_PROCESSED_DIR = TEST_DATA_DIR / "test_processed" #Feel free to change this ***************
TEST_RESULTS_DIR = TEST_DATA_DIR / "test_results" #Feel free to change this ***************

# Create the folders
TEST_LOADED_DIR.mkdir(exist_ok=True)
TEST_PROCESSED_DIR.mkdir(exist_ok=True)
TEST_RESULTS_DIR.mkdir(exist_ok=True)

#Test CSV File Names
KAGGLE_NAME= "KAGGLE_TEST.csv"#Feel free to change this ***************
FRED_NAME="FRED_TEST.csv" #Feel free to change this ***************
GOOGLE_NAME="GOOGLE_TEST.csv" #Feel free to change this ***************

#Test Kaggle Dataset
TEST_KAGGLE_DATASET = "username/nonexistent_dataset" #Feel free to change this ***************
#This project normally uses (and is specifically coded to use): "ahmedshahriarsakib/usa-real-estate-dataset" https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset
#For example, you can try "yasserh/housing-prices-dataset" https://www.kaggle.com/datasets/yasserh/housing-prices-dataset

#Test Kaggle Config for the kaggle.json file which contains the username and key
KAGGLE_CONFIG_DIR = r"C:\Users\Your\Directory\Here" #Feel free to change this ***************

#Test FRED (Federal Reserve Economic Data) API key
TEST_FRED_API_KEY = "FAKE_KEY_12345" #Feel free to change this ***************

#Test FRED Series
TEST_FRED_SERIES = "FAKE_SERIES" #Feel free to change this ***************
#This project normally uses: "MORTGAGE30US"
#For example, "UNRATE" for unemployment rate or "GDP" for Real Gross Domestic Product
#More can be found at https://fred.stlouisfed.org/
#On that website, once you select the data, Series ID will be found to the right of the name. For ex: 30-Year Fixed Rate Mortgage Average in the United States (MORTGAGE30US)

# Test Google Trends search term
TEST_GOOGLE_SEARCH = "news" #Feel free to change this ***************
#This project normally uses: "homes for sale"


# Test sleep for testing
TEST_SLEEP = 10 #Feel free to change this ***************
'''This project normally uses 20 seconds. This is the sleep time between Google pulls since it blocks us
if requests are made too quickly within each other. The wait time is used twice in the code so 20 seconds
would be 40 seconds total'''

START_DATE = "2004-12-31" #Feel free to change this ***************
END_DATE   = "2024-12-31" #Feel free to change this ***************
#This project normally uses 2004-12-31 to 2024-12-31 (20 years)

# ============================================================
# INDIVIDUAL TEST FUNCTIONS
# ============================================================

def test_kaggle():
    print("===============TEST: Kaggle Pull===============")
    kaggle_housing(data_dir=TEST_LOADED_DIR,dataset=TEST_KAGGLE_DATASET,kaggle_config_dir=KAGGLE_CONFIG_DIR, KAGGLE_NAME=KAGGLE_NAME)
    print("===============================================\n")

def test_fred():
    print("===============TEST: FRED Pull=================")
    FRED_mortgage(api_key=TEST_FRED_API_KEY, series_id=TEST_FRED_SERIES, data_dir=TEST_LOADED_DIR, FRED_NAME=FRED_NAME)
    print("===============================================\n")

def test_google():
    print("===============TEST: Google Trends Pull========")
    GTrends_Homes_Selling(time_sleep=TEST_SLEEP,kw=TEST_GOOGLE_SEARCH,data_dir=TEST_LOADED_DIR, GOOGLE_NAME=GOOGLE_NAME, START_DATE = START_DATE, END_DATE = END_DATE)
    print("===============================================\n")



def test_kaggle_processing():
    print("===============TEST: Kaggle Data Processing========")
    try:
        process_realtor_data(filename=KAGGLE_NAME,data_dir=TEST_LOADED_DIR,processed_dir=TEST_PROCESSED_DIR,kaggle_name_clean="KAGGLE_CLEAN.csv",START_DATE = START_DATE, END_DATE = END_DATE)
    except Exception as e:
        print("Error: Reason:", e)
        print('Note: This program is specifically coded to use the wording and formatting of the data in "ahmedshahriarsakib/usa-real-estate-dataset"')
    print("===============================================\n")

def test_FRED_processing():
    print("===============TEST: FRED Data Processing========")
    try:
        process_mortgage_data(filename=FRED_NAME,data_dir=TEST_LOADED_DIR,processed_dir=TEST_PROCESSED_DIR,fred_name_clean="FRED_CLEAN.csv",START_DATE = START_DATE, END_DATE = END_DATE)
    except Exception as e:
        print("Error: Reason:", e)
        print('Note: This program is specifically coded to use the wording and formatting of the data in series ID: "MORTGAGE30US"')
    print("===============================================\n")

def test_GOOGLE_processing():
    print("===============TEST: GOOGLE Data Processing========")
    try:
        process_google_data(filename=GOOGLE_NAME,data_dir=TEST_LOADED_DIR,processed_dir=TEST_PROCESSED_DIR,google_name_clean="GOOGLE_CLEAN.csv",google_search_term=TEST_GOOGLE_SEARCH,START_DATE = START_DATE, END_DATE = END_DATE)
    except Exception as e:
        print("Error: Reason:", e)
        print('Note: This program is specifically coded to use the wording and formatting of the data in series ID: "MORTGAGE30US"')
    print("===============================================\n")

def test_merge_data():
    print("===============TEST: Merging Data========")
    try:
        process_merge_data(
            processed_dir = TEST_PROCESSED_DIR,
            kaggle_name_clean="KAGGLE_CLEAN.csv",
            google_name_clean="GOOGLE_CLEAN.csv",
            fred_name_clean="FRED_CLEAN.csv",
            merged_dir="MERGED_CLEAN.csv",
            google_search_term=TEST_GOOGLE_SEARCH,
        )
    except Exception as e:
        print("Error: Reason:", e)
        print('Note: This program is specifically coded to use the wording and formatting of the 3 original data sets, not different test data sets.')
    print("===============================================\n")



def test_analyze():
    print("===============TEST: Full Analysis=======")
    try:
        df = load_merged_data(processed_dir=TEST_PROCESSED_DIR, merged_dir="MERGED_CLEAN.csv")

        # Individual plots
        plot_time_series(df, results_dir=TEST_RESULTS_DIR)
        plot_time_series_smoothed(df, results_dir=TEST_RESULTS_DIR)
        plot_scatter_search_vs_mortgage(df, results_dir=TEST_RESULTS_DIR)
        plot_scatter_search_vs_price(df, results_dir=TEST_RESULTS_DIR)
        plot_correlation_heatmap(df, results_dir=TEST_RESULTS_DIR)
        plot_pairplot(df, results_dir=TEST_RESULTS_DIR)

        print("Analysis test complete.")
    except Exception as e:
        print("Error: Reason:", e)
        print('Note: This program is specifically coded to graph with the data from the 3 original data sets, not different test data sets.')
    print("===============================================\n")


# ============================================================
# RUN ALL TESTS
# ============================================================

def run_all_tests():
    print("========================================")
    print(" RUNNING ALL LOAD.PY TESTS")
    print("========================================\n")
    clear_data_folder(TEST_LOADED_DIR) #put this inside each one same with processed and results
    test_kaggle()
    test_fred()
    test_google()


    print("========================================")
    print(" RUNNING ALL PROCESS.PY TESTS")
    print("========================================\n")
    clear_processed_folder(TEST_PROCESSED_DIR)
    test_kaggle_processing()
    test_FRED_processing()
    test_GOOGLE_processing()
    test_merge_data()


    print("========================================")
    print(" RUNNING ALL ANALYZE.PY TESTS")
    print("========================================\n")
    clear_results_folder(TEST_RESULTS_DIR)
    test_analyze()


    print("All tests completed.")


if __name__ == "__main__":
    run_all_tests()
