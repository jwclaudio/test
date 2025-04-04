# Portfolio Optimizer

A web application that helps users optimize their investment portfolio using the efficient frontier model. The application allows users to input ETF symbols and provides portfolio optimization recommendations based on historical data.

## Features

- Input multiple ETF symbols
- Real-time portfolio optimization
- Efficient frontier visualization
- Optimal portfolio weights calculation
- Key portfolio metrics (Expected Return, Risk, Sharpe Ratio)
- Modern and responsive UI

## Setup

1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter ETF symbols in the input field (e.g., SPY, VOO, QQQ)
2. Click "Add ETF" or press Enter to add each ETF
3. The application will automatically calculate and display:
   - The efficient frontier plot
   - Optimal portfolio weights
   - Key portfolio metrics
4. Remove ETFs by clicking the X button on their tags

## Example ETF Symbols

- SPY (S&P 500 ETF)
- VOO (Vanguard S&P 500 ETF)
- QQQ (NASDAQ 100 ETF)
- VTI (Vanguard Total Stock Market ETF)
- BND (Vanguard Total Bond Market ETF)

## Technical Details

The application uses:
- Flask for the backend
- yfinance for fetching financial data
- pandas and numpy for calculations
- scipy for optimization
- plotly for interactive visualizations
- Bootstrap for responsive design

## Note

This application is for educational purposes only. Always do your own research and consider consulting with financial advisors before making investment decisions. 