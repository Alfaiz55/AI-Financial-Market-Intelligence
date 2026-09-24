# AI-Powered Financial Market Intelligence Platform

An AI-powered financial market analysis application that combines market data, financial news, quantitative analysis, and an LLM-powered agent to answer natural-language questions about stocks.

## Overview

The application collects market and financial news data through APIs, processes the data with Python and Pandas, stores it in SQLite, performs financial analysis, and uses a Gemini-powered AI agent with tool calling to answer user questions.

Instead of only displaying stock prices and charts, the system is designed to answer questions such as:

- What is the latest price of a stock?
- What was the recent average return?
- How unusual was the recent volume?
- What is the current volatility?
- What happened to the stock recently?
- What relevant news was published around a significant market movement?

## Key Features

- Market data ingestion using Alpha Vantage API
- Financial news and sentiment analysis
- Data processing and analysis using Pandas and NumPy
- Daily return and rolling volatility analysis
- 20-day moving average analysis
- Average volume and volume ratio analysis
- Momentum and price-position analysis
- Drawdown and volatility-regime analysis
- Volume anomaly and price-movement analysis
- Market-news relationship analysis
- Gemini LLM integration
- AI agent with function/tool calling
- Natural-language financial queries
- SQLite database storage
- User-facing Python interface
- Environment-variable based API key management

## Technology Stack

- **Python** — Core application development
- **Pandas** — Data processing and financial analysis
- **NumPy** — Numerical calculations
- **Requests** — REST API integration
- **SQLite** — Local database storage
- **Google Gemini API** — LLM-powered market explanations
- **Alpha Vantage API** — Market data and financial news
- **python-dotenv** — Environment variable and API key management
- **Tkinter** — User interface
- **Git & GitHub** — Version control and project hosting

## Architecture

```text
User
  ↓
Python UI
  ↓
AI Agent
  ↓
Gemini LLM
  ↓
Financial Tools
  ├── Market Data
  ├── Financial News
  ├── Financial Analytics
  ├── Advanced Analysis
  └── Market-News Timing Analysis
  ↓
SQLite Database
  ↓
Alpha Vantage APIs
```

## Project Structure

```text
AI-Financial-Market-Intelligence/
│
├── app/
│   └── app.py
│
├── src/
│   ├── ai/
│   │   ├── agent.py
│   │   ├── llm.py
│   │   └── tools.py
│   │
│   ├── analytics/
│   │   ├── analysis.py
│   │   └── analysis2.py
│   │
│   ├── api/
│   │   ├── market_api.py
│   │   └── news_api.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── data/
│   └── config.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Future Enhancements

- More historical market data
- Specialized ML models for market prediction
- Additional financial indicators
- More news and sentiment analysis
- Web-based interface
- Deployment
- Improved conversation history
