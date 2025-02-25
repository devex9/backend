import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_nse_data(symbol="HAL"):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Define date range (1 year)
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)

    nse_url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}&series=[%22EQ%22]&from={start_date.strftime('%d-%m-%Y')}&to={end_date.strftime('%d-%m-%Y')}"
    
    session = requests.Session()
    response = session.get(nse_url, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"]
        df = pd.DataFrame(data)
        
        # Rename & clean columns
        column_mapping = {
            "CH_TIMESTAMP": "Date",
            "CH_SYMBOL": "Stock Symbol",
            "CH_CLOSING_PRICE": "Close Price",
            "CH_TOT_TRADED_QTY": "Volume"
        }
        df.rename(columns=column_mapping, inplace=True)
        
        # Convert date
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%Y", errors="coerce")
        
        return df.to_dict(orient="records")
    else:
        return {"error": "Failed to fetch data"}

