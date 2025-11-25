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
from config import (
    KAGGLE_NAME,
    FRED_NAME,
    GOOGLE_NAME,
    time_sleep,
)

def run_load(local_time_sleep):
    print("----------------------Running Data Collection----------------------")
    clear_data_folder()
    kaggle_housing()
    FRED_mortgage()
    GTrends_Homes_Selling(local_time_sleep)

    print('All data successfully collected and saved to "data" folder.')


def run_data_processing():
    print("----------------------Running Data Cleaning/Processing----------------------")
    clear_processed_folder()
    process_realtor_data(KAGGLE_NAME)
    process_mortgage_data(FRED_NAME)
    process_google_data(GOOGLE_NAME)
    process_merge_data()

    print("All data successfully cleaned and saved to data/processed folder.")


def run_analysis():
    print("----------------------Running Data Analysis----------------------")
    clear_results_folder()
    df = load_merged_data()

    #print("Loaded merged dataset:")
    ####print(df.head())

    plot_time_series(df)
    plot_time_series_smoothed(df)
    plot_scatter_search_vs_mortgage(df)
    plot_scatter_search_vs_price(df)
    plot_correlation_heatmap(df)
    plot_pairplot(df)

    print('All graphs generated and saved to the "results" folder.')


def main():
    # -------------------- Command-Line Arguments --------------------


    parser = argparse.ArgumentParser(
        description="Run data collection, processing, and analysis."
    )

    parser.add_argument("--load", action="store_true",
                        help="Run load.py data collection pipeline")
    parser.add_argument("--process", action="store_true",
                        help="Run process.py cleaning + merging")
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