import requests
from bs4 import BeautifulSoup
import json
import time

# Define tickers by domain and size category
tickers = {
    "YahooFinance": {
        "large": ["AAPL", "MSFT", "GOOGL"],        # Large-cap companies
        "mid": ["NVDA", "PYPL", "NFLX"],           # Mid-cap companies
        "small": ["PLTR", "FSLY", "DOCU"],         # Small-cap companies
        "startup": ["SNAP", "UBER", "ZM"]          # Startup companies
    },
    "Morningstar": {
        "large": ["BRK.B", "XOM", "CVX"],
        "mid": ["MRK", "IBM", "HON"],
        "small": ["RKT", "GME", "DKNG"],
        "startup": ["TSLA", "SPCE", "BYND"]
    },
    "Nasdaq": {
        "large": ["AMZN", "TSLA", "FB"],
        "mid": ["SQ", "ROKU", "SPOT"],
        "small": ["CRWD", "ZS", "MDB"],
        "startup": ["ASAN", "BILL", "LYFT"]
    }
}

# Function to scrape Yahoo Finance
def scrape_yahoo_finance(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/sustainability"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    esg_data = {"ticker": ticker, "esg_score": None}
    esg_score = soup.find('div', {'data-test': 'esg-score'})
    if esg_score:
        esg_data["esg_score"] = esg_score.text.strip()
    return esg_data

# Function to scrape Morningstar
def scrape_morningstar(ticker):
    url = f"https://www.morningstar.com/stocks/xnas/{ticker}/quote"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    esg_data = {"ticker": ticker, "esg_risk_score": None}
    esg_score = soup.find('span', class_='esg-risk-score')
    if esg_score:
        esg_data["esg_risk_score"] = esg_score.text.strip()
    return esg_data

# Function to scrape Nasdaq
def scrape_nasdaq(ticker):
    url = f"https://www.nasdaq.com/market-activity/stocks/{ticker}/sustainability"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    esg_data = {"ticker": ticker, "sustainability_score": None}
    sustainability_score = soup.find('div', {'class': 'sustainability-score'})
    if sustainability_score:
        esg_data["sustainability_score"] = sustainability_score.text.strip()
    return esg_data

# Main function to scrape data and save to JSON
def scrape_all_data():
    all_data = {}

    # Scrape Yahoo Finance data
    all_data["YahooFinance"] = {}
    for size, size_tickers in tickers["YahooFinance"].items():
        all_data["YahooFinance"][size] = []
        for ticker in size_tickers:
            print(f"Scraping Yahoo Finance for {ticker}")
            data = scrape_yahoo_finance(ticker)
            all_data["YahooFinance"][size].append(data)
            time.sleep(2)  # Rate limiting

    # Scrape Morningstar data
    all_data["Morningstar"] = {}
    for size, size_tickers in tickers["Morningstar"].items():
        all_data["Morningstar"][size] = []
        for ticker in size_tickers:
            print(f"Scraping Morningstar for {ticker}")
            data = scrape_morningstar(ticker)
            all_data["Morningstar"][size].append(data)
            time.sleep(2)  # Rate limiting

    # Scrape Nasdaq data
    all_data["Nasdaq"] = {}
    for size, size_tickers in tickers["Nasdaq"].items():
        all_data["Nasdaq"][size] = []
        for ticker in size_tickers:
            print(f"Scraping Nasdaq for {ticker}")
            data = scrape_nasdaq(ticker)
            all_data["Nasdaq"][size].append(data)
            time.sleep(2)  # Rate limiting

    # Save data to JSON
    with open("esg_data.json", "w") as f:
        json.dump(all_data, f, indent=4)
    print("Data saved to esg_data.json")

# Run the scraping function
scrape_all_data()
