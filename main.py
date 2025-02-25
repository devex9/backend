from fastapi import FastAPI
from fetch_data import fetch_nse_data


from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
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
