#!/usr/bin/env python3
"""
Debugging and troubleshooting utilities for MCP Stock Server
This helps identify and fix common issues
"""

import json
import sys
import traceback
import asyncio
import subprocess
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MCPDebugger:
    """Debug utilities for MCP servers"""
    
    def __init__(self):
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_imports(self):
        """Test all required imports"""
        print("\n🔍 Testing Imports...")
        
        imports_to_test = [
            ("mcp.server.fastmcp", "FastMCP"),
            ("yfinance", "yf"),  
            ("matplotlib.pyplot", "plt"),
            ("pandas", "pd"),
            ("numpy", "np"),
            ("datetime", "datetime"),
            ("io", "io"),
            ("base64", "base64")
        ]
        
        for module, alias in imports_to_test:
            try:
                if alias == "yf":
                    import yfinance as yf
                elif alias == "plt":
                    import matplotlib.pyplot as plt
                elif alias == "pd":
                    import pandas as pd
                elif alias == "np":
                    import numpy as np
                else:
                    __import__(module)
                
                self.log_test(f"Import {module}", True)
            except ImportError as e:
                self.log_test(f"Import {module}", False, str(e))
            except Exception as e:
                self.log_test(f"Import {module}", False, f"Unexpected error: {str(e)}")
    
    def test_yahoo_finance(self):
        """Test Yahoo Finance connectivity and data fetching"""
        print("\n🌐 Testing Yahoo Finance...")
        
        try:
            import yfinance as yf
            
            # Test 1: Basic ticker creation
            ticker = yf.Ticker("AAPL")
            self.log_test("Yahoo Finance Ticker Creation", True)
            
            # Test 2: Get basic info
            try:
                info = ticker.info
                if info and len(info) > 0:
                    company_name = info.get('longName', 'Unknown')
                    self.log_test("Yahoo Finance Info Fetch", True, f"Company: {company_name}")
                else:
                    self.log_test("Yahoo Finance Info Fetch", False, "Empty info returned")
            except Exception as e:
                self.log_test("Yahoo Finance Info Fetch", False, str(e))
            
            # Test 3: Get historical data
            try:
                # Get last 5 days of data
                end_date = datetime.now()
                start_date = end_date - timedelta(days=10)  # 10 days to ensure we get some data
                
                data = ticker.history(start=start_date, end=end_date)
                if not data.empty:
                    self.log_test("Yahoo Finance Historical Data", True, 
                                f"Got {len(data)} data points")
                else:
                    self.log_test("Yahoo Finance Historical Data", False, "No historical data returned")
            except Exception as e:
                self.log_test("Yahoo Finance Historical Data", False, str(e))
                
        except ImportError:
            self.log_test("Yahoo Finance Import", False, "yfinance not installed")
        except Exception as e:
            self.log_test("Yahoo Finance General", False, str(e))
    
    def test_date_parsing(self):
        """Test date parsing functionality"""
        print("\n📅 Testing Date Parsing...")
        
        def parse_date(date_str: str) -> str:
            """Test version of date parsing"""
            try:
                month = date_str[:2]
                day = date_str[2:4]
                year = date_str[4:]
                dt = datetime(int(year), int(month), int(day))
                return dt.strftime('%Y-%m-%d')
            except Exception as e:
                raise ValueError(f"Invalid date format: {date_str}. Error: {str(e)}")
        
        test_cases = [
            ("01012024", "2024-01-01", "Valid date - Jan 1, 2024"),
            ("12312023", "2023-12-31", "Valid date - Dec 31, 2023"),
            ("02292024", "2024-02-29", "Leap year date"),
            ("13012024", None, "Invalid month"),
            ("01322024", None, "Invalid day"),  
            ("010124", None, "Wrong format - too short"),
            ("0101202", None, "Wrong format - too short"),
            ("abc12024", None, "Non-numeric input")
        ]
        
        for input_date, expected, description in test_cases:
            try:
                result = parse_date(input_date)
                if expected is None:
                    self.log_test(f"Date Parse: {description}", False, 
                                f"Should have failed but got: {result}")
                elif result == expected:
                    self.log_test(f"Date Parse: {description}", True)
                else:
                    self.log_test(f"Date Parse: {description}", False, 
                                f"Expected {expected}, got {result}")
            except Exception as e:
                if expected is None:
                    self.log_test(f"Date Parse: {description}", True, "Correctly failed")
                else:
                    self.log_test(f"Date Parse: {description}", False, str(e))
    
    def test_matplotlib(self):
        """Test matplotlib functionality"""
        print("\n📊 Testing Matplotlib...")
        
        try:
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            import matplotlib.pyplot as plt
            import numpy as np
            import io
            import base64
            
            # Create a simple test plot
            fig, ax = plt.subplots(figsize=(8, 6))
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            ax.plot(x, y)
            ax.set_title("Test Plot")
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            plot_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            if plot_base64 and len(plot_base64) > 100:
                self.log_test("Matplotlib Plot Generation", True, 
                            f"Generated {len(plot_base64)} chars of base64 data")
            else:
                self.log_test("Matplotlib Plot Generation", False, "Plot generation failed")
                
        except Exception as e:
            self.log_test("Matplotlib Test", False, str(e))
    
    async def test_mcp_server_startup(self, server_path="stock_server.py"):
        """Test MCP server startup"""
        print("\n🚀 Testing MCP Server Startup...")
        
        if not os.path.exists(server_path):
            self.log_test("MCP Server File Exists", False, f"{server_path} not found")
            return
        
        self.log_test("MCP Server File Exists", True)
        
        try:
            # Try to start server process
            process = await asyncio.create_subprocess_exec(
                sys.executable, server_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.log_test("MCP Server Process Start", True)
            
            # Send a simple request
            try:
                list_tools_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list",
                    "params": {}
                }
                
                request_json = json.dumps(list_tools_request) + '\n'
                process.stdin.write(request_json.encode())
                await process.stdin.drain()
                
                # Wait for response with timeout
                try:
                    response_line = await asyncio.wait_for(
                        process.stdout.readline(), timeout=10.0
                    )
                    response = json.loads(response_line.decode().strip())
                    
                    if "result" in response and "tools" in response["result"]:
                        tool_count = len(response["result"]["tools"])
                        self.log_test("MCP Server Tools List", True, 
                                    f"Found {tool_count} tools")
                    else:
                        self.log_test("MCP Server Tools List", False, 
                                    "Invalid response format")
                        
                except asyncio.TimeoutError:
                    self.log_test("MCP Server Response", False, "Timeout waiting for response")
                except json.JSONDecodeError as e:
                    self.log_test("MCP Server Response", False, f"JSON decode error: {str(e)}")
            
            except Exception as e:
                self.log_test("MCP Server Communication", False, str(e))
            
            # Clean up
            process.terminate()
            await process.wait()
            
        except Exception as e:
            self.log_test("MCP Server Startup", False, str(e))
    
    def test_fastmcp_import(self):
        """Test FastMCP import specifically"""
        print("\n⚡ Testing FastMCP...")
        
        try:
            from mcp.server.fastmcp import FastMCP
            
            # Try to create a FastMCP instance
            mcp = FastMCP("test_server")
            self.log_test("FastMCP Instance Creation", True)
            
            # Test tool decoration
            @mcp.tool()
            async def test_tool() -> str:
                """Test tool"""
                return "test"
            
            self.log_test("FastMCP Tool Decoration", True)
            
        except ImportError as e:
            self.log_test("FastMCP Import", False, str(e))
        except Exception as e:
            self.log_test("FastMCP General", False, str(e))
    
    def generate_report(self):
        """Generate a detailed test report"""
        print("\n" + "="*60)
        print("🔍 MCP STOCK SERVER DEBUG REPORT")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\nSummary:")
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
        
        print(f"\n📋 Detailed Results:")
        for result in self.test_results:
            print(f"   {result['status']}: {result['test']}")
            if result['details']:
                print(f"      {result['details']}")
        
        # Save report to file
        with open("debug_report.json", "w") as f:
            json.dump({
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests, 
                    "failed": failed_tests,
                    "success_rate": passed_tests/total_tests*100
                },
                "results": self.test_results,
                "generated_at": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n💾 Report saved to debug_report.json")

async def main():
    """Run all debugging tests"""
    debugger = MCPDebugger()
    
    print("🔧 MCP Stock Server Debugger")
    print("="*50)
    
    # Run all tests
    debugger.test_fastmcp_import()
    debugger.test_imports()
    debugger.test_yahoo_finance()
    debugger.test_date_parsing()
    debugger.test_matplotlib()
    await debugger.test_mcp_server_startup()
    
    # Generate report
    debugger.generate_report()

if __name__ == "__main__":
    import os
    asyncio.run(main())
