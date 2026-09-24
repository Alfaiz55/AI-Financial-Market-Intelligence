import sqlite3
import os



# Database location


database_path = os.path.join("data", "financial_market.db")



# Connect to SQLite database


connection = sqlite3.connect(database_path)
cursor = connection.cursor()

print("Database Connected successfully.")


# Create market_data table

create_market_table = """
CREATE TABLE IF NOT EXISTS market_data (

    Market_ID INTEGER PRIMARY KEY AUTOINCREMENT,

    Ticker TEXT NOT NULL,

    Date DATE NOT NULL,

    Open REAL,

    High REAL,

    Low REAL,

    Close REAL,

    Volume INTEGER,

    Daily_Return REAL,

    Average_Volume_20D REAL,
    Rolling_Volatility_20D REAL,
    Moving_Average_20D REAL,
    Volume_Ratio REAL,
    UNIQUE(Ticker, Date)

);
"""

connection.execute(create_market_table)

# Create news_data table
create_news_table = """
CREATE TABLE IF NOT EXISTS news_data (
    News_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Ticker TEXT NOT NULL,
    Title TEXT NOT NULL,
    Time_Published DATETIME NOT NULL,
    URL TEXT UNIQUE NOT NULL,
    Source TEXT,
    Summary TEXT,
    Relevance_Score REAL,
    Sentiment_Score REAL,
    Sentiment_Label TEXT,
    News_Date DATE,
    News_Time TIME
);
"""

connection.execute(create_news_table)
connection.commit()

print("Database tables created successfully.")


# Insert market data
def insert_market_data(market_df, ticker_symbol):
    market_query = """
    INSERT OR IGNORE INTO market_data (
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
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    for date, row in market_df.iterrows():
        values = (
            ticker_symbol,
            date.strftime("%Y-%m-%d"),
            row["Open"],
            row["High"],
            row["Low"],
            row["Close"],
            row["Volume"],
            row["Daily_Return"],
            row["Average_Volume_20D"],
            row["Rolling_Volatility_20D"],
            row["Moving_Average_20D"],
            row["Volume_Ratio"]
        )

        cursor.execute(market_query, values)
        connection.commit()


    print(f"{ticker_symbol} market data inserted successfully.")

def get_latest_market_date(ticker_symbol):

    query = """
    SELECT MAX(Date)
    FROM market_data
    WHERE Ticker = ?;
    """

    cursor.execute(query, (ticker_symbol,))

    result = cursor.fetchone()

    if result is None or result[0] is None:
        return None

    return result[0]


# Insert news data

def insert_news_data(news_df):

    news_query = """
    INSERT OR IGNORE INTO news_data (
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
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

    for _, row in news_df.iterrows():

        values = (
            row["Ticker"],
            row["Title"],
            row["URL"],
            row["Time_Published"].strftime("%Y-%m-%d %H:%M:%S"),
            row["Source"],
            row["Summary"],
            row["Relevance_Score"],
            row["Sentiment_Score"],
            row["Sentiment_Label"],
            row["News_Date"].isoformat(),
            row["News_Time"].strftime("%H:%M:%S")
        )

        cursor.execute(news_query, values)

    connection.commit()

    print(f"{len(news_df)} news articles inserted successfully.")


