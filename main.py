from fastapi import FastAPI
from fetch_data import fetch_nse_data
import pandas as pd
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Stock Analysis API"}

@app.get("/stock/{symbol}")
def get_stock_data(symbol: str):
    return fetch_nse_data(symbol)

# NSE Bhavcopy URL (Latest Stock List)
NSE_BHAVCOPY_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

# Fetch stock symbols from NSE Bhavcopy
def get_stock_symbols():
    try:
        df = pd.read_csv(NSE_BHAVCOPY_URL)  # Read CSV from NSE
        return df["SYMBOL"].tolist()  # Extract stock symbols
    except Exception as e:
        return {"error": f"Failed to fetch stock list: {str(e)}"}

# API Endpoint: Get Stock List
@app.get("/stocks/list")
def stock_list():
    return {"stocks": get_stock_symbols()}
