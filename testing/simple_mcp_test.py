#!/usr/bin/env python3
"""
Simple test to verify MCP server can handle basic requests
"""

import asyncio
import json
import subprocess
import sys

async def test_mcp_server():
    """Test basic MCP server functionality"""
    print("🧪 Testing MCP Server")
    print("=" * 40)
    
    # Start server
    print("🚀 Starting server...")
    process = subprocess.Popen(
        [sys.executable, "main.py", "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    try:
        # Test initialization
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("📤 Sending initialization...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            try:
                response = json.loads(response_line.strip())
                print(f"📥 Response: {response}")
                
                if "result" in response:
                    print("✅ Server initialized successfully")
                    
                    # Test tools list
                    tools_request = {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/list",
                        "params": {}
                    }
                    
                    print("📤 Requesting tools list...")
                    process.stdin.write(json.dumps(tools_request) + "\n")
                    process.stdin.flush()
                    
                    tools_response = process.stdout.readline()
                    if tools_response:
                        tools_data = json.loads(tools_response.strip())
                        print(f"📥 Tools response: {tools_data}")
                        
                        if "result" in tools_data and "tools" in tools_data["result"]:
                            tools = tools_data["result"]["tools"]
                            print(f"✅ Found {len(tools)} tools:")
                            for tool in tools:
                                print(f"   - {tool['name']}")
                        else:
                            print(f"❌ Failed to get tools: {tools_data}")
                else:
                    print(f"❌ Initialization failed: {response}")
                    
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON response: {response_line}")
        else:
            print("❌ No response from server")
            
    finally:
        print("🛑 Stopping server...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
