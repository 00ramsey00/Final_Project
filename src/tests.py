import argparse
from data_collection import (
    load_env,
    set_directories_and_keys,
    create_data_folder,
    kaggle_housing,
    FRED_mortgage,
    GTrends_Homes_Selling
)

def main():
    # -------------------- Command-Line Arguments --------------------
    parser = argparse.ArgumentParser(
        description="Run full data collection pipeline (Kaggle, FRED, Google Trends)."
    )
    parser.add_argument(
        "--sleep",
        type=int,
        default=20,#Wait time between google requests. This is here so you can speed it up if it works for you.
        #Default is 20 seconds which is what worked for me. This is used two times so 40 seconds total.
        help="Time (in seconds) to wait between Google Trends requests (default: 20)."
    )

    args = parser.parse_args()

    args.sleep = max(1, min(args.sleep, 30)) #Prevents accidentally putting too low of a sleep time or too high



    print("Running tests for Final Progress Report: Data Collection")

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

    GTrends_Homes_Selling(extract_dir,args.sleep) #By default, args.sleep is 20 seconds (40 total). Change it above.



    print("All data successfully collected and saved.")


if __name__ == "__main__":
    main()