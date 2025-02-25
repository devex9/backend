import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_nse_data(symbol="HAL"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    }
    
    # Define date range (1 year)
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)

    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)  # Establish session

    all_data = pd.DataFrame()
    current_date = start_date
    
    while current_date <= end_date:
        chunk_start = current_date.strftime("%d-%m-%Y")
        chunk_end = (current_date + timedelta(days=30)).strftime("%d-%m-%Y")

        nse_url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}&series=[%22EQ%22]&from={chunk_start}&to={chunk_end}"
        response = session.get(nse_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data["data"])
            drop_columns = ["_id", "mTIMESTAMP", "SLBMH_TOT_VAL", "__v", "updatedAt", "createdAt", "CH_ISIN", "TIMESTAMP"]
            df.drop(columns=[col for col in drop_columns if col in df.columns], inplace=True)
            all_data = pd.concat([all_data, df], ignore_index=True)
        else:
            print(f"Failed to fetch data for {chunk_start} to {chunk_end}")

        current_date += timedelta(days=30)
    
    column_mapping = {
        "CH_TIMESTAMP": "Date",
        "CH_SYMBOL": "Stock Symbol",
        "CH_SERIES": "Series",
        "CH_OPENING_PRICE": "Open Price",
        "CH_TRADE_HIGH_PRICE": "High Price",
        "CH_TRADE_LOW_PRICE": "Low Price",
        "CH_CLOSING_PRICE": "Close Price",
        "CH_LAST_TRADED_PRICE": "Last Traded Price",
        "CH_PREV_CLS": "Previous Close",
        "CH_TOT_TRADED_QTY": "Volume",
        "CH_TOT_TRADED_VAL": "Total Traded Value",
        "CH_52WEEK_HIGH_PRICE": "52-Week High",
        "CH_52WEEK_LOW_PRICE": "52-Week Low"
    }
    all_data.rename(columns=column_mapping, inplace=True)
    all_data["Date"] = pd.to_datetime(all_data["Date"], format="%Y-%m-%d", errors="coerce").fillna(
        pd.to_datetime(all_data["Date"], format="%d-%b-%Y", errors="coerce")
    )
    
    # Replace NaN and infinite values with None to avoid JSON serialization errors
    all_data = all_data.replace([float("inf"), float("-inf")], pd.NA).fillna(pd.NA)
    
    return all_data.to_dict(orient="records")
