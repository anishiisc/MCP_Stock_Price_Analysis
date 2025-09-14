#!/usr/bin/env python3
"""
Example MCP client to test the stock server
This demonstrates how to interact with our MCP server programmatically
"""

import asyncio
import json
import subprocess
from typing import Dict, Any

class MCPClient:
    def __init__(self, server_script: str):
        """Initialize MCP client with server script path"""
        self.server_script = server_script
        self.process = None
    
    async def start_server(self):
        """Start the MCP server process"""
        self.process = await asyncio.create_subprocess_exec(
            'python', self.server_script,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        print("🚀 MCP Server started!")
    
    async def send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        request_json = json.dumps(request) + '\n'
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode().strip())
        
        return response
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool on the MCP server"""
        params = {
            "name": tool_name,
            "arguments": arguments
        }
        return await self.send_request("tools/call", params)
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available tools on the server"""
        return await self.send_request("tools/list", {})
    
    async def list_resources(self) -> Dict[str, Any]:
        """List available resources on the server"""
        return await self.send_request("resources/list", {})
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a specific resource"""
        params = {"uri": uri}
        return await self.send_request("resources/read", params)
    
    async def stop_server(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            print("🛑 MCP Server stopped!")

async def demo_stock_analysis():
    """Demonstrate stock analysis using MCP server"""
    client = MCPClient("stock_server.py")
    
    try:
        await client.start_server()
        
        print("\n" + "="*50)
        print("📊 MCP STOCK SERVER DEMO")
        print("="*50)
        
        # List available tools
        print("\n1️⃣ Listing available tools...")
        tools_response = await client.list_tools()
        if "result" in tools_response:
            for tool in tools_response["result"]["tools"]:
                print(f"   🔧 {tool['name']}: {tool['description']}")
        
        # Get stock data for Apple
        print("\n2️⃣ Getting Apple (AAPL) stock data...")
        apple_data = await client.call_tool("get_stock_data", {
            "ticker": "AAPL",
            "name": "Apple Inc Analysis",
            "start_date": "01012024",  # Jan 1, 2024
            "end_date": "12312024"     # Dec 31, 2024
        })
        
        if "result" in apple_data:
            data = apple_data["result"]
            print(f"   📈 {data['name']} ({data['ticker']})")
            print(f"   💰 Opening Price: ${data['opening_price']}")
            print(f"   💰 Closing Price: ${data['closing_price']}")
            print(f"   📊 Price Change: ${data['price_change']}")
            print(f"   📈 Percentage Change: {data['percentage_change']}%")
            print(f"   📊 Data Points: {data['data_points']}")
        else:
            print(f"   ❌ Error: {apple_data.get('error', 'Unknown error')}")
        
        # Compare two stocks
        print("\n3️⃣ Comparing Apple vs Microsoft...")
        comparison = await client.call_tool("compare_stocks", {
            "ticker1": "AAPL",
            "ticker2": "MSFT", 
            "start_date": "01012024",
            "end_date": "12312024"
        })
        
        if "result" in comparison:
            comp = comparison["result"]
            if "error" not in comp:
                print(f"   🏆 Better Performer: {comp['better_performer']}")
                print(f"   📊 Performance Difference: {comp['performance_difference']}%")
                print(f"   📈 {comp['stock1']['ticker']}: {comp['stock1']['percentage_change']}%")
                print(f"   📈 {comp['stock2']['ticker']}: {comp['stock2']['percentage_change']}%")
            else:
                print(f"   ❌ Comparison Error: {comp['error']}")
        
        # Read stock resource
        print("\n4️⃣ Reading Apple stock resource...")
        resource = await client.read_resource("stock://data/AAPL")
        if "result" in resource:
            print("   📋 Company Information:")
            print(resource["result"]["contents"][0]["text"])
        
        # Generate plot (this will return base64 data)
        print("\n5️⃣ Generating Apple stock plot...")
        plot_result = await client.call_tool("plot_stock_price", {
            "ticker": "AAPL",
            "name": "Apple Inc",
            "start_date": "01012024",
            "end_date": "12312024"
        })
        
        if "result" in plot_result and plot_result["result"].startswith("data:image"):
            print("   📊 Plot generated successfully! (Base64 image data)")
            print(f"   📏 Data length: {len(plot_result['result'])} characters")
        else:
            print(f"   ❌ Plot Error: {plot_result.get('result', 'Unknown error')}")
        
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
    
    finally:
        await client.stop_server()

async def interactive_mode():
    """Interactive mode for testing different stocks"""
    client = MCPClient("stock_server.py")
    
    try:
        await client.start_server()
        print("\n🔄 Interactive MCP Stock Server Mode")
        print("Type 'quit' to exit")
        
        while True:
            print("\n" + "-"*30)
            ticker = input("Enter stock ticker (or 'quit'): ").upper().strip()
            
            if ticker == 'QUIT':
                break
            
            if not ticker:
                continue
            
            start_date = input("Start date (mmddyyyy, e.g., 01012024): ").strip()
            end_date = input("End date (mmddyyyy, e.g., 12312024): ").strip()
            
            try:
                result = await client.call_tool("get_stock_data", {
                    "ticker": ticker,
                    "name": f"{ticker} Analysis",
                    "start_date": start_date,
                    "end_date": end_date
                })
                
                if "result" in result:
                    data = result["result"]
                    if "error" in data:
                        print(f"❌ Error: {data['error']}")
                    else:
                        print(f"\n📊 Results for {ticker}:")
                        print(f"Opening: ${data['opening_price']}")
                        print(f"Closing: ${data['closing_price']}")
                        print(f"Change: {data['percentage_change']}%")
                        print(f"High: ${data['highest_price']}")
                        print(f"Low: ${data['lowest_price']}")
                else:
                    print(f"❌ Request failed: {result}")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    finally:
        await client.stop_server()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(demo_stock_analysis())
