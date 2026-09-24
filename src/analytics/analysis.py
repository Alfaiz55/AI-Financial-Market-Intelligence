import sqlite3
import os

import pandas as pd

# Database location
database_path = os.path.join(
    "data",
    "financial_market.db"
)

# Get market data from database
def get_market_data(ticker_symbol):

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        Ticker,
        Date,
        Open,
        High,
        Low,
        Close,
        Volume,
        Daily_Return,
        Average_Volume_20D,
        Rolling_Volatility_20D,
        Moving_Average_20D,
        Volume_Ratio
    FROM market_data
    WHERE Ticker = ?
    ORDER BY Date ASC;
    """

    market_df = pd.read_sql_query(
        query,
        connection,
        params=(ticker_symbol,)
    )

    connection.close()

    if market_df.empty:
        return None

    market_df["Date"] = pd.to_datetime(
        market_df["Date"]
    )

    return market_df


# Get news data from database
def get_news_data(ticker_symbol):

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        News_ID,
        Ticker,
        Title,
        URL,
        Time_Published,
        Source,
        Summary,
        Relevance_Score,
        Sentiment_Score,
        Sentiment_Label,
        News_Date,
        News_Time
    FROM news_data
    WHERE Ticker = ?
    ORDER BY Time_Published DESC;
    """

    news_df = pd.read_sql_query(
        query,
        connection,
        params=(ticker_symbol,)
    )

    connection.close()

    if news_df.empty:
        return None

    news_df["Time_Published"] = pd.to_datetime(
        news_df["Time_Published"]
    )

    news_df["News_Date"] = pd.to_datetime(
        news_df["News_Date"]
    ).dt.date

    return news_df



# Latest market snapshot
def analyze_latest_market(market_df):

    latest = market_df.iloc[-1]

    close_price = latest["Close"]
    daily_return = latest["Daily_Return"]
    volatility = latest["Rolling_Volatility_20D"]
    moving_average = latest["Moving_Average_20D"]
    volume_ratio = latest["Volume_Ratio"]

    # Distance from 20-day moving average
    price_vs_ma = (
        (close_price - moving_average)
        / moving_average
    )

    return {
        "Ticker": latest["Ticker"],
        "Date": latest["Date"].strftime("%Y-%m-%d"),
        "Close": close_price,
        "Daily_Return": daily_return,
        "Rolling_Volatility_20D": volatility,
        "Moving_Average_20D": moving_average,
        "Volume_Ratio": volume_ratio,
        "Price_vs_20D_MA": price_vs_ma
    }


# Recent performance analysis
def analyze_recent_performance(
    market_df,
    window=20
):

    recent_data = market_df.tail(window)

    first_close = recent_data.iloc[0]["Close"]
    latest_close = recent_data.iloc[-1]["Close"]

    total_return = (
        latest_close - first_close
    ) / first_close

    average_daily_return = (
        recent_data["Daily_Return"].mean()
    )

    highest_close = recent_data["Close"].max()
    lowest_close = recent_data["Close"].min()

    return {
        "Period_Days": len(recent_data),
        "Period_Return": total_return,
        "Average_Daily_Return": average_daily_return,
        "Highest_Close": highest_close,
        "Lowest_Close": lowest_close
    }


# Volatility analysis
def analyze_volatility(
    market_df,
    window=20
):

    recent_data = market_df.tail(window)

    average_volatility = (
        recent_data["Rolling_Volatility_20D"].mean()
    )

    latest_volatility = (
        recent_data.iloc[-1]["Rolling_Volatility_20D"]
    )

    maximum_volatility = (
        recent_data["Rolling_Volatility_20D"].max()
    )

    minimum_volatility = (
        recent_data["Rolling_Volatility_20D"].min()
    )

    return {
        "Latest_Volatility": latest_volatility,
        "Average_Volatility": average_volatility,
        "Maximum_Volatility": maximum_volatility,
        "Minimum_Volatility": minimum_volatility
    }


# Volume analysis
def analyze_volume(
    market_df,
    window=20
):

    recent_data = market_df.tail(window)

    average_volume = (
        recent_data["Volume"].mean()
    )

    latest_volume = (
        recent_data.iloc[-1]["Volume"]
    )

    latest_volume_ratio = (
        recent_data.iloc[-1]["Volume_Ratio"]
    )

    maximum_volume = (
        recent_data["Volume"].max()
    )

    return {
        "Latest_Volume": latest_volume,
        "Average_Volume": average_volume,
        "Volume_Ratio": latest_volume_ratio,
        "Maximum_Volume": maximum_volume
    }

# Trend analysis
def analyze_trend(latest_market):

    close_price = latest_market["Close"]
    moving_average = latest_market["Moving_Average_20D"]

    if close_price > moving_average:
        trend = "Above 20-day moving average"

    elif close_price < moving_average:
        trend = "Below 20-day moving average"

    else:
        trend = "At 20-day moving average"

    return trend


# Daily movement analysis
def analyze_daily_movement(latest_market):

    daily_return = latest_market["Daily_Return"]

    if daily_return > 0:
        direction = "Positive"

    elif daily_return < 0:
        direction = "Negative"

    else:
        direction = "Flat"

    return {
        "Direction": direction,
        "Return": daily_return
    }


# Detect unusual price movement
def detect_unusual_movement(latest_market):

    daily_return = abs(
        latest_market["Daily_Return"]
    )

    volatility = (
        latest_market["Rolling_Volatility_20D"]
    )

    volume_ratio = (
        latest_market["Volume_Ratio"]
    )

    unusual_price_move = (
        daily_return > volatility
    )

    unusual_volume = (
        volume_ratio >= 1.5
    )

    return {
        "Unusual_Price_Movement": unusual_price_move,
        "Unusual_Volume": unusual_volume
    }


# News analysis
def analyze_news(news_df):

    if news_df is None or news_df.empty:

        return {
            "News_Count": 0,
            "Average_Sentiment": None,
            "Bullish_Count": 0,
            "Bearish_Count": 0,
            "Neutral_Count": 0
        }

    news_count = len(news_df)

    average_sentiment = (
        news_df["Sentiment_Score"].mean()
    )

    bullish_count = (
        news_df["Sentiment_Label"]
        .str.contains("Bullish", case=False, na=False)
        .sum()
    )

    bearish_count = (
        news_df["Sentiment_Label"]
        .str.contains("Bearish", case=False, na=False)
        .sum()
    )

    neutral_count = (
        news_df["Sentiment_Label"]
        .str.contains("Neutral", case=False, na=False)
        .sum()
    )

    return {
        "News_Count": news_count,
        "Average_Sentiment": average_sentiment,
        "Bullish_Count": int(bullish_count),
        "Bearish_Count": int(bearish_count),
        "Neutral_Count": int(neutral_count)
    }


# Latest news
def get_latest_news(
    news_df,
    limit=5
):

    if news_df is None or news_df.empty:
        return []

    latest_news = news_df.head(limit)

    news_list = []

    for _, article in latest_news.iterrows():

        news_list.append({
            "Title": article["Title"],
            "URL": article["URL"],
            "Source": article["Source"],
            "Time_Published": article[
                "Time_Published"
            ].strftime("%Y-%m-%d %H:%M:%S"),
            "Relevance_Score": article[
                "Relevance_Score"
            ],
            "Sentiment_Score": article[
                "Sentiment_Score"
            ],
            "Sentiment_Label": article[
                "Sentiment_Label"
            ]
        })

    return news_list


# Combine market and news by date
def analyze_market_news_relationship(
    market_df,
    news_df
):

    if news_df is None or news_df.empty:
        return pd.DataFrame()

    news_by_date = (
        news_df
        .groupby("News_Date")
        .agg(
            News_Count=("News_ID", "count"),
            Average_News_Sentiment=(
                "Sentiment_Score",
                "mean"
            )
        )
        .reset_index()
    )

    market_copy = market_df.copy()

    market_copy["News_Date"] = (
        market_copy["Date"].dt.date
    )

    combined_df = market_copy.merge(
        news_by_date,
        on="News_Date",
        how="left"
    )

    return combined_df

# Analyze news around a market date
def analyze_news_around_market_date(
    news_df,
    target_date
):

    if news_df is None or news_df.empty:
        return pd.DataFrame()

    target_date = pd.to_datetime(
        target_date
    ).date()

    same_day_news = news_df[
        news_df["News_Date"] == target_date
    ].copy()

    if same_day_news.empty:
        return pd.DataFrame()

    # Alpha Vantage timestamps are treated as UTC
    same_day_news["Time_Published"] = (
        pd.to_datetime(
            same_day_news["Time_Published"],
            utc=True
        )
        .dt.tz_convert("America/New_York")
    )

    # Classify news relative to NYSE regular market hours
    def classify_news_time(timestamp):

        market_open = timestamp.replace(
            hour=9,
            minute=30,
            second=0
        )

        market_close = timestamp.replace(
            hour=16,
            minute=0,
            second=0
        )

        if timestamp < market_open:
            return "Pre-Market"

        elif timestamp <= market_close:
            return "Market Hours"

        else:
            return "After-Market"

    same_day_news["Market_Timing"] = (
        same_day_news["Time_Published"]
        .apply(classify_news_time)
    )

    # Most relevant articles first
    same_day_news = same_day_news.sort_values(
        by="Relevance_Score",
        ascending=False
    )

    return same_day_news[
        [
            "Title",
            "URL",
            "Time_Published",
            "Market_Timing",
            "Source",
            "Relevance_Score",
            "Sentiment_Score",
            "Sentiment_Label"
        ]
    ]

def prepare_llm_context(analysis):
    """
    Convert the analysis results into a clean Python dictionary
    that can be safely passed to an LLM.
    """

    latest_market = analysis["latest_market"]
    recent_performance = analysis["recent_performance"]
    volatility = analysis["volatility"]
    volume = analysis["volume"]
    daily_movement = analysis["daily_movement"]
    unusual_movement = analysis["unusual_movement"]
    news_analysis = analysis["news_analysis"]

    llm_context = {
        "ticker": str(latest_market["Ticker"]),
        "date": str(latest_market["Date"]),

        "latest_market": {
            "close": float(latest_market["Close"]),
            "daily_return": float(latest_market["Daily_Return"]),
            "rolling_volatility_20d": float(
                latest_market["Rolling_Volatility_20D"]
            ),
            "moving_average_20d": float(
                latest_market["Moving_Average_20D"]
            ),
            "volume_ratio": float(
                latest_market["Volume_Ratio"]
            ),
            "price_vs_20d_ma": float(
                latest_market["Price_vs_20D_MA"]
            )
        },

        "recent_performance": {
            "period_days": int(
                recent_performance["Period_Days"]
            ),
            "period_return": float(
                recent_performance["Period_Return"]
            ),
            "average_daily_return": float(
                recent_performance["Average_Daily_Return"]
            ),
            "highest_close": float(
                recent_performance["Highest_Close"]
            ),
            "lowest_close": float(
                recent_performance["Lowest_Close"]
            )
        },

        "volatility": {
            "latest": float(
                volatility["Latest_Volatility"]
            ),
            "average": float(
                volatility["Average_Volatility"]
            ),
            "maximum": float(
                volatility["Maximum_Volatility"]
            ),
            "minimum": float(
                volatility["Minimum_Volatility"]
            )
        },

        "volume": {
            "latest": int(
                volume["Latest_Volume"]
            ),
            "average": float(
                volume["Average_Volume"]
            ),
            "ratio": float(
                volume["Volume_Ratio"]
            ),
            "maximum": int(
                volume["Maximum_Volume"]
            )
        },

        "trend": str(analysis["trend"]),

        "daily_movement": {
            "direction": str(
                daily_movement["Direction"]
            ),
            "return": float(
                daily_movement["Return"]
            )
        },

        "unusual_movement": {
            "unusual_price_movement": bool(
                unusual_movement["Unusual_Price_Movement"]
            ),
            "unusual_volume": bool(
                unusual_movement["Unusual_Volume"]
            )
        },

        "news_analysis": {
            "news_count": int(
                news_analysis["News_Count"]
            ),
            "average_sentiment": (
                float(news_analysis["Average_Sentiment"])
                if news_analysis["Average_Sentiment"] is not None
                else None
            ),
            "bullish_count": int(
                news_analysis["Bullish_Count"]
            ),
            "bearish_count": int(
                news_analysis["Bearish_Count"]
            ),
            "neutral_count": int(
                news_analysis["Neutral_Count"]
            )
        },

        "latest_news": []
    }

    for article in analysis["latest_news"]:
        llm_context["latest_news"].append({
            "title": str(article["Title"]),
            "url": str(article["URL"]),
            "source": str(article["Source"]),
            "time_published": str(
                article["Time_Published"]
            ),
            "relevance_score": float(
                article["Relevance_Score"]
            ),
            "sentiment_score": float(
                article["Sentiment_Score"]
            ),
            "sentiment_label": str(
                article["Sentiment_Label"]
            )
        })

    return llm_context
# Create complete analysis
def create_market_analysis(ticker_symbol):

    market_df = get_market_data(
        ticker_symbol
    )

    news_df = get_news_data(
        ticker_symbol
    )

    if market_df is None:
        print(
            f"No market data found for {ticker_symbol}."
        )
        return None

    latest_market = analyze_latest_market(
        market_df
    )

    recent_performance = analyze_recent_performance(
        market_df
    )

    volatility = analyze_volatility(
        market_df
    )

    volume = analyze_volume(
        market_df
    )

    trend = analyze_trend(
        latest_market
    )

    daily_movement = analyze_daily_movement(
        latest_market
    )

    unusual_movement = detect_unusual_movement(
        latest_market
    )

    news_analysis = analyze_news(
        news_df
    )

    latest_news = get_latest_news(
        news_df
    )
    
    latest_market_news = analyze_news_around_market_date(
        news_df,
        latest_market["Date"]

    )

    market_news = analyze_market_news_relationship(
        market_df,
        news_df
    )

    analysis = {

        "latest_market": latest_market,

        "recent_performance": recent_performance,

        "volatility": volatility,

        "volume": volume,

        "trend": trend,

        "daily_movement": daily_movement,

        "unusual_movement": unusual_movement,

        "news_analysis": news_analysis,
        "latest_news": latest_news,

        "latest_market_news": latest_market_news,

        "market_news_data": market_news
    }

    return analysis

# Test analysis
if __name__ == "__main__":

    ticker_symbol = "IBM"

    analysis = create_market_analysis(
        ticker_symbol
    )

    if analysis is not None:

        llm_context= prepare_llm_context(analysis)
        print("\nLLM Context:")
        print(llm_context)
        
        

    print("\nNews Around Latest Market Date:")

    print(
        analysis["latest_market_news"].to_string(

            index=False
        )
    )      
