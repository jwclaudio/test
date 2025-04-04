from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def format_currency(value):
    """Format large numbers into readable currency values with B/M suffixes"""
    if value >= 1_000_000_000:  # Billion
        return f"{value/1_000_000_000:.1f}B"
    elif value >= 1_000_000:  # Million
        return f"{value/1_000_000:.1f}M"
    else:
        return f"{value:,.0f}"

def get_historical_data(symbols, period='1y'):
    """Fetch historical data for given symbols"""
    data = pd.DataFrame()
    valid_symbols = []
    
    for symbol in symbols:
        try:
            logger.debug(f"Fetching data for symbol: {symbol}")
            # Clean the symbol (remove any spaces and convert to uppercase)
            symbol = symbol.strip().upper()
            
            # Handle common ETF suffixes
            if not symbol.endswith(('.US', '.TO', '.L', '.HK')):
                # Try common ETF suffixes if the symbol doesn't have one
                suffixes = ['', '.US', '.TO', '.L', '.HK']
                symbol_found = False
                
                for suffix in suffixes:
                    try:
                        test_symbol = symbol + suffix
                        logger.debug(f"Trying symbol with suffix: {test_symbol}")
                        ticker = yf.Ticker(test_symbol)
                        info = ticker.info
                        
                        if info and 'regularMarketPrice' in info:
                            symbol = test_symbol
                            symbol_found = True
                            logger.debug(f"Found valid symbol: {symbol}")
                            break
                    except Exception as e:
                        logger.debug(f"Failed with suffix {suffix}: {str(e)}")
                        continue
                
                if not symbol_found:
                    logger.error(f"Symbol {symbol} not found with any common suffix")
                    continue
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info or 'regularMarketPrice' not in info:
                logger.error(f"Symbol {symbol} not found or has no market data")
                continue
                
            hist = ticker.history(period=period)
            if hist.empty:
                logger.error(f"No historical data found for symbol: {symbol}")
                continue
                
            data[symbol] = hist['Close']
            valid_symbols.append(symbol)
            logger.debug(f"Successfully fetched data for {symbol}")
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            continue
    
    if not valid_symbols:
        raise ValueError("No valid symbols found. Please check the ETF symbols and try again. Common ETF symbols include: SPY, VOO, QQQ, VTI, BND")
        
    return data

def calculate_portfolio_metrics(returns, weights):
    """Calculate portfolio metrics (return, risk)"""
    try:
        portfolio_return = np.sum(returns.mean() * weights) * 252
        portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        return portfolio_return, portfolio_risk
    except Exception as e:
        logger.error(f"Error calculating portfolio metrics: {str(e)}")
        raise

def optimize_portfolio(returns, num_portfolios=1000):
    """Generate efficient frontier"""
    try:
        num_assets = len(returns.columns)
        results = []
        
        for _ in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            portfolio_return, portfolio_risk = calculate_portfolio_metrics(returns, weights)
            results.append({
                'weights': weights,
                'return': portfolio_return,
                'risk': portfolio_risk,
                'sharpe': portfolio_return / portfolio_risk if portfolio_risk != 0 else 0
            })
        
        return pd.DataFrame(results)
    except Exception as e:
        logger.error(f"Error in portfolio optimization: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('pages/home/home.html')

@app.route('/portfolio')
def portfolio():
    return render_template('pages/portfolio_optimizer/portfolio.html')

@app.route('/education')
def education():
    return render_template('pages/education/education.html')

@app.route('/about')
def about():
    return render_template('pages/about_us/about.html')

@app.route('/screener')
def screener():
    return render_template('pages/etf_screener/screener.html')

if __name__ == '__main__':
    app.run(debug=True)