import math
import pandas as pd
from src.analytics.analysis import (
    get_market_data,
    get_news_data,
    create_market_analysis,
    analyze_news_around_market_date
)

from src.database.database import insert_market_data
from src.api.market_api import fetch_market_data

from src.analytics.analysis2 import (
    analyze_momentum,
    analyze_price_position,
    analyze_drawdown,
    analyze_volatility_regime,
    analyze_volume_anomaly,
    analyze_price_movement_severity,
    analyze_latest_candle,
    analyze_price_levels
)


def make_json_safe(value):
    """
    Convert Pandas and NumPy values into standard Python types
    that can safely be passed to an LLM or serialized as JSON.
    """

    if value is None:
        return None

    # Handle dictionaries
    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    # Handle lists / tuples
    if isinstance(value, (list, tuple)):
        return [
            make_json_safe(item)
            for item in value
        ]

    # Handle Pandas DataFrame
    if hasattr(value, "to_dict"):
        return make_json_safe(
            value.to_dict(orient="records")
        )

    # Handle Pandas / NumPy scalar values
    if hasattr(value, "item"):
        try:
            return value.item()
        except (ValueError, TypeError):
            pass

    # Handle Pandas Timestamp / datetime
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except (ValueError, TypeError):
            pass

    # Handle NaN / infinity
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None

    return value


# ============================================================
# MARKET DATA TOOL
# ============================================================

def get_market_data_tool(ticker_symbol):
    """
    Get recent historical market data for a ticker.
    """

    market_df = get_market_data(ticker_symbol)

    if market_df is None:
        return {
            "success": False,
            "message": f"No market data found for {ticker_symbol}."
        }

    result = {
        "success": True,
        "ticker": ticker_symbol,
        "records": len(market_df),
        "data": market_df.tail(20).to_dict(
            orient="records"
        )
    }

    return make_json_safe(result)


# ============================================================
# NEWS DATA TOOL
# ============================================================

def get_news_data_tool(ticker_symbol):
    """
    Get recent financial news for a ticker.
    """

    news_df = get_news_data(ticker_symbol)

    if news_df is None or news_df.empty:
        return {
            "success": False,
            "message": f"No news found for {ticker_symbol}."
        }

    result = {
        "success": True,
        "ticker": ticker_symbol,
        "records": len(news_df),
        "data": news_df.head(20).to_dict(
            orient="records"
        )
    }

    return make_json_safe(result)


# ============================================================
# COMPLETE MARKET ANALYSIS TOOL
# ============================================================

def get_market_analysis_tool(ticker_symbol):
    """
    Run the complete basic market and news analysis.
    """

    analysis = create_market_analysis(
        ticker_symbol
    )

    if analysis is None:
        return {
            "success": False,
            "message": f"Unable to analyze {ticker_symbol}."
        }

    result = {
        "success": True,
        "ticker": ticker_symbol,
        "analysis": analysis
    }

    return make_json_safe(result)


# ============================================================
# ADVANCED ANALYTICS TOOL
# ============================================================

def get_advanced_analysis_tool(ticker_symbol):
    """
    Run advanced financial analytics for a ticker.
    """

    market_df = get_market_data(
        ticker_symbol
    )

    if market_df is None:
        return {
            "success": False,
            "message": f"No market data found for {ticker_symbol}."
        }

    result = {
        "success": True,
        "ticker": ticker_symbol,

        "momentum": analyze_momentum(
            market_df
        ),

        "price_position": analyze_price_position(
            market_df
        ),

        "drawdown": analyze_drawdown(
            market_df
        ),

        "volatility_regime": analyze_volatility_regime(
            market_df
        ),

        "volume_anomaly": analyze_volume_anomaly(
            market_df
        ),

        "price_movement_severity":
            analyze_price_movement_severity(
                market_df
            ),

        "latest_candle": analyze_latest_candle(
            market_df
        ),

        "price_levels": analyze_price_levels(
            market_df
        )
    }

    return make_json_safe(result)


# ============================================================
# MARKET + NEWS TIMING TOOL
# ============================================================

def get_market_news_timing_tool(ticker_symbol):
    """
    Analyze news published around the latest market date.
    """

    market_df = get_market_data(
        ticker_symbol
    )

    news_df = get_news_data(
        ticker_symbol
    )

    if market_df is None:
        return {
            "success": False,
            "message": f"No market data found for {ticker_symbol}."
        }

    if news_df is None or news_df.empty:
        return {
            "success": False,
            "message": f"No news found for {ticker_symbol}."
        }

    latest_date = market_df.iloc[-1]["Date"]

    news_timing = analyze_news_around_market_date(
        news_df,
        latest_date
    )

    result = {
        "success": True,
        "ticker": ticker_symbol,
        "market_date": str(
            latest_date.date()
            if hasattr(latest_date, "date")
            else latest_date
        ),
        "news": news_timing.to_dict(
            orient="records"
        )
    }

    return make_json_safe(result)


# GENERIC MARKET DATA QUERY
def query_market_data_tool(
    ticker_symbol,
    fields=None,
    start_date=None,
    end_date=None,
    limit=20
):
    """
    Query market data for a ticker.

    The latest market data is fetched from the API before querying
    the database so that the tool works with fresh data.
    """

    # 1. Make sure the latest market data is available
    refresh_result = get_or_fetch_market_data(ticker_symbol)

    if not refresh_result.get("success"):
        return {
            "success": False,
            "ticker_symbol": ticker_symbol,
            "error": refresh_result.get(
                "message",
                "Market data could not be retrieved."
            )
        }

    # 2. Allowed database fields
    allowed_fields = {
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Daily_Return",
        "Average_Volume_20D",
        "Rolling_Volatility_20D",
        "Moving_Average_20D",
        "Volume_Ratio"
    }

    # 3. Default fields
    if fields is None:
        fields = ["Date", "Close"]

    # 4. Validate fields
    invalid_fields = [
        field for field in fields
        if field not in allowed_fields
    ]

    if invalid_fields:
        return {
            "success": False,
            "ticker_symbol": ticker_symbol,
            "error": f"Invalid fields requested: {invalid_fields}",
            "allowed_fields": sorted(allowed_fields)
        }

    # 5. Read data directly from database
    market_df = get_market_data(ticker_symbol)

    if market_df.empty:
        return {
            "success": False,
            "ticker_symbol": ticker_symbol,
            "error": "No market data found."
        }

    # 6. Convert Date
    market_df["Date"] = pd.to_datetime(
        market_df["Date"],
        errors="coerce"
    )

    market_df = market_df.dropna(subset=["Date"])

    # 7. Date filters
    if start_date is not None:
        start_date_value = pd.to_datetime(
            start_date,
            errors="coerce"
        )

        if pd.isna(start_date_value):
            return {
                "success": False,
                "ticker_symbol": ticker_symbol,
                "error": f"Invalid start_date: {start_date}"
            }

        market_df = market_df[
            market_df["Date"] >= start_date_value
        ]

    if end_date is not None:
        end_date_value = pd.to_datetime(
            end_date,
            errors="coerce"
        )

        if pd.isna(end_date_value):
            return {
                "success": False,
                "ticker_symbol": ticker_symbol,
                "error": f"Invalid end_date: {end_date}"
            }

        market_df = market_df[
            market_df["Date"] <= end_date_value
        ]

    # 8. Newest first
    market_df = market_df.sort_values(
        by="Date",
        ascending=False
    )

    # 9. Select requested fields
    market_df = market_df[fields]

    # 10. Limit rows
    market_df = market_df.head(limit)

    # 11. Convert Date to string
    if "Date" in market_df.columns:
        market_df["Date"] = market_df["Date"].dt.strftime(
            "%Y-%m-%d"
        )

    # 12. JSON-safe records
    records = market_df.to_dict(
        orient="records"
    )

    records = make_json_safe(records)

    # 13. Return result
    return {
        "success": True,
        "ticker_symbol": ticker_symbol,
        "source": refresh_result.get("source"),
        "latest_date": refresh_result.get("latest_date"),
        "fields": fields,
        "row_count": len(records),
        "data": records
    }

# FRESH MARKET DATA FUNCTION

def get_or_fetch_market_data(ticker_symbol):
    """
    Fetch the latest available market data for any ticker,
    store it in the database, and make the data available
    for subsequent queries.

    Existing records are not deleted.

    The database UNIQUE(Ticker, Date) constraint prevents
    duplicate records.
    """

    print(
        f"Fetching latest market data "
        f"for {ticker_symbol}..."
    )

    market_df = fetch_market_data(
        ticker_symbol
    )

    if market_df is None or market_df.empty:
        return {
            "success": False,
            "ticker": ticker_symbol,
            "message": (
                f"Unable to fetch market data "
                f"for {ticker_symbol}."
            )
        }

    # --------------------------------------------------------
    # STORE DATA
    # --------------------------------------------------------

    insert_market_data(
        market_df,
        ticker_symbol
    )

    latest_date = market_df.index.max()

    return {
        "success": True,
        "ticker": ticker_symbol,
        "source": "api",
        "latest_date": str(
            latest_date.date()
        ),
        "message": (
            f"Latest available market data "
            f"for {ticker_symbol} was fetched "
            f"and stored through "
            f"{latest_date.date()}."
        )
    }


# ============================================================
# FOCUSED METRIC TOOLS
# ============================================================
#
# These tools use query_market_data_tool().
#
# Therefore they automatically inherit the freshness
# mechanism above.
#
# Gemini can call these individually or combine several
# tools for a more complex question.
# ============================================================


# ------------------------------------------------------------
# LATEST PRICE
# ------------------------------------------------------------

def get_latest_price_tool(ticker_symbol):
    """
    Get the latest available closing price.
    """

    return query_market_data_tool(
        ticker_symbol=ticker_symbol,
        fields=[
            "Date",
            "Close"
        ],
        limit=1
    )


# ------------------------------------------------------------
# AVERAGE PRICE
# ------------------------------------------------------------

def get_average_price_tool(
    ticker_symbol,
    window=20
):
    """
    Calculate the average closing price over
    the requested number of trading sessions.
    """

    result = query_market_data_tool(
        ticker_symbol=ticker_symbol,
        fields=[
            "Date",
            "Close"
        ],
        limit=window
    )

    if not result.get("success"):
        return result

    records = result.get(
        "data",
        []
    )

    valid_prices = [
        row["Close"]
        for row in records
        if row.get("Close") is not None
    ]

    if not valid_prices:
        return {
            "success": False,
            "ticker": ticker_symbol,
            "message": (
                "No closing price data "
                "available."
            )
        }

    average_price = (
        sum(valid_prices)
        / len(valid_prices)
    )

    return make_json_safe({
        "success": True,
        "ticker": ticker_symbol,
        "window": len(valid_prices),
        "average_closing_price": average_price
    })


# ------------------------------------------------------------
# MOVING AVERAGE
# ------------------------------------------------------------

def get_moving_average_tool(
    ticker_symbol,
    window=20
):
    """
    Get the latest moving average price for the
    requested window.
    """

    result = query_market_data_tool(
        ticker_symbol=ticker_symbol,
        fields=[
            "Date",
            "Moving_Average_20D"
        ],
        limit=window
    )

    if not result.get("success"):
        return result

    records = result.get(
        "data",
        []
    )

    # The moving average value is already calculated
    # by market_api.py.
    valid_records = [
        row
        for row in records
        if row.get(
            "Moving_Average_20D"
        ) is not None
    ]

    if not valid_records:
        return {
            "success": False,
            "ticker": ticker_symbol,
            "message": (
                "Moving average data "
                "is not available."
            )
        }

    latest_record = valid_records[0]

    return make_json_safe({
        "success": True,
        "ticker": ticker_symbol,
        "window": window,
        "date": latest_record.get("Date"),
        "moving_average": (
            latest_record.get(
                "Moving_Average_20D"
            )
        )
    })


# ------------------------------------------------------------
# LATEST RETURN
# ------------------------------------------------------------

def get_latest_return_tool(ticker_symbol):
    """
    Get the latest daily return.
    """

    return query_market_data_tool(
        ticker_symbol=ticker_symbol,
        fields=[
            "Date",
            "Daily_Return"
        ],
        limit=1
    )


# ------------------------------------------------------------
# AVERAGE RETURN
# ------------------------------------------------------------

def get_average_return_tool(
    ticker_symbol,
    window=20
):
    """
    Calculate the average daily return over
    the requested number of trading sessions.
    """

    result = query_market_data_tool(
        ticker_symbol=ticker_symbol,
        fields=[
            "Date",
            "Daily_Return"
        ],
        limit=window
    )

    if not result.get("success"):
        return result

    records = result.get(
        "data",
        []
    )

    valid_returns = [
        row["Daily_Return"]
        for row in records
        if row.get("Daily_Return") is not None
    ]

    if not valid_returns:
        return {
            "success": False,
            "ticker": ticker_symbol,
            "message": (
                "No daily return data "
                "available."
            )
        }

    average_return = (
        sum(valid_returns)
        / len(valid_returns)
    )

    return make_json_safe({
        "success": True,
        "ticker": ticker_symbol,
        "window": len(valid_returns),
        "average_daily_return": average_return
    })


# ------------------------------------------------------------
# LATEST VOLUME
# ------------------------------------------------------------

def get_latest_volume_tool(ticker_symbol):
    """
    Get the latest trading volume.
    """

    return query_market_data_tool(
        ticker_symbol=ticker_symbol,
        fields=[
            "Date",
            "Volume"
        ],
        limit=1
    )


# ------------------------------------------------------------
# AVERAGE VOLUME
# ------------------------------------------------------------

def get_average_volume_tool(
    ticker_symbol,
    window=20
):
    """
    Calculate the average trading volume over
    the requested number of trading sessions.
    """

    result = query_market_data_tool(
        ticker_symbol=ticker_symbol,
        fields=[
            "Date",
            "Volume"
        ],
        limit=window
    )

    if not result.get("success"):
        return result

    records = result.get(
        "data",
        []
    )

    valid_volumes = [
        row["Volume"]
        for row in records
        if row.get("Volume") is not None
    ]

    if not valid_volumes:
        return {
            "success": False,
            "ticker": ticker_symbol,
            "message": (
                "No volume data available."
            )
        }

    average_volume = (
        sum(valid_volumes)
        / len(valid_volumes)
    )

    return make_json_safe({
        "success": True,
        "ticker": ticker_symbol,
        "window": len(valid_volumes),
        "average_volume": average_volume
    })


# ------------------------------------------------------------
# VOLATILITY
# ------------------------------------------------------------

def get_volatility_tool(
    ticker_symbol,
    window=20
):
    """
    Get the latest rolling volatility value.
    """

    result = query_market_data_tool(
        ticker_symbol=ticker_symbol,
        fields=[
            "Date",
            "Rolling_Volatility_20D"
        ],
        limit=window
    )

    if not result.get("success"):
        return result

    records = result.get(
        "data",
        []
    )

    valid_records = [
        row
        for row in records
        if row.get(
            "Rolling_Volatility_20D"
        ) is not None
    ]

    if not valid_records:
        return {
            "success": False,
            "ticker": ticker_symbol,
            "message": (
                "Volatility data "
                "is not available."
            )
        }

    latest_record = valid_records[0]

    return make_json_safe({
        "success": True,
        "ticker": ticker_symbol,
        "window": window,
        "date": latest_record.get("Date"),
        "rolling_volatility": (
            latest_record.get(
                "Rolling_Volatility_20D"
            )
        )
    })