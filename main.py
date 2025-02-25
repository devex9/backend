from fastapi import FastAPI
from fetch_data import fetch_nse_data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Stock Analysis API"}

@app.get("/stock/{symbol}")
def get_stock_data(symbol: str):
    return fetch_nse_data(symbol)
