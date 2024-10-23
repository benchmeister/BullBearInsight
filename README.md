# BullBearInsight

**BullBearInsight** is a Python-based stock market analysis tool that leverages **Prophet** and **Linear Regression** models to predict stock prices, track trends, and analyze market movements. With an interactive dashboard and multiple market indicators, this tool offers a comprehensive solution for both novice and expert users alike.

## Features
- **Interactive Dashboard**: Visualizes stock data and predictions in a user-friendly interface.
- **Market Indicators**: Includes RSI, Moving Averages, Bollinger Bands, and more.
- **Stock Price Prediction**: Utilizes Prophet and Linear Regression for next-day price forecasting.
- **Data Visualization**: Provides insightful graphs for both historical and predicted data.
- **Backtesting Trading Strategies**: Allows users to evaluate trading strategies using past data.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Models Used](#models-used)
- [Dashboard Features](#dashboard-features)
- [Market Indicators](#market-indicators)
- [License](#license)
- [Contributors](#contributors)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/BullBearInsight.git
    cd BullBearInsight
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your API keys (e.g., Alpha Vantage, yfinance) in the `.env` file:
    ```bash
    API_KEY=<your_alpha_vantage_api_key>
    ```

## Usage

To start the analysis and access the interactive dashboard on your browser:
```bash
python main.py
