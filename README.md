# Retail Sales Analytics Dashboard

An interactive Data Analyst portfolio project built with **Python, Pandas, Plotly, and Streamlit**. Explore sales, profit, customer types, categories, regions, and product performance with filters and downloadable results.

## Dashboard features
- KPI cards: total sales, total profit, order count, profit margin
- Monthly sales and profit trend
- Sales breakdown by category
- Regional sales/profit comparison
- Top 10 products by sales
- Filters for date, region, category, and customer type
- Searchable order table and filtered CSV download

## Run locally (Windows / VS Code)

1. Install Python 3.10 or newer.
2. Extract this project ZIP and open the `Retail_Sales_Analytics_Dashboard` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
   Activate it in PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, skip activation and continue with the next commands.
5. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
6. Start the dashboard:
   ```bash
   python -m streamlit run app.py
   ```
7. Streamlit will show a local URL, usually `http://localhost:8501`. Open it in Chrome.

## Upload to GitHub
1. Create a new repository on GitHub, for example `retail-sales-analytics-dashboard`.
2. Extract the ZIP.
3. Upload the files and folders inside the project folder (especially `app.py`, `requirements.txt`, `README.md`, and `data/sales_data.csv`) to the repository.
4. Commit the files.

## Publish a live dashboard with Streamlit Community Cloud
1. Push the project to GitHub.
2. Go to https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
4. Deploy. Streamlit installs packages from `requirements.txt`.

## Project structure
```text
Retail_Sales_Analytics_Dashboard/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── sales_data.csv
```

## Important note
The bundled dataset is synthetic demo data generated for learning and portfolio demonstration. It does not represent a real company or actual customer records.
