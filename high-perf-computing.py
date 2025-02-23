import time
import random
from functools import lru_cache

# Simulated stock price API call (instead of real API)
# This method can be expanded and real api can be integreated
#Simulates fetching real-time stock price with random fluctuations.
def fetch_stock_price(stock: str):
    time.sleep(0.5)  # Simulate network delay
    return round(random.uniform(100, 500), 2)
    # could replace with actual API to the STOCK data.


# Lookup table for caching recent stock prices
stock_price_lookup_table = {}

def get_stock_price(stock: str):
    #Retrieve stock price with lookup table to avoid redundant API calls.
    if stock in stock_price_lookup_table:
        return stock_price_lookup_table[stock]
    price = fetch_stock_price(stock)
    stock_price_lookup_table[stock] = price  # Store in lookup table
    return price

# Memoization for Moving Average calculations
moving_avg_cache = {}

def moving_average(stock: str, days: int):
    #Computes simple moving average with memoization to avoid recomputation.
    if (stock, days) in moving_avg_cache:
        return moving_avg_cache[(stock, days)]
    
    prices = [get_stock_price(stock) for _ in range(days)]  # Simulated past prices
    avg = sum(prices) / days
    moving_avg_cache[(stock, days)] = avg  # Store result
    return avg

# Caching RSI(Relative Strength Index) using LRU Cache
#LRU caching is supported by python itself.
@lru_cache(maxsize=100)
def calculate_rsi(stock: str, period: int = 14):
    """Computes RSI using cached values for performance."""
    prices = [get_stock_price(stock) for _ in range(period)]
    
    gains = [max(0, prices[i] - prices[i-1]) for i in range(1, len(prices))]
    losses = [max(0, prices[i-1] - prices[i]) for i in range(1, len(prices))]
    
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    
    if avg_loss == 0:
        return 100  # RSI is maxed out
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

#Run tests
if __name__ == "__main__":
    stock_symbol = "Google"
    print(f"Fetching stock price for {stock_symbol}: {get_stock_price(stock_symbol)}")
    print(f"10-day Moving Average for {stock_symbol}: {moving_average(stock_symbol, 10)}")
    print(f"RSI for {stock_symbol}: {calculate_rsi(stock_symbol, 14)}")
