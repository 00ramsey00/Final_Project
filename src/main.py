import argparse

# Import data collection
from load import (
    clear_data_folder,
    kaggle_housing,
    FRED_mortgage,
    GTrends_Homes_Selling
)

# Import processing
from process import (
    process_realtor_data,
    process_mortgage_data,
    process_google_data,
    process_merge_data,
    clear_processed_folder,
)

# Import analysis
from analyze import (
    load_merged_data,
    plot_time_series,
    plot_time_series_smoothed,
    plot_scatter_search_vs_mortgage,
    plot_scatter_search_vs_price,
    plot_correlation_heatmap,
    plot_pairplot,
    clear_results_folder,
)

# Import cleaned filenames from config.py
from config import time_sleep

def run_load(local_time_sleep):
    print("----------------------Running Data Collection----------------------")
    clear_data_folder()
    kaggle_housing()
    FRED_mortgage()
    GTrends_Homes_Selling(local_time_sleep)

    print('Data Collection Complete: All successfully collected data will be saved to "data/" folder.')


def run_data_processing():
    print("----------------------Running Data Cleaning/Processing----------------------")
    clear_processed_folder()

    try:
        process_realtor_data()
    except Exception as e:
        print("KAGGLE PROCESSING ERROR: Reason:", e)
    
    try:
        process_mortgage_data()
    except Exception as e:
        print("FRED PROCESSING ERROR: Reason:", e)

    try:
        process_google_data()
    except Exception as e:
        print("FRED PROCESSING ERROR: Reason:", e)

    try:
        process_merge_data()
    except Exception as e:
        print("MERGING ERROR: Reason:", e)

    print('Data Cleaning/Processing Complete: All successfully processed data will be saved to "data/processed/" folder.')

def run_analysis():
    print("----------------------Running Data Analysis----------------------")
    clear_results_folder()
    try:
        df = load_merged_data()

    # Generate and save all plots
        plot_time_series(df)
        plot_time_series_smoothed(df)
        plot_scatter_search_vs_mortgage(df)
        plot_scatter_search_vs_price(df)
        plot_correlation_heatmap(df)
        plot_pairplot(df)
    except Exception as e:
        print("ANALYSIS RESULTS GENERATION ERROR: Reason:", e)

    print('Data Analysis Complete: All successfully generated graphs will be saved to "results/" folder.')

def main():
    # -------------------- Command-Line Arguments --------------------


    parser = argparse.ArgumentParser(
        description="Run data collection, processing, and analysis."
    )

    parser.add_argument("--load", action="store_true",
                        help="Run load.py data collection")
    parser.add_argument("--process", action="store_true",
                        help="Run process.py cleaning and merging")
    parser.add_argument("--analyze", action="store_true",
                        help="Run analyze.py and generate graphs")
    parser.add_argument("--all", action="store_true",
                        help="Run all steps: load data then process then analyze")

    parser.add_argument("--sleep", type=int, default=time_sleep,
                        help="Override sleep time for Google Trends (default 20 seconds set by config.py)")

    args = parser.parse_args()

    local_time_sleep = max(1, min(args.sleep, 50)) # Prevents accidentally putting too low of a sleep time or too high

    # DEFAULT BEHAVIOR = run everything if no flags used
    if not (args.load or args.process or args.analyze or args.all):
        #print("\nNo flags provided,  running FULL PIPELINE.\n")
        run_load(local_time_sleep)
        run_data_processing()
        run_analysis()
        return

    # If flags *were* used:
    # If --all is selected
    if args.all:
        run_load(local_time_sleep)
        run_data_processing()
        run_analysis()
        return

    # Otherwise, run selected features
    if args.load:
        run_load(local_time_sleep)

    if args.process:
        run_data_processing()

    if args.analyze:
        run_analysis()



if __name__ == "__main__":
    main()