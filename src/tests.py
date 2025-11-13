from data_collection import (
    load_env,
    set_directories_and_keys,
    create_data_folder,
    kaggle_housing,
    FRED_mortgage,
    GTrends_Homes_Selling
)

if __name__ == "__main__":
    print("Running tests for HW11: Data Collection")

    # -------------------- Setup --------------------
    #print("Loading environment variables and directories...")
    load_env()
    set_directories_and_keys()
    extract_dir = create_data_folder()
    # -------------------- Task 1 --------------------
    #print("Task 1: Kaggle Housing Data")
    kaggle_housing(extract_dir)

    # -------------------- Task 2 --------------------
    #print("Task 2: FRED Mortgage Data")
    FRED_mortgage(extract_dir)

    # -------------------- Task 3 --------------------
    #print("Task 3: Google Trends Data")

    time_sleep = 20 #Wait time between google requests. This is here so you can speed it up if it works for you.
    #Default is 20 seconds which is what worked for me. This is used two times so 40 seconds total.

    GTrends_Homes_Selling(extract_dir,time_sleep)



    print("All data successfully collected and saved.")