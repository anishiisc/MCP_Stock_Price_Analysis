#!/usr/bin/env python3
"""
Setup and test script for the MCP Stock Server
This script helps with installation and verification
"""

import subprocess
import sys
import os
import json
from datetime import datetime, timedelta

def install_requirements():
    """Install required packages"""
    requirements = [
        "fastmcp==0.2.0",
        "yfinance>=0.2.28",
        "matplotlib>=3.8.0",
        "pandas>=2.1.0", 
        "numpy>=1.26.0"
    ]
    
    print("📦 Installing required packages...")
    for requirement in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"✅ Installed: {requirement}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install: {requirement}")
            return False
    
    print("✅ All packages installed successfully!")
    return True

def verify_installation():
    """Verify that all required packages are installed"""
    packages = ["mcp", "yfinance", "matplotlib", "pandas", "numpy"]
    
    print("\n🔍 Verifying installation...")
    all_good = True
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is NOT available")
            all_good = False
    
    return all_good

def create_test_config():
    """Create a test configuration file"""
    config = {
        "test_stocks": ["AAPL", "GOOGL", "MSFT", "TSLA"],
        "test_date_ranges": [
            {"start": "01012024", "end": "03312024", "name": "Q1 2024"},
            {"start": "01012023", "end": "12312023", "name": "Full Year 2023"}
        ],
        "server_config": {
            "transport": "stdio",
            "timeout": 30
        }
    }
    
    with open("test_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created test_config.json")

def run_basic_tests():
    """Run basic functionality tests"""
    print("\n🧪 Running basic tests...")
    
    # Test 1: Import test
    try:
        from datetime import datetime
        import yfinance as yf
        print("✅ Test 1: Imports successful")
    except Exception as e:
        print(f"❌ Test 1: Import failed - {e}")
        return False
    
    # Test 2: Yahoo Finance connectivity
    try:
        stock = yf.Ticker("AAPL")
        info = stock.info
        if info and 'longName' in info:
            print("✅ Test 2: Yahoo Finance connectivity working")
        else:
            print("⚠️ Test 2: Yahoo Finance connectivity limited")
    except Exception as e:
        print(f"❌ Test 2: Yahoo Finance failed - {e}")
    
    # Test 3: Date parsing
    try:
        from datetime import datetime
        test_date = "01152024"
        month = test_date[:2]
        day = test_date[2:4]
        year = test_date[4:]
        dt = datetime(int(year), int(month), int(day))
        formatted = dt.strftime('%Y-%m-%d')
        if formatted == "2024-01-15":
            print("✅ Test 3: Date parsing working")
        else:
            print("❌ Test 3: Date parsing failed")
    except Exception as e:
        print(f"❌ Test 3: Date parsing error - {e}")
    
    return True

def create_sample_usage():
    """Create sample usage documentation"""
    usage = """
# MCP Stock Server Usage Examples

## 1. Basic Usage
python stock_server.py

## 2. Test with client
python example_client.py

## 3. Interactive mode
python example_client.py interactive

## 4. Example tool calls:

### Get Stock Data
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_stock_data",
    "arguments": {
      "ticker": "AAPL",
      "name": "Apple Analysis",
      "start_date": "01012024",
      "end_date": "12312024"
    }
  }
}

### Compare Stocks
{
  "jsonrpc": "2.0", 
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "compare_stocks",
    "arguments": {
      "ticker1": "AAPL",
      "ticker2": "GOOGL",
      "start_date": "01012024",
      "end_date": "12312024"
    }
  }
}

### Read Resource
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/read",
  "params": {
    "uri": "stock://data/AAPL"
  }
}

## Date Format
- Input format: mmddyyyy (e.g., 01152024 for January 15, 2024)
- The server converts this to yyyy-mm-dd format internally

## Available Tools
1. get_stock_data - Get historical stock data with statistics
2. plot_stock_price - Generate stock price charts
3. compare_stocks - Compare performance between two stocks

## Available Resources  
- stock://data/{ticker} - Get current stock information
"""
    
    with open("USAGE.md", "w") as f:
        f.write(usage)
    
    print("✅ Created USAGE.md")

def main():
    """Main setup function"""
    print("🚀 MCP Stock Server Setup")
    print("=" * 40)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Installation failed. Please check your Python environment.")
        return False
    
    # Step 2: Verify installation
    if not verify_installation():
        print("❌ Verification failed. Some packages are missing.")
        return False
    
    # Step 3: Create test files
    create_test_config()
    create_sample_usage()
    
    # Step 4: Run basic tests
    if not run_basic_tests():
        print("❌ Basic tests failed.")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the server: python stock_server.py")
    print("2. Test with client: python example_client.py") 
    print("3. Interactive mode: python example_client.py interactive")
    print("4. Check USAGE.md for more examples")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
