# Title: The Relationship Between Online Housing Interest, Mortgage Rates, and Home Prices

This project explores whether housing demand (via google searches) moves with mortgage rates and prices. By analyzing median home prices, 30-year mortgage rates, and Google search interest (for the past 10 to 20 years), the study aims to uncover how public interest and mortgage rates together predict housing market trends. Using a multi-variable regression model, the project will assess correlations between search intent and borrowing conditions, providing insights into how early indicators like Google Trends might anticipate changes in housing affordability and market activity.

---

## Data sources

### 1 | Median Home Prices
- **Source:** Kaggle housing datasets  
- **URL:** https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset  
- **Type:** API  
- **Fields:**  
  • Date  
  • Region  
  • Median Home Price  
  • (TBD) Home Value Index (ZHVI), Sales Volume (if another dataset is used)  
- **Format:** CSV  
- **Accessed via Python:** Yes  
- **Estimated Data Size:** >300 (will very likely be much higher, TBD after cleaning up data)

---

### 2 | 30-Year Fixed Mortgage Rates
- **Source:** Federal Reserve Economic Data (FRED API)  
- **URL:** https://fred.stlouisfed.org/docs/api/fred/series_observations.html#Description 
- **Type:** API  
- **Fields:**  
  • Date  
  • Mortgage Rate (%)  
- **Format:** JSON → converted to CSV  
- **Accessed via Python:** Yes  
- **Estimated Data Size:** >300 (will very likely be much higher, TBD after cleaning up data)

---

### 3 | Google Search Interest (“homes for sale”)
- **Source:** Google Trends (via PyTrends)  
- **URL:** https://trends.google.com/  
- **Type:** API  
- **Fields:**  
  • Date  
  • Search Interest Index (0–100)  
- **Format:** JSON  
- **Accessed via Python:** Yes  
- **Estimated Data Size:** >300 (will very likely be much higher, TBD after cleaning up data)

---

## Results
TBD

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
numpy            # Provides numerical operations and array handling (used indirectly through pandas)
pandas           # Used for loading, manipulating, and saving datasets as CSV files
requests         # Handles HTTP requests to external APIs (used for FRED API data)
kaggle           # Connects to the Kaggle API to download datasets programmatically
python-dotenv    # Loads environment variables (e.g., API keys) from a .env file
pytrends         # Provides access to Google Trends data via Python
```

### Built-in Python Modules

```
time             # Controls pauses/sleep between API calls to avoid request limits
os               # Handles file paths, folders, and environment settings
json             # Parses and converts data between JSON and Python dictionaries
```

---

## Running analysis

### Option 1: Directly from `tests.py` file
From `src/` directory, open and run `tests.py`  
Data will appear in `data/` folder.

---

### Option 2: Command Terminal
From `src/` directory, run:

```
python tests.py
```

Data will appear in `data/` folder.

Optional: To adjust the sleep time between google requests for the Pytrends Homes for Sales function, input:

```
python tests.py --sleep 10
```

Min time 1 second, max 30 seconds  
Note: This can also be adjusted in the `tests.py` file
