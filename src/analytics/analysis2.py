import pandas as pd

#advanced financial analytics

#price momentum analysis

def analyze_momentum(market_df):
    """Analyze short-term and medium-term price momentum."""
    latest= market_df.iloc[-1]
    close_price=latest["Close"]
    return_5d=(market_df["Close"].pct_change(5).iloc[-1])
    return_10d = (
        market_df["Close"].pct_change(10).iloc[-1]
    )

    return_20d = (
        market_df["Close"].pct_change(20).iloc[-1]
    )

    if return_5d > 0 and return_10d > 0:
        momentum = "Positive"

    elif return_5d < 0 and return_10d < 0:
        momentum = "Negative"

    else:
        momentum = "Mixed"

    return {
        "Current_Price": close_price,
        "Return_5D": return_5d,
        "Return_10D": return_10d,
        "Return_20D": return_20d,
        "Momentum": momentum
    }

#price position within recent range

def analyze_price_position(
    market_df,
    window=20
):
    """
    Determine where the latest closing price sits
    within the recent high-low trading range.
    """

    recent_data = market_df.tail(window)

    highest_price = recent_data["High"].max()
    lowest_price = recent_data["Low"].min()

    latest_close = recent_data.iloc[-1]["Close"]

    price_range = highest_price - lowest_price

    if price_range == 0:
        range_position = 0.5

    else:
        range_position = (
            latest_close - lowest_price
        ) / price_range

    if range_position >= 0.75:
        position = "Near recent high"

    elif range_position <= 0.25:
        position = "Near recent low"

    else:
        position = "Middle of recent range"

    return {
        "Highest_Price": highest_price,
        "Lowest_Price": lowest_price,
        "Latest_Close": latest_close,
        "Range_Position": range_position,
        "Position": position
    }

#Drawdown analysis

def analyze_drawdown(market_df):
    """
    Measure the current decline from the historical
    peak close available in the dataset.
    """

    latest_close = market_df.iloc[-1]["Close"]

    highest_close = market_df["Close"].max()

    drawdown = (
        (latest_close - highest_close)
        / highest_close
    )

    return {
        "Latest_Close": latest_close,
        "Historical_Highest_Close": highest_close,
        "Current_Drawdown": drawdown
    }

# Volatiltiy regime analysis
def analyze_volatility_regime(
    market_df,
    short_window=5,
    long_window=20
):
    """
    Compare short-term volatility with longer-term volatility
    to determine whether market variability is increasing,
    decreasing, or stable.
    """

    returns = market_df["Daily_Return"]

    short_volatility = (
        returns.rolling(short_window).std().iloc[-1]
    )

    long_volatility = (
        returns.rolling(long_window).std().iloc[-1]
    )

    if pd.isna(short_volatility) or pd.isna(long_volatility):
        regime = "Insufficient data"

    elif short_volatility > long_volatility * 1.2:
        regime = "Increasing volatility"

    elif short_volatility < long_volatility * 0.8:
        regime = "Decreasing volatility"

    else:
        regime = "Stable volatility"

    return {
        "Short_Term_Volatility": short_volatility,
        "Long_Term_Volatility": long_volatility,
        "Volatility_Regime": regime
    }

# Volume anomaly analysis
def analyze_volume_anomaly(
    market_df,
    window=20
):
    """
    Compare recent trading volume with its historical
    average and identify the strength of the volume activity.
    """

    recent_data = market_df.tail(window)

    latest_volume = recent_data.iloc[-1]["Volume"]

    average_volume = recent_data["Volume"].mean()

    volume_ratio = (
        latest_volume / average_volume
    )

    if volume_ratio >= 2:
        activity = "Very high volume"

    elif volume_ratio >= 1.5:
        activity = "High volume"

    elif volume_ratio >= 1.2:
        activity = "Above average volume"

    elif volume_ratio <= 0.8:
        activity = "Below average volume"

    else:
        activity = "Normal volume"

    return {
        "Latest_Volume": latest_volume,
        "Average_Volume": average_volume,
        "Volume_Ratio": volume_ratio,
        "Volume_Activity": activity
    }



# Price movement severity
def analyze_price_movement_severity(
    market_df
):
    """
    Compare the latest daily return with recent volatility
    to estimate how unusual today's movement is.
    """

    latest = market_df.iloc[-1]

    daily_return = latest["Daily_Return"]

    volatility = latest[
        "Rolling_Volatility_20D"
    ]

    if pd.isna(volatility) or volatility == 0:
        movement_multiple = None
        severity = "Insufficient data"

    else:
        movement_multiple = (
            abs(daily_return) / volatility
        )

        if movement_multiple >= 2:
            severity = "Very unusual movement"

        elif movement_multiple >= 1.5:
            severity = "Unusual movement"

        elif movement_multiple >= 1:
            severity = "Above typical movement"

        else:
            severity = "Within typical movement"

    return {
        "Daily_Return": daily_return,
        "Rolling_Volatility_20D": volatility,
        "Movement_Multiple": movement_multiple,
        "Movement_Severity": severity
    }

# Candle Analysis

def analyze_latest_candle(market_df):
    """
    Analyze the latest OHLC candle structure.
    """

    latest = market_df.iloc[-1]

    open_price = latest["Open"]
    high_price = latest["High"]
    low_price = latest["Low"]
    close_price = latest["Close"]

    total_range = high_price - low_price

    body_size = abs(
        close_price - open_price
    )

    upper_shadow = (
        high_price
        - max(open_price, close_price)
    )

    lower_shadow = (
        min(open_price, close_price)
        - low_price
    )

    if close_price > open_price:
        candle_direction = "Bullish"

    elif close_price < open_price:
        candle_direction = "Bearish"

    else:
        candle_direction = "Neutral"

    if total_range == 0:
        body_ratio = 0
    else:
        body_ratio = body_size / total_range

    return {
        "Open": open_price,
        "High": high_price,
        "Low": low_price,
        "Close": close_price,
        "Total_Range": total_range,
        "Body_Size": body_size,
        "Upper_Shadow": upper_shadow,
        "Lower_Shadow": lower_shadow,
        "Body_Ratio": body_ratio,
        "Candle_Direction": candle_direction
    }

# Support and resistance context

def analyze_price_levels(
    market_df,
    window=20
):
    """
    Identify simple recent support and resistance levels
    using the lowest low and highest high.
    """

    recent_data = market_df.tail(window)

    support = recent_data["Low"].min()

    resistance = recent_data["High"].max()

    latest_close = recent_data.iloc[-1]["Close"]

    distance_from_support = (
        (latest_close - support)
        / support
    )

    distance_from_resistance = (
        (resistance - latest_close)
        / resistance
    )

    return {
        "Support": support,
        "Resistance": resistance,
        "Latest_Close": latest_close,
        "Distance_From_Support": distance_from_support,
        "Distance_From_Resistance": distance_from_resistance
    }

# Test Analytics

if __name__ == "__main__":

    from src.analytics.analysis import get_market_data

    ticker_symbol = "IBM"

    market_df = get_market_data(
        ticker_symbol
    )

    if market_df is not None:
        print("ADVANCED MARKET ANALYSIS")

        print("\nMomentum:")
        print(
            analyze_momentum(market_df)
        )

        print("\nPrice Position:")
        print(
            analyze_price_position(market_df)
        )

        print("\nDrawdown:")
        print(
            analyze_drawdown(market_df)
        )

        print("\nVolatility Regime:")
        print(
            analyze_volatility_regime(market_df)
        )

        print("\nVolume Anomaly:")
        print(
            analyze_volume_anomaly(market_df)
        )

        print("\nPrice Movement Severity:")
        print(
            analyze_price_movement_severity(
                market_df
            )
        )

        print("\nLatest Candle:")
        print(
            analyze_latest_candle(market_df)
        )

        print("\nPrice Levels:")
        print(
            analyze_price_levels(market_df)
        )