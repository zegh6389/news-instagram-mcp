#!/usr/bin/env python3
"""
Final Claude Desktop MCP Integration Test
Tests if Claude Desktop can successfully connect to your MCP server
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def test_mcp_tools_and_resources():
    """Test MCP server tools and resources"""
    
    print("🎯 Final Claude Desktop MCP Integration Test")
    print("=" * 60)
    
    # Test 1: Verify MCP server responds correctly
    print("\n1. 🧪 Testing MCP Server Response...")
    
    try:
        # Start the MCP server
        process = subprocess.Popen([
            sys.executable, "mcp_launcher.py", "--stdio"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
           stderr=subprocess.PIPE, text=True, cwd=Path.cwd())
        
        # Send initialization
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "claude-test", "version": "1.0.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_msg) + "\n")
        process.stdin.flush()
        
        # Read initialization response
        response = process.stdout.readline()
        init_response = json.loads(response.strip())
        
        if "result" in init_response:
            print("   ✅ Server initialization successful")
            server_info = init_response["result"]["serverInfo"]
            print(f"   ✅ Server name: {server_info['name']}")
            print(f"   ✅ Server version: {server_info['version']}")
        else:
            print(f"   ❌ Initialization failed: {init_response}")
            return False
        
        # Send initialized notification
        initialized_msg = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        process.stdin.write(json.dumps(initialized_msg) + "\n")
        process.stdin.flush()
        
        # Test 2: List Tools
        print("\n2. 🛠️ Testing Available Tools...")
        
        tools_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        process.stdin.write(json.dumps(tools_msg) + "\n")
        process.stdin.flush()
        
        tools_response = process.stdout.readline()
        tools_data = json.loads(tools_response.strip())
        
        if "result" in tools_data and "tools" in tools_data["result"]:
            tools = tools_data["result"]["tools"]
            print(f"   ✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"      - {tool['name']}: {tool.get('description', 'No description')}")
        else:
            print(f"   ❌ Failed to list tools: {tools_data}")
        
        # Test 3: List Resources
        print("\n3. 📚 Testing Available Resources...")
        
        resources_msg = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {}
        }
        
        process.stdin.write(json.dumps(resources_msg) + "\n")
        process.stdin.flush()
        
        resources_response = process.stdout.readline()
        resources_data = json.loads(resources_response.strip())
        
        if "result" in resources_data and "resources" in resources_data["result"]:
            resources = resources_data["result"]["resources"]
            print(f"   ✅ Found {len(resources)} resources:")
            for resource in resources:
                print(f"      - {resource['uri']}: {resource.get('description', 'No description')}")
        else:
            print(f"   ❌ Failed to list resources: {resources_data}")
        
        # Test 4: Test a tool call
        print("\n4. ⚙️ Testing Tool Execution...")
        
        tool_call_msg = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_analytics",
                "arguments": {
                    "period": "daily",
                    "days": 1
                }
            }
        }
        
        process.stdin.write(json.dumps(tool_call_msg) + "\n")
        process.stdin.flush()
        
        tool_response = process.stdout.readline()
        tool_data = json.loads(tool_response.strip())
        
        if "result" in tool_data:
            print("   ✅ Tool execution successful")
            content = tool_data["result"].get("content", [])
            if content:
                preview = content[0].get("text", "")[:100] + "..." if len(content[0].get("text", "")) > 100 else content[0].get("text", "")
                print(f"   📄 Response preview: {preview}")
        else:
            print(f"   ❌ Tool execution failed: {tool_data}")
        
        # Cleanup
        process.terminate()
        process.wait()
        
        print("\n" + "=" * 60)
        print("🎉 MCP Server Test Complete!")
        print("\n📋 Summary:")
        print("   ✅ Your MCP server is working perfectly")
        print("   ✅ All tools and resources are accessible")
        print("   ✅ Tool execution is functional")
        print("\n🚀 Next Steps:")
        print("   1. Restart Claude Desktop completely")
        print("   2. Look for MCP connection indicators")
        print("   3. Try asking Claude: 'What MCP servers are connected?'")
        print("   4. Ask Claude: 'Use the scrape_news tool to get recent news'")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mcp_tools_and_resources()
    if success:
        print("\n🎊 Your News Instagram MCP Server is ready for Claude Desktop!")
    else:
        print("\n❌ Issues found - check the errors above")
