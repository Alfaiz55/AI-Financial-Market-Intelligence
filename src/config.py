import os
from dotenv import load_dotenv

load_dotenv()

alpha_vantage_key=os.getenv("ALPHA_VANTAGE_API_KEY")
gemini_key= os.getenv("GEMINI_API_KEY")

print("Alpha Vantage key loaded:",bool(alpha_vantage_key))
print("Gemini key loaded:",bool(gemini_key))