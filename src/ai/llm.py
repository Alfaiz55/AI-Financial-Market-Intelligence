import os
import json
import time

from dotenv import load_dotenv
from google import genai

from src.analytics.analysis import (
    create_market_analysis,
    prepare_llm_context
)


# --------------------------------------------------
# Environment and Gemini client
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )

client = genai.Client(api_key=api_key)


# Gemini models to try in order
MODEL_NAMES = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]


# --------------------------------------------------
# Gemini market explanation
# --------------------------------------------------

def generate_market_explanation(llm_context):
    """
    Send structured market analysis to Gemini
    and generate a human-readable explanation.
    """

    system_instruction = """
You are a financial market analysis assistant.

Your job is to explain market data using ONLY the
evidence provided by the application.

Do not invent facts, prices, news, causes, or events.

Clearly distinguish between:
- observed market data
- news information
- possible explanations

Do not claim that a news article caused a price movement
unless the provided evidence establishes causation.

Do not provide financial advice or tell the user to buy,
sell, or hold a security.

Explain the market situation clearly for a general user.
"""

    prompt = f"""
Analyze the following market information for the user.

Market analysis data:

{json.dumps(llm_context, indent=2)}

Provide a concise explanation containing:

1. Market Summary
2. What happened to the price
3. Volatility and volume context
4. Recent performance
5. Relevant news context
6. Important observations and uncertainty

Use percentages where appropriate.

Remember:
- The data represents observations, not guaranteed causes.
- Do not give buy/sell/hold recommendations.
- Do not invent information that is not present in the data.
"""

    # Try each configured Gemini model
    for model_name in MODEL_NAMES:

        max_retries = 3

        # Retry the current model if it temporarily returns 503
        for attempt in range(max_retries):

            try:

                print(
                    f"Trying Gemini model: {model_name}"
                )

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "system_instruction": system_instruction
                    }
                )

                return response.text

            except Exception as error:

                error_message = str(error)

                # Temporary Gemini server unavailability
                if "503" in error_message:

                    if attempt < max_retries - 1:

                        wait_time = 2 ** attempt

                        print(
                            f"{model_name} temporarily unavailable. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)

                    else:

                        print(
                            f"{model_name} unavailable after "
                            f"{max_retries} attempts."
                        )

                # Any other error should not be silently ignored
                else:
                    raise

        # Move to the next model after retries are exhausted
        print(
            f"Trying the next Gemini model..."
        )

    raise RuntimeError(
        "All configured Gemini models are currently unavailable."
    )


# --------------------------------------------------
# Main test
# --------------------------------------------------

if __name__ == "__main__":

    ticker_symbol = "IBM"

    # Get analysis from the database
    analysis = create_market_analysis(ticker_symbol)

    if analysis is not None:

        # Convert Pandas/NumPy values into clean Python types
        llm_context = prepare_llm_context(analysis)

        # Send real project analysis to Gemini
        explanation = generate_market_explanation(
            llm_context
        )

        print("\n" + "=" * 60)
        print(
            f"GEMINI MARKET EXPLANATION: {ticker_symbol}"
        )
        print("=" * 60)

        print(explanation)