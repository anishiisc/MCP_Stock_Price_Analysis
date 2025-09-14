from mcp.server.fastmcp import FastMCP
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import io
import base64

mcp = FastMCP("stock_server")

def parse_date(date_str: str) -> str:
    """Convert mmddyyyy format to yyyy-mm-dd format for yfinance"""
    try:
        # Parse mmddyyyy format
        month = date_str[:2]
        day = date_str[2:4]
        year = date_str[4:]
        
        # Convert to datetime to validate
        dt = datetime(int(year), int(month), int(day))
        
        # Return in yyyy-mm-dd format
        return dt.strftime('%Y-%m-%d')
    except (ValueError, IndexError):
        raise ValueError(f"Invalid date format: {date_str}. Expected mmddyyyy format.")

@mcp.tool()
async def get_stock_data(ticker: str, name: str, start_date: str, end_date: str) -> dict:
    """Fetch stock price data from Yahoo Finance.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        name: A descriptive name for the stock/analysis
        start_date: Start date in mmddyyyy format (e.g., '01012023')
        end_date: End date in mmddyyyy format (e.g., '12312023')
    
    Returns:
        Dictionary containing stock data and basic statistics
    """
    try:
        # Parse dates
        start_formatted = parse_date(start_date)
        end_formatted = parse_date(end_date)
        
        # Fetch data from Yahoo Finance
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_formatted, end=end_formatted)
        
        if data.empty:
            return {
                "error": f"No data found for ticker {ticker} in the specified date range",
                "ticker": ticker,
                "name": name
            }
        
        # Calculate basic statistics
        stats = {
            "ticker": ticker,
            "name": name,
            "start_date": start_formatted,
            "end_date": end_formatted,
            "data_points": len(data),
            "opening_price": round(data['Open'].iloc[0], 2),
            "closing_price": round(data['Close'].iloc[-1], 2),
            "highest_price": round(data['High'].max(), 2),
            "lowest_price": round(data['Low'].min(), 2),
            "average_price": round(data['Close'].mean(), 2),
            "price_change": round(data['Close'].iloc[-1] - data['Open'].iloc[0], 2),
            "percentage_change": round(((data['Close'].iloc[-1] / data['Open'].iloc[0]) - 1) * 100, 2),
            "average_volume": int(data['Volume'].mean())
        }
        
        return stats
        
    except Exception as e:
        return {
            "error": f"Failed to fetch data: {str(e)}",
            "ticker": ticker,
            "name": name
        }

@mcp.tool()
async def plot_stock_price(ticker: str, name: str, start_date: str, end_date: str) -> str:
    """Create a plot of stock prices and return as base64 encoded image.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        name: A descriptive name for the stock/analysis
        start_date: Start date in mmddyyyy format (e.g., '01012023')
        end_date: End date in mmddyyyy format (e.g., '12312023')
    
    Returns:
        Base64 encoded PNG image of the stock price plot
    """
    try:
        # Parse dates
        start_formatted = parse_date(start_date)
        end_formatted = parse_date(end_date)
        
        # Fetch data
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_formatted, end=end_formatted)
        
        if data.empty:
            return f"No data found for ticker {ticker} in the specified date range"
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        
        # Plot closing price
        plt.subplot(2, 1, 1)
        plt.plot(data.index, data['Close'], linewidth=2, color='blue', label='Close Price')
        plt.plot(data.index, data['Open'], linewidth=1, color='green', alpha=0.7, label='Open Price')
        plt.title(f'{name} ({ticker}) - Stock Price Chart\n{start_formatted} to {end_formatted}', 
                 fontsize=14, fontweight='bold')
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot volume
        plt.subplot(2, 1, 2)
        plt.bar(data.index, data['Volume'], alpha=0.6, color='orange', label='Volume')
        plt.title('Trading Volume', fontsize=12, fontweight='bold')
        plt.ylabel('Volume', fontsize=12)
        plt.xlabel('Date', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{plot_base64}"
        
    except Exception as e:
        return f"Failed to create plot: {str(e)}"

@mcp.tool()
async def compare_stocks(ticker1: str, ticker2: str, start_date: str, end_date: str) -> dict:
    """Compare two stocks over a given period.
    
    Args:
        ticker1: First stock ticker symbol
        ticker2: Second stock ticker symbol  
        start_date: Start date in mmddyyyy format
        end_date: End date in mmddyyyy format
    
    Returns:
        Comparison data for both stocks
    """
    try:
        # Get data for both stocks
        stock1_data = await get_stock_data(ticker1, ticker1, start_date, end_date)
        stock2_data = await get_stock_data(ticker2, ticker2, start_date, end_date)
        
        if 'error' in stock1_data or 'error' in stock2_data:
            return {
                "error": "Failed to get data for one or both stocks",
                "stock1_error": stock1_data.get('error', 'No error'),
                "stock2_error": stock2_data.get('error', 'No error')
            }
        
        comparison = {
            "comparison_period": f"{parse_date(start_date)} to {parse_date(end_date)}",
            "stock1": {
                "ticker": ticker1,
                "percentage_change": stock1_data['percentage_change'],
                "price_change": stock1_data['price_change'],
                "final_price": stock1_data['closing_price']
            },
            "stock2": {
                "ticker": ticker2,
                "percentage_change": stock2_data['percentage_change'],
                "price_change": stock2_data['price_change'],
                "final_price": stock2_data['closing_price']
            }
        }
        
        # Determine winner
        if stock1_data['percentage_change'] > stock2_data['percentage_change']:
            comparison['better_performer'] = ticker1
            comparison['performance_difference'] = round(
                stock1_data['percentage_change'] - stock2_data['percentage_change'], 2
            )
        else:
            comparison['better_performer'] = ticker2
            comparison['performance_difference'] = round(
                stock2_data['percentage_change'] - stock1_data['percentage_change'], 2
            )
        
        return comparison
        
    except Exception as e:
        return {"error": f"Comparison failed: {str(e)}"}

@mcp.resource("stock://data/{ticker}")
async def read_stock_resource(ticker: str) -> str:
    """Resource endpoint to get current stock information"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return f"""
Stock Information for {ticker}:
Company Name: {info.get('longName', 'N/A')}
Sector: {info.get('sector', 'N/A')}
Industry: {info.get('industry', 'N/A')}
Current Price: ${info.get('currentPrice', 'N/A')}
Market Cap: ${info.get('marketCap', 'N/A'):,}
52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}
52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}
        """
    except Exception as e:
        return f"Error fetching stock resource: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')