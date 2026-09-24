import os
import pandas as pd
import requests
from dotenv import load_dotenv



load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
url = "https://www.alphavantage.co/query"




def fetch_news_data(ticker_symbol):
    """
    Fetch financial news for a ticker from Alpha Vantage,
    extract ticker-specific sentiment information, and
    return a clean Pandas DataFrame.
    """

    
    # API parameters
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker_symbol,
        "apikey": api_key
    }


   
    # Send request to Alpha Vantage
    response = requests.get(url, params=params)

    print("Status code:", response.status_code)


    # Convert API response from JSON into Python dictionary
    data = response.json()



    # Check whether the API returned news data

    if "feed" not in data:
        print("No news data found.")
        print(data)

        return None

    # Convert news feed into DataFrame
    news_df = pd.DataFrame(data["feed"])



    # Keep only the article-level information we need

    news_df = news_df[
        [
            "title",
            "url",
            "time_published",
            "source",
            "summary",
            "ticker_sentiment"
        ]
    ]


  
    #Extract ticker-specific information
    clean_news = []


    for _, article in news_df.iterrows():

        for ticker_data in article["ticker_sentiment"]:

            # Find sentiment information for our ticker
            if ticker_data.get("ticker") == ticker_symbol:

                clean_news.append({
                    "Ticker": ticker_symbol,
                    "Title": article["title"],
                    "URL": article["url"] ,
                    "Time_Published": article["time_published"],
                    "Source": article["source"],
                    "Summary": article["summary"],
                    "Relevance_Score": float(
                        ticker_data["relevance_score"]
                    ),
                    "Sentiment_Score": float(
                        ticker_data["ticker_sentiment_score"]
                    ),
                    "Sentiment_Label": ticker_data[
                        "ticker_sentiment_label"
                    ]
                })

                # Stop searching this article once
                # the requested ticker is found
                break



    clean_news_df = pd.DataFrame(clean_news)

    # Convert publication timestamp into datetime

    clean_news_df["Time_Published"] = pd.to_datetime(
        clean_news_df["Time_Published"],
        format="%Y%m%dT%H%M%S"
    )

    # Separate publication date and time
    clean_news_df["News_Date"] = (
        clean_news_df["Time_Published"].dt.date
    )

    clean_news_df["News_Time"] = (
        clean_news_df["Time_Published"].dt.time
    )

    # Return the fully prepared news DataFrame
    return clean_news_df

#Test the function
if __name__ == "__main__":

    # Current test ticker
    ticker_symbol = "IBM"

    # Fetch news data
    clean_news_df = fetch_news_data(ticker_symbol)


    # Display results only if data was successfully returned
    if clean_news_df is not None:

        print(f"\nClean {ticker_symbol} News Data:")
        print(clean_news_df.head())


        print(
            f"\nNumber of {ticker_symbol}-related articles:",
            len(clean_news_df)
        )

    print(clean_news_df.columns.tolist())