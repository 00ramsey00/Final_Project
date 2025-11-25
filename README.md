# Title: The Relationship Between Online Housing Interest, Mortgage Rates, and Home Prices

This project explores whether housing demand (via google searches) moves with mortgage rates and prices. By analyzing median home prices, 30-year mortgage rates, and Google search interest (for the 20 years), the study aims to uncover how public interest and mortgage rates together predict housing market trends. By using time-series analysis, smoothed trend lines, correlation matrices, and regression plots of publicly available data, the project will assess correlations, providing insights into how early indicators like Google Trends might anticipate changes in housing affordability and market activity. All data collection, processing, and analyzing is completed using a fully automated Python pipeline, publicly available on GitHub.

---

## Data sources

### 1 | Median Home Prices
- **Source:** Kaggle housing datasets  
- **URL:** https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset  
- **Type:** API  
- **Fields:**  
  • Sold Date    
  • Price  
  • (10 not used)  
- **Format:** CSV  
- **Accessed via Python:** Yes  
- **Estimated Data Size:** 2,226,382

---

### 2 | 30-Year Fixed Mortgage Rates
- **Source:** Federal Reserve Economic Data (FRED API)  
- **URL:** https://fred.stlouisfed.org/docs/api/fred/series_observations.html#Description 
- **Type:** API  
- **Fields:**  
  • Weekly Date  
  • Mortgage Rate (%)  
  • (2 not used)  
- **Format:** JSON → CSV  
- **Accessed via Python:** Yes  
- **Estimated Data Size:** 2,852

---

### 3 | Google Search Interest (“homes for sale”)
- **Source:** Google Trends (via PyTrends)  
- **URL:** https://trends.google.com/  
- **Type:** API  
- **Fields:**  
  • Monthly Date  
  • Google Search Interest Index (0–100)  
  • (1 not used) 
- **Format:** Pandas DataFram → JSON  
- **Accessed via Python:** Yes  
- **Estimated Data Size:** 241

---

## Summary of Results

(See PowerPoint in `doc/` folder.)

Do early indicators such as Google Trends anticipate changes in housing affordability and market activity? 
  -No, not with this specific data set. Correlation is not strong enough.

Do rates and prices move with Google search trends?
  -Not prices but rates do. Higher the rates, lower the general public’s 	interest in purchasing a home.

Any future considerations?
  -Yes, consider additional housing price data with more precise filters, include additional Google search terms (currently limited by amount of requests), consider shorter analysis periods with major events removed.

Additional Notes:
-Though the real estate data contained over 2 million data points, it could still be skewed in terms of whether some states had more data than others or whether more data was collected in specific years than others.
-It is possible to filter housing price and google trend data by state but mortgage rate is federal and cannot be further filtered.
-Percentage and directional changes were derived but ultimately not used due to lack of experience in data analysis.

---

## Installation

In `.env.example` file, set the following and rename to `.env`:

```
KAGGLE_CONFIG_DIR= #Folder location of your kaggle.json file
FRED_API_KEY="" #Your FRED API Key
#For kaggle, do not use "" when inputting the directory
```

---

### Required Libraries

```
numpy               # Provides numerical operations and array handling (used indirectly through pandas)
pandas              # Used for loading, manipulating, and saving datasets as CSV files
requests            # Handles HTTP requests to external APIs (used for FRED API data)
kaggle              # Connects to the Kaggle API to download datasets programmatically
python-dotenv       # Loads environment variables (e.g., API keys) from a .env file
pytrends            # Provides access to Google Trends data via Python
matplotlib.pyplot   # Used to create time-series charts, line graphs, scatter plots, and formatted visualizations.
seaborn             # Used for statistical visualizations including regression lines, correlation heatmaps, and pair plots.
```

### Built-in Python Modules

```
time             # Controls pauses/sleep between API calls to avoid request limits
os               # Handles file paths, folders, and environment settings
json             # Parses and converts data between JSON and Python dictionaries
```

---

## Running Program

### Option 1: Python: Run ALL (Data Collection, Processing, and Analyzing) Directly from `tests.py` file
From `src/` directory, open and run `tests.py`  

Data will appear in `data/` folder.
Processed data will appear in `data/processed` folder.
Results will appear in `results/` folder.

---

### Option 2: Anaconda Command Terminal: Run Data Collection, Processing, and Analyzing individually

Activate your CONDA environment

From `src/` directory:

 run:

```
python tests.py --load
```

Data will appear in `data/` folder.

Optional: To adjust the sleep time between google requests for the Pytrends Homes for Sales function, input:

```
python tests.py --load --sleep 15
```

Note: Min time 1 second, max 50 seconds. The program sleeps twice during the Google Trends pull. 
Note: This can also be adjusted in the `tests.py` file



From `src/` directory:

 run:

```
python tests.py --process
```

Processed data will appear in `data/processed` folder.



From `src/` directory:

 run:

```
python tests.py --analyze
```

Results will appear in `results/` folder.

---

### Option 3: Anaconda Command Terminal: Run ALL (Data Collection, Processing, and Analyzing)

Activate your CONDA environment

From `src/` directory:

 run:

```
python tests.py --all
```  

OR

```
python tests.py
```  

Data will appear in `data/` folder.
Processed data will appear in `data/processed` folder.
Results will appear in `results/` folder.


Optionally run:

```
python tests.py --all --sleep 15
```
Similar to above

---

### Note:

You may adjust output filenames and even the analysis date range in the `config.py` file.




Thank you!