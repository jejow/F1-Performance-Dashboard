# F1 Performance Dashboard

A Streamlit-based interactive dashboard to analyze Formula 1 performance by driver, car/engine, and circuit, plus race vs sprint comparisons (2023–2025). It visualizes key telemetry-style metrics such as speed, RPM, throttle, brake, and gear usage patterns.

Important: The dataset is not bundled with this repository. The app reads CSV files from a local folder named `f1_cleaned_data/` that you provide.

## Before You Run (Get the Data First)

You must have data available under `f1_cleaned_data/` before launching the app. Choose ONE of the following:

Option A — Download ready-to-use dataset:

- Google Drive link: https://drive.google.com/drive/folders/195xYOXAbZBYR-XWG4yqnA7Wl-vTjTbe3?usp=sharing
- After download, extract/place the `f1_cleaned_data/` folder at the project root (same level as `main.py`).

Option B — Scrape/build the data yourself:

- Open the notebook at `data_scraping/Collab/Data_scraping.ipynb` and follow the steps to collect and export CSVs.
- Save your outputs into the folder structure shown below (`f1_cleaned_data/<YEAR>/<race|sprint>/*.csv`).

## Supported Data Layout

Place your CSVs like this (rooted at the project directory):

```
f1_cleaned_data/
  └─ <YEAR>/
      ├─ race/
      │   ├─ <any_name_1>.csv
      │   └─ <any_name_2>.csv
      └─ sprint/
          ├─ <any_name_3>.csv
          └─ <any_name_4>.csv
```

Recommended columns (the app adapts if some are missing):

- Common: `driver_name`, `speed`, `rpm`, `throttle`, `brake`, `n_gear`
- Helpful for extra analytics: `race` (circuit name), `lap`, `date`

Example CSV row (short header):

```
driver_name,speed,rpm,throttle,brake,n_gear,race,lap,date
Max Verstappen,312.4,11800,78.2,0.0,8,Monza,12,2024-09-01T13:24:51Z
```

If a column is missing, related charts will be hidden automatically.

## Features

- Overview with global performance metrics and filters (year, session type, driver).
- Driver analysis: speed vs RPM, throttle vs brake, gear distribution, lap/time speed trends.
- Car/engine analysis: RPM vs speed efficiency, gear shift patterns and distribution, top speed.
- Circuit analysis: speed distribution, gear patterns, RPM vs throttle, circuit characteristics.
- Cross-year comparison (2023–2025): race vs sprint average/max speed, RPM trends.
- Performance helpers: data caching, sampling to keep the browser smooth, sidebar performance metrics.

## Project Structure

```
F1 Performance Dashboard/
├─ main.py                    # Main overview page
├─ pages/                     # Streamlit multipage screens
│  ├─ 1_Driver_Performance.py
│  ├─ 2_Car_Performance.py
│  ├─ 3_Race_Comparison.py
│  └─ 4_Circuit_Analysis.py
├─ utils.py                   # Data loaders, chart helpers
├─ performance_monitor.py     # Sidebar performance metrics
├─ assets/                    # Screenshots for README/UI
├─ data_scraping/             # Scraping notebook (optional)
├─ requirements.txt           # Python dependencies
└─ f1_cleaned_data/           # (You provide) per-year/session CSVs
```

## Prerequisites

- Python 3.9+
- OS: Windows (commands below use Command Prompt / cmd.exe)

## Installation (Windows cmd)

1) Create and activate a virtual environment:

```bat
python -m venv .venv
.venv\Scripts\activate
```

If `python` is not recognized, try:

```bat
py -m venv .venv
.venv\Scripts\activate
```

2) Install dependencies:

```bat
pip install -r requirements.txt
```

3) Ensure data exists under `f1_cleaned_data/` (see "Before You Run").

## Run the App

From the project root, start Streamlit:

```bat
streamlit run main.py
```

Streamlit will open your browser to a local URL (usually http://localhost:8501).

## Screenshots

- Overview: ![Overview](assets/1.png)
- Driver Analysis: ![Driver](assets/2.png)
- Circuit Analysis: ![Circuit](assets/3.png)

## How It Works (Quick)

- `utils.py`
  - `load_data(...)`, `load_data_filtered(...)` read CSVs and cache results (`@st.cache_data`).
  - `get_available_years/circuits/drivers` scan directories/sample CSVs to populate dynamic filters.
  - Chart helpers like `create_average_speed_bar`, `create_speed_rpm_scatter`, etc.
- `main.py` shows overview metrics and general charts.
- `pages/` contains Streamlit multipage screens (ordered by numeric prefixes).
- `performance_monitor.py` adds optional sidebar performance metrics.

## License

MIT

## Credits

Built with:

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- [Plotly](https://plotly.com/python/)
