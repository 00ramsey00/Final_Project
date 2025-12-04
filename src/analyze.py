#This code will analyze the cleaned data generated from process.py
#Results will be saved as CSV files in "results/" folder in the parent directory

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from config import (
    RESULTS_DIR, PROCESSED_DIR,
    MERGED_CLEAN,
    TIME_SERIES_NAME, SMOOTH_SERIES_NAME,
    GOOGLE_FRED_NAME, GOOGLE_KAGGLE_NAME,
    HEATMAP_NAME, PAIRPLOT_NAME,
)

def clear_results_folder(results_dir=RESULTS_DIR):
    # ----- CLEAN RESULTS FOLDER BEFORE STARTING -----
    for f in os.listdir(results_dir):
        if f.endswith(".png"):
            os.remove(results_dir / f)
    #print("Cleaned old CSV files from data/processed directory.")

def save_plot(filename, results_dir = RESULTS_DIR): #Saves the current matplotlib figure to the results folder as a png file
    out_path = results_dir / filename
    plt.savefig(out_path)
    #print(f"Saved: {full_path}")


def load_merged_data(processed_dir = PROCESSED_DIR, merged_dir = MERGED_CLEAN ): #Loads the merged.csv dataset for use in making the graphs
    merged_path = processed_dir / merged_dir
    df = pd.read_csv(merged_path)

    # Convert month column back into datetime so Python can work with it
    df["month"] = pd.to_datetime(df["month"])

    return df


# -----------------------------------------------------------
# Line Plot - All variables over time
# -----------------------------------------------------------
def plot_time_series(df, results_dir = RESULTS_DIR): #Basic graph of Housing Prices VS Mortgage Rates VS Google Search Score
    # Make the base plot
    fig, ax1 = plt.subplots(figsize=(12,6))

    # First axis (home prices)
    ax1.plot(df["month"], df["avg_price"] / 1000, color="blue", label="Avg Home Price")
    ax1.set_ylabel("Avg Home Price (K$)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # Add gridlines on the main axis
    ax1.grid(True)


    # Second axis (mortgage rate)
    ax2 = ax1.twinx()
    ax2.plot(df["month"], df["mortgage_rate"], color="red", label="Mortgage Rate")
    ax2.set_ylabel("Mortgage Rate (%)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")


    # Third axis (search interest)
    ax3 = ax1.twinx()
    ax3.spines.right.set_position(("axes", 1.06))
    ax3.plot(df["month"], df["search_interest"], color="green", label="Search Interest")
    ax3.set_ylabel("Search Interest", color="green")
    ax3.tick_params(axis="y", labelcolor="green")

    # Make x-axis show only years instead of every month
    ax1.set_xticks(df["month"][df["month"].dt.month == 1])
    ax1.set_xticklabels(df["month"][df["month"].dt.month == 1].dt.strftime("%Y"))

    # Combined legend
    line1 = ax1.get_lines()[0]
    line2 = ax2.get_lines()[0]
    line3 = ax3.get_lines()[0]

    plt.legend([line1, line2, line3],
               ["Avg Home Price", "Mortgage Rate", "Search Interest"],
               loc="upper left")

    # Title and layout
    plt.title("Housing Market Trends (2004–2024)")
    plt.tight_layout()

    # Save and show
    save_plot(TIME_SERIES_NAME,results_dir)
    #plt.show()


# -----------------------------------------------------------
# Line Plot - All variables over time smoothed (Moving Average)
# -----------------------------------------------------------
def plot_time_series_smoothed(df, results_dir = RESULTS_DIR): #Same as above but 6 month moving average to smooth out zig zags

    # Make a copy so we don't modify the original df
    smooth = df.copy()

    # 6-month moving averages
    rolling_window = 6
    smooth["avg_price_smooth"] = smooth["avg_price"].rolling(rolling_window).mean()
    smooth["mortgage_smooth"] = smooth["mortgage_rate"].rolling(rolling_window).mean()
    smooth["search_smooth"] = smooth["search_interest"].rolling(rolling_window).mean()

    # Drop first 5 rows (they are NaN due to rolling window)
    smooth = smooth.dropna()

    # Create figure + first axis
    fig, ax1 = plt.subplots(figsize=(12,6))


    # First axis (home prices)
    ax1.plot(smooth["month"], smooth["avg_price_smooth"] / 1000,
             color="blue", linewidth=2, label="Avg Home Price (Smoothed)")
    ax1.set_ylabel("Avg Home Price (K$)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(True)


    # Second axis (mortgage rate)
    ax2 = ax1.twinx()
    ax2.plot(smooth["month"], smooth["mortgage_smooth"],
             color="red", linewidth=2, label="Mortgage Rate (Smoothed)")
    ax2.set_ylabel("Mortgage Rate (%)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")


    # Third axis (search interest)
    ax3 = ax1.twinx()
    ax3.spines.right.set_position(("axes", 1.06))
    ax3.plot(smooth["month"], smooth["search_smooth"],
             color="green", linewidth=2, label="Search Interest (Smoothed)")
    ax3.set_ylabel("Search Interest", color="green")
    ax3.tick_params(axis="y", labelcolor="green")

    # Make x-axis show only years instead of every month
    ax1.set_xticks(df["month"][df["month"].dt.month == 1])
    ax1.set_xticklabels(df["month"][df["month"].dt.month == 1].dt.strftime("%Y"))


    # Legend
    lines = (
        ax1.get_lines() +
        ax2.get_lines() +
        ax3.get_lines()
    )
    labels = [l.get_label() for l in lines]

    plt.legend(lines, labels, loc="upper left")

    plt.title("Smoothed Housing Market Trends (6-Month Moving Average)")
    plt.tight_layout()

    # Save to results folder
    save_plot(SMOOTH_SERIES_NAME,results_dir)
    #plt.show()



# -----------------------------------------------------------
# Scatter: Search Interest vs Mortgage Rate
# -----------------------------------------------------------
def plot_scatter_search_vs_mortgage(df, results_dir = RESULTS_DIR):
    plt.figure(figsize=(8,6))

    # Scatter with search on X
    plt.scatter(df["search_interest"], df["mortgage_rate"], alpha=0.5, label="Data Points")

    # Regression line
    sns.regplot(
        x=df["search_interest"],
        y=df["mortgage_rate"],
        scatter=False,
        color="red",
        label="Trend Line"
    )

    plt.title("Search Interest vs Mortgage Rate")
    plt.xlabel("Search Interest")
    plt.ylabel("Mortgage Rate (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    save_plot(GOOGLE_FRED_NAME,results_dir)
    #plt.show()



# -----------------------------------------------------------
# Scatter: Search Interest vs Average Price
# -----------------------------------------------------------
def plot_scatter_search_vs_price(df, results_dir = RESULTS_DIR):
    plt.figure(figsize=(8,6))

    plt.scatter(df["search_interest"], df["avg_price"], alpha=0.5, label="Data Points")

    sns.regplot(
        x=df["search_interest"],
        y=df["avg_price"],
        scatter=False,
        color="red",
        label="Trend Line"
    )

    plt.title("Search Interest vs Average Price")
    plt.xlabel("Search Interest")
    plt.ylabel("Average Home Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    save_plot(GOOGLE_KAGGLE_NAME,results_dir)
    #plt.show()




# -----------------------------------------------------------
# Correlation Heatmap
# -----------------------------------------------------------
def plot_correlation_heatmap(df, results_dir = RESULTS_DIR):
    corr = df[["avg_price", "mortgage_rate", "search_interest"]].corr()

    plt.figure(figsize=(6,4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")

    plt.title("Correlation Heatmap")
    plt.tight_layout()

    save_plot(HEATMAP_NAME,results_dir)
    #plt.show()

    #print("\nCorrelation Matrix:")
    #print(corr)


# -----------------------------------------------------------
# Pair Plot
# -----------------------------------------------------------
def plot_pairplot(df, results_dir = RESULTS_DIR):
    # Keep ONLY the 3 core variables
    plot_df = df[["avg_price", "mortgage_rate", "search_interest"]]

    # Create the pair plot
    sns.pairplot(
        plot_df,
        diag_kind="hist",      # histograms on diagonal
        kind="reg",            # regression line in scatter plots
        plot_kws={
            "line_kws": {"color": "red"},
            "scatter_kws": {"alpha": 0.5}
        }
    )
    plt.suptitle("Pair Plot: Avg Price, Mortgage Rate, Search Interest", y=1.02)
    save_plot(PAIRPLOT_NAME,results_dir)

    #plt.show()






if __name__ == "__main__":
    print("----------------------Running Data Analysis----------------------")
    clear_results_folder()
    # Load merged data
    try:
        df = load_merged_data()

    #print("\nLoaded merged dataset:")
    #print(df.head())

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


