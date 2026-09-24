import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.ai.tools import (
    get_market_analysis_tool,
    get_advanced_analysis_tool,
    get_market_news_timing_tool,
    query_market_data_tool,
    

    get_latest_price_tool,
    get_average_price_tool,
    get_moving_average_tool,

    get_latest_return_tool,
    get_average_return_tool,

    get_latest_volume_tool,
    get_average_volume_tool,

    get_volatility_tool
)

# Environment

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )

# Gemini Client

client = genai.Client(
    api_key=api_key
)

# Available Python Tools

available_functions = {

    # Existing analysis tools
    "get_market_analysis": get_market_analysis_tool,
    "get_advanced_analysis": get_advanced_analysis_tool,
    "get_market_news_timing": get_market_news_timing_tool,

    # Generic market-data tools
    "query_market_data": query_market_data_tool,
    

    # Price tools
    "get_latest_price": get_latest_price_tool,
    "get_average_price": get_average_price_tool,
    "get_moving_average": get_moving_average_tool,

    # Return tools
    "get_latest_return": get_latest_return_tool,
    "get_average_return": get_average_return_tool,

    # Volume tools
    "get_latest_volume": get_latest_volume_tool,
    "get_average_volume": get_average_volume_tool,

    # Risk / volatility
    "get_volatility": get_volatility_tool
}


# Function Declarations

market_analysis_declaration = {
    "name": "get_market_analysis",
    "description": (
        "Gets the main financial market analysis for a stock, "
        "including latest price, daily return, volatility, "
        "moving average, volume, trend, unusual movement, "
        "and financial news sentiment."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": (
                    "Stock ticker symbol, for example IBM."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
}


advanced_analysis_declaration = {
    "name": "get_advanced_analysis",
    "description": (
        "Performs advanced financial analysis including "
        "momentum, price position, drawdown, volatility "
        "regime, volume anomaly, price movement severity, "
        "latest candle analysis, and recent price levels."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": (
                    "Stock ticker symbol, for example IBM."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
}


market_news_timing_declaration = {
    "name": "get_market_news_timing",
    "description": (
        "Analyzes financial news published around the latest "
        "market date and identifies whether news occurred "
        "before market hours, during market hours, or after "
        "market hours."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": (
                    "Stock ticker symbol, for example IBM."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
}

query_market_data_declaration = types.FunctionDeclaration(
    name="query_market_data",
    description=(
        "Query specific market data fields for a stock from the database. "
        "Use this when the user asks for specific market values such as "
        "price, closing price, volume, return, volatility, moving average, "
        "or historical market data."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol, such as IBM or TSLA."
            },
            "fields": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": (
                    "Specific fields required to answer the user's question. "
                    "Available fields are: Date, Open, High, Low, Close, "
                    "Volume, Daily_Return, Average_Volume_20D, "
                    "Rolling_Volatility_20D, Moving_Average_20D, "
                    "Volume_Ratio."
                )
            },
            "start_date": {
                "type": "string",
                "description": "Optional start date in YYYY-MM-DD format."
            },
            "end_date": {
                "type": "string",
                "description": "Optional end date in YYYY-MM-DD format."
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of records to return."
            }
        },
        "required": ["ticker_symbol", "fields"]
    }
)


latest_price_declaration = types.FunctionDeclaration(
    name="get_latest_price",
    description="Get the latest available closing price for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol, such as IBM, MSFT, AMZN, or TSLA."
            }
        },
        "required": ["ticker_symbol"]
    }
)

# Price Tool Declarations

latest_price_declaration = types.FunctionDeclaration(
    name="get_latest_price",
    description=(
        "Get the latest available closing price for a stock."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": (
                    "Stock ticker symbol, such as "
                    "IBM, MSFT, AMZN, or TSLA."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
)

# Price Tool Declarations

latest_price_declaration = types.FunctionDeclaration(
    name="get_latest_price",
    description=(
        "Get the latest available closing price for a stock."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": (
                    "Stock ticker symbol, such as "
                    "IBM, MSFT, AMZN, or TSLA."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
)


average_price_declaration = types.FunctionDeclaration(
    name="get_average_price",
    description=(
        "Calculate the average closing price over a specified "
        "number of recent trading sessions."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol."
            },
            "window": {
                "type": "integer",
                "description": (
                    "Number of recent trading sessions to use "
                    "for calculating the average price."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
)


moving_average_declaration = types.FunctionDeclaration(
    name="get_moving_average",
    description=(
        "Get the latest moving average price for a stock."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol."
            },
            "window": {
                "type": "integer",
                "description": (
                    "Moving average window in trading sessions."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
)


# Return Tool Declarations

latest_return_declaration = types.FunctionDeclaration(
    name="get_latest_return",
    description=(
        "Get the latest daily return for a stock."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol."
            }
        },
        "required": ["ticker_symbol"]
    }
)


average_return_declaration = types.FunctionDeclaration(
    name="get_average_return",
    description=(
        "Calculate the average daily return over a specified "
        "number of recent trading sessions."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol."
            },
            "window": {
                "type": "integer",
                "description": (
                    "Number of recent trading sessions to use "
                    "for calculating the average daily return."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
)


# Volume Tool Declarations

latest_volume_declaration = types.FunctionDeclaration(
    name="get_latest_volume",
    description=(
        "Get the latest trading volume for a stock."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol."
            }
        },
        "required": ["ticker_symbol"]
    }
)


average_volume_declaration = types.FunctionDeclaration(
    name="get_average_volume",
    description=(
        "Calculate the average trading volume over a specified "
        "number of recent trading sessions."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol."
            },
            "window": {
                "type": "integer",
                "description": (
                    "Number of recent trading sessions to use "
                    "for calculating average volume."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
)


# Volatility Tool Declaration

volatility_declaration = types.FunctionDeclaration(
    name="get_volatility",
    description=(
        "Get the latest rolling volatility for a stock."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ticker_symbol": {
                "type": "string",
                "description": "Stock ticker symbol."
            },
            "window": {
                "type": "integer",
                "description": (
                    "Volatility window in trading sessions."
                )
            }
        },
        "required": ["ticker_symbol"]
    }
)


# Gemini Tool Configuration

tools = types.Tool(
    function_declarations=[
        # Existing analysis tools
        market_analysis_declaration,
        advanced_analysis_declaration,
        market_news_timing_declaration,

        # Generic market-data tools
        query_market_data_declaration,
        

        # Price tools
        latest_price_declaration,
        average_price_declaration,
        moving_average_declaration,

        # Return tools
        latest_return_declaration,
        average_return_declaration,

        # Volume tools
        latest_volume_declaration,
        average_volume_declaration,

        # Volatility tool
        volatility_declaration
    ]
)

# Gemini Tool Configuration

tools = types.Tool(
    function_declarations=[
        # Existing analysis tools
        market_analysis_declaration,
        advanced_analysis_declaration,
        market_news_timing_declaration,

        # Generic market-data tool
        query_market_data_declaration,

        # Price tools
        latest_price_declaration,
        average_price_declaration,
        moving_average_declaration,

        # Return tools
        latest_return_declaration,
        average_return_declaration,

        # Volume tools
        latest_volume_declaration,
        average_volume_declaration,

        # Volatility tool
        volatility_declaration
    ]
)

config = types.GenerateContentConfig(
    tools=[tools],

    system_instruction="""
You are an AI financial market analysis assistant.

Answer user questions using the financial tools provided by the application.

Use tools when actual market data or financial analysis is required.
Do not invent market data, prices, news, or events.
Use the ticker symbol provided by the user.

For simple factual market-data questions such as price, volume,
date, return, or another specific market field, use
query_market_data.

Once query_market_data provides enough information to answer the
question, answer immediately. Do not call another tool.

If the user asks for "yesterday" or "previous trading day",
return only the requested value for that trading session.

Use analysis tools such as get_market_analysis,
get_advanced_analysis, or get_market_news_timing when the user
explicitly asks for analysis, explanation, comparison, trend,
volatility, news context, or other additional analysis.

For questions requiring multiple pieces of analysis, you may use
multiple appropriate tools.

Answer only what the user asked for.

Clearly distinguish observed data from possible explanations.
Do not claim that news caused a price movement unless the
available evidence establishes that relationship.

Do not provide financial advice.
Do not tell the user to buy, sell, or hold a security.

Give clear explanations based only on the available evidence.
"""
)


# Execute Tool
def execute_tool(function_name, function_args):
    """
    Execute the Python function requested by Gemini.
    """

    if function_name not in available_functions:
        return {
            "success": False,
            "message": (
                f"Unknown function requested: {function_name}"
            )
        }

    function = available_functions[function_name]

    try:
        result = function(**function_args)

        return result

    except Exception as error:
        return {
            "success": False,
            "message": f"Tool execution failed: {str(error)}"
        }

# Agent
def generate_with_fallback(
    contents,
    model_name=None,
    config_override=None
):
    """
    Generate a Gemini response with retry and model fallback.

    If a model has already been selected, continue from that model
    and fall back to the next available model if necessary.
    """

    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash"
    ]

    # If a model was already selected, start from that model
    # instead of restarting from the first model.
    if model_name in models:
        start_index = models.index(model_name)
        models = models[start_index:]

    # Use the normal tool-enabled config unless
    # another config was explicitly provided.
    active_config = (
        config_override
        if config_override is not None
        else config
    )

    for current_model in models:

        for attempt in range(3):

            try:
                print(
                    f"\nGenerating response with: {current_model}"
                )

                response = client.models.generate_content(
                    model=current_model,
                    contents=contents,
                    config=active_config
                )

                return response, current_model

            except Exception as error:

                error_message = str(error)

                # Temporary server problem
                if "503" in error_message:

                    if attempt < 2:

                        wait_time = 2 ** attempt

                        print(
                            f"{current_model} unavailable. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)

                    else:

                        print(
                            f"{current_model} unavailable "
                            f"after 3 attempts."
                        )

                # Quota exceeded
                elif "429" in error_message:

                    print(
                        f"{current_model} quota exceeded. "
                        f"Moving to the next model..."
                    )

                    break

                else:
                    raise

    raise RuntimeError(
        "All configured Gemini models are currently unavailable "
        "or their quotas have been exceeded."
    )
    
def run_market_agent(user_question):
    """
    Send a user question to Gemini and allow Gemini
    to decide which financial tools should be called.
    """

    print("FINANCIAL INTELLIGENCE AGENT")

    print("\nUser question:")
    print(user_question)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=user_question
                )
            ]
        )
    ]

    # First Gemini request
    response, selected_model = generate_with_fallback(
        contents
    )

    # Tool-calling loop
    while response.function_calls:

        # Keep Gemini's function-call response
        contents.append(
            response.candidates[0].content
        )

        function_response_parts = []

        # Track whether this was a direct data-retrieval request
        data_tool_used = False

        for function_call in response.function_calls:

            function_name = function_call.name

            function_args = dict(
                function_call.args
            )

            print("\nGemini requested tool:")
            print(function_name)

            print("Arguments:")
            print(function_args)

            # Execute Python function
            result = execute_tool(
                function_name,
                function_args
            )

            print("\nTool executed successfully.")

            # These tools provide direct factual data.
            if function_name in {
                "query_market_data",
                "get_latest_price",
                "get_average_price",
                "get_moving_average",
                "get_latest_return",
                "get_average_return",
                "get_latest_volume",
                "get_average_volume",
                "get_volatility"
            }:
                data_tool_used = True

            function_response_parts.append(
                types.Part.from_function_response(
                    name=function_name,
                    response={
                        "result": result
                    }
                )
            )

        # Add tool results to conversation
        contents.append(
            types.Content(
                role="user",
                parts=function_response_parts
            )
        )

        # ----------------------------------------------------------
        # Direct data tool already provided the requested information.
        # Generate the final answer WITHOUT giving Gemini more tools.
        # ----------------------------------------------------------

        if data_tool_used:

            final_config = types.GenerateContentConfig(
                system_instruction="""
You are a financial market analysis assistant.

Use the tool result already provided in the conversation
to answer the user's original question.

Do not request another tool.

Do not add unrelated analysis.

Do not invent information.

Answer only what the user asked for.

Do not provide financial advice.
"""
            )

            print(
                "\nGenerating final answer without additional tools..."
            )

            response, selected_model = generate_with_fallback(
                contents,
                model_name=selected_model,
                config_override=final_config
            )

            return response.text

            
        

        # ----------------------------------------------------------
        # Analysis tools may require additional tool calls.
        # ----------------------------------------------------------

        response, selected_model = generate_with_fallback(
            contents,
            model_name=selected_model
        )

    return response.text

# Test
if __name__ == "__main__":
    
    print("FINANCIAL INTELLIGENCE AGENT")
    

    question = input("\nAsk your market question: ")

    answer = run_market_agent(question)

    
    print("FINAL AGENT ANSWER")

    print(answer)