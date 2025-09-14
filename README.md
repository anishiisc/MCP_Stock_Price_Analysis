# 📈 MCP Stock Server - Complete Guide

**Understanding Model Context Protocol (MCP) through a Stock Price Server Example**

*Created by Dr. Anish Roychowdhury, Plaksha University*

## 🎯 What You'll Learn

This comprehensive tutorial teaches you how to build MCP servers by creating a stock price analysis server. You'll understand:

- How MCP servers bridge AI models and external data sources
- The relationship between tools, resources, and business logic
- Error handling, caching, and security best practices
- Testing and debugging MCP servers
- Real-world deployment considerations

## 📋 Prerequisites

- Python 3.8 or higher
- Basic understanding of async/await in Python
- Familiarity with APIs and JSON

## 🚀 Quick Start

### 1. Setup and Installation

```bash
# Clone or download all the files
# Run the automated setup
python setup_and_test.py

# This will:
# ✅ Install all required packages
# ✅ Verify your Python environment  
# ✅ Test Yahoo Finance connectivity
# ✅ Create configuration files
```

### 2. Start the MCP Server

```bash
# Start the server (runs on stdin/stdout by default)
python stock_server.py
```

### 3. Test with the Example Client

```bash
# Run automated demo
python example_client.py

# Run interactive mode
python example_client.py interactive
```

## 📁 Project Structure

```
mcp_stock_project/
├── 📄 stock_server.py              # Main MCP server implementation
├── 📄 example_client.py            # Test client with examples
├── 📄 setup_and_test.py           # Automated setup and verification
├── 📄 debug_and_troubleshoot.py   # Debugging utilities
├── 📄 requirements.txt            # Python dependencies
├── 📄 test_config.json           # Test configuration (auto-generated)
├── 📄 USAGE.md                   # Usage examples (auto-generated)
├── 📄 README.md                  # This file
└── 📄 mcp_guide.tex              # Comprehensive LaTeX guide
```

## 🔧 Available Tools

### 1. `get_stock_data`
Fetches historical stock data and calculates key statistics.

**Parameters:**
- `ticker`: Stock symbol (e.g., 'AAPL', 'GOOGL')
- `name`: Descriptive name for analysis
- `start_date`: Start date in mmddyyyy format
- `end_date`: End date in mmddyyyy format

**Example:**
```json
{
  "ticker": "AAPL",
  "name": "Apple Analysis", 
  "start_date": "01012024",
  "end_date": "12312024"
}
```

### 2. `plot_stock_price`
Generates stock price charts with volume data.

**Returns:** Base64 encoded PNG image

### 3. `compare_stocks`
Compares performance between two stocks over a time period.

**Example:**
```json
{
  "ticker1": "AAPL",
  "ticker2": "GOOGL",
  "start_date": "01012024", 
  "end_date": "12312024"
}
```

## 📊 Understanding the MCP Architecture

### The Tool Chain Flow

```
AI Client Request → MCP Server Tool → Yahoo Finance API → Data Processing → Response
```

### Key Components Explained

1. **MCP Tools** (`@mcp.tool()` decorators)
   - Act as interfaces between AI and external systems
   - Handle input validation and error management
   - Return structured JSON responses

2. **Business Logic** (data processing functions)
   - Parse and validate inputs (dates, ticker symbols)
   - Fetch data from Yahoo Finance
   - Calculate statistics and generate insights

3. **Resources** (`@mcp.resource()` decorators)  
   - Provide read-only access to data
   - Example: `stock://data/AAPL` for company information

## 🛠️ Debugging and Troubleshooting

### Run Comprehensive Tests

```bash
# Test all components
python debug_and_troubleshoot.py

# This checks:
# ✅ All package imports
# ✅ Yahoo Finance connectivity
# ✅ Date parsing functions
# ✅ Matplotlib chart generation
# ✅ MCP server startup
# ✅ JSON-RPC communication
```

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `ImportError: fastmcp` | Package not installed | `pip install fastmcp` |
| `No data returned` | Invalid ticker or date range | Check ticker symbol and dates |
| `Rate limiting errors` | Too many API calls | Add delays between calls |
| `Plot generation fails` | Matplotlib backend issues | Use `matplotlib.use('Agg')` |

## 🔍 Detailed Code Walkthrough

### How `get_stock_data` Works

1. **Input Validation**
   ```python
   # Convert mmddyyyy to yyyy-mm-dd
   start_formatted = parse_date(start_date)
   ```

2. **Data Fetching**
   ```python
   stock = yf.Ticker(ticker)
   data = stock.history(start=start_formatted, end=end_formatted)
   ```

3. **Statistical Analysis**
   ```python
   stats = {
       "opening_price": round(data['Open'].iloc[0], 2),
       "closing_price": round(data['Close'].iloc[-1], 2),
       "percentage_change": round(((data['Close'].iloc[-1] / data['Open'].iloc[0]) - 1) * 100, 2)
   }
   ```

### Comparison with Account Server Example

| Aspect | Stock Server | Account Server |
|--------|-------------|----------------|
| **State** | Stateless (no persistence) | Stateful (database) |
| **Data Source** | Yahoo Finance API | Internal database |
| **Operations** | Read-only queries | CRUD operations |
| **Complexity** | Medium (data processing) | High (business logic) |

## 🎓 Learning Path

### Beginner Level
1. Run the setup and test scripts
2. Understand the basic tool definitions
3. Test with the example client
4. Read the generated LaTeX guide

### Intermediate Level  
1. Modify existing tools to add new statistics
2. Add input validation and error handling
3. Implement simple caching mechanisms
4. Create new tools for different financial data

### Advanced Level
1. Add authentication and rate limiting
2. Implement comprehensive logging
3. Build a stateful server with database persistence
4. Deploy to production with monitoring

## 📚 Additional Resources

### Generated Documentation
- `mcp_guide.pdf` - Comprehensive visual guide (compile from LaTeX)
- `USAGE.md` - Command examples and JSON-RPC samples
- `debug_report.json` - Detailed test results

### Key Concepts to Master
- **JSON-RPC Communication** - How MCP uses this protocol
- **Async Programming** - Understanding async/await patterns
- **Error Handling** - Graceful failure and recovery
- **Data Validation** - Input sanitization and validation
- **API Rate Limiting** - Handling external API constraints

## 🔐 Security Considerations

### Input Validation
```python
# Always validate and sanitize inputs
def validate_ticker(ticker: str) -> bool:
    return bool(re.match(r'^[A-Z0-9]{1,5}$', ticker.upper()))
```

### Rate Limiting
```python
# Implement delays between API calls
@rate_limit(0.5)  # Max 1 call per 2 seconds
def get_stock_data(ticker):
    # API call here
```

## 🚀 Next Steps

1. **Extend the Server**
   - Add more financial indicators (RSI, MACD, etc.)
   - Implement portfolio analysis tools
   - Add cryptocurrency support

2. **Improve Architecture**
   - Add database caching layer
   - Implement user authentication
   - Add request/response logging

3. **Production Deployment**
   - Containerize with Docker
   - Set up monitoring and alerting
   - Implement proper configuration management

## ❓ FAQ

**Q: Why use MCP instead of a regular API?**
A: MCP provides a standardized way for AI models to discover and use tools, with built-in support for type safety, documentation, and error handling.

**Q: Can I modify the date format?**
A: Yes! The `parse_date` function can be modified to accept different formats. The current mmddyyyy format is just an example.

**Q: How do I add authentication?**
A: You can add API key validation in the tool functions or implement OAuth2 flows for more complex authentication.

**Q: Can this work with other data sources?**
A: Absolutely! Replace the Yahoo Finance calls with any other financial data API (Alpha Vantage, IEX Cloud, etc.).

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new financial analysis tools
- Improve error handling and validation
- Create additional test cases
- Enhance the documentation

## 📄 License

This educational material is provided as-is for learning purposes. The Yahoo Finance data is subject to their terms of service.

---

**Created by Dr. Anish Roychowdhury, Plaksha University**

*This tutorial demonstrates MCP server development through practical, hands-on examples. The goal is to understand the underlying concepts that apply to any MCP server implementation.*
