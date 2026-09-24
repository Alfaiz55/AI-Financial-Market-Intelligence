import os
import pandas as pd
import requests
from dotenv import load_dotenv



#Load environment variables and API configuration
load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
url = "https://www.alphavantage.co/query"


#Function to fetch and prepare market data
def fetch_market_data(ticker_symbol):
    """
    Fetch daily market data for a ticker from Alpha Vantage,
    convert it into a Pandas DataFrame, and calculate
    basic financial analytics.
    """

    
    # API parameters
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker_symbol,
        "outputsize": "compact",
        "apikey": api_key
    }


    # --------------------------------------------------------
    # Send request to Alpha Vantage
    # --------------------------------------------------------

    response = requests.get(url, params=params)

    print("Status code:", response.status_code)


    # --------------------------------------------------------
    # Convert API response from JSON into Python dictionary
    # --------------------------------------------------------

    data = response.json()


    # --------------------------------------------------------
    # Check whether market data was returned
    # --------------------------------------------------------

    if "Time Series (Daily)" not in data:
        print("No market data found.")
        print(data)

        return None


    # --------------------------------------------------------
    # Extract daily time-series data
    # --------------------------------------------------------

    time_series = data["Time Series (Daily)"]


    # --------------------------------------------------------
    # Convert JSON time-series into Pandas DataFrame
    #
    # orient="index" makes each date a row.
    # --------------------------------------------------------

    market_df = pd.DataFrame.from_dict(
        time_series,
        orient="index"
    )


    # --------------------------------------------------------
    # Rename Alpha Vantage columns into readable names
    # --------------------------------------------------------

    market_df = market_df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })


    # --------------------------------------------------------
    # Convert price and volume values from strings to numbers
    # --------------------------------------------------------

    market_df = market_df.apply(pd.to_numeric)


    # --------------------------------------------------------
    # Convert the date index into Pandas datetime format
    # --------------------------------------------------------

    market_df.index = pd.to_datetime(market_df.index)


    # --------------------------------------------------------
    # Sort dates from oldest to newest
    # --------------------------------------------------------

    market_df = market_df.sort_index()


    # ========================================================
    # 3. Calculate financial analytics
    # ========================================================

    # Daily percentage return
    market_df["Daily_Return"] = (
        market_df["Close"].pct_change()
    )


    # Average trading volume over the previous 20 trading days
    market_df["Average_Volume_20D"] = (
        market_df["Volume"].rolling(20).mean()
    )


    # Standard deviation of the previous 20 daily returns
    market_df["Rolling_Volatility_20D"] = (
        market_df["Daily_Return"].rolling(20).std()
    )


    # Average closing price over the previous 20 trading days
    market_df["Moving_Average_20D"] = (
        market_df["Close"].rolling(20).mean()
    )


    # Current volume compared with its 20-day average
    market_df["Volume_Ratio"] = (
        market_df["Volume"]
        / market_df["Average_Volume_20D"]
    )
    # Return the fully prepared DataFrame
    return market_df

# Test the function
if __name__ == "__main__":

    # Current test ticker
    ticker_symbol = "IBM"

    # Fetch market data
    market_df = fetch_market_data(ticker_symbol)


    # Only display results if data was successfully returned
    if market_df is not None:

        print(f"\nClean {ticker_symbol} Market Data:")
        print(market_df.tail())


        print(f"\nLatest {ticker_symbol} Metrics:")

        print(
            market_df[
                [
                    "Close",
                    "Daily_Return",
                    "Rolling_Volatility_20D",
                    "Moving_Average_20D",
                    "Volume_Ratio"
                ]
            ].tail(1)
        )