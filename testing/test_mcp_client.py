#!/usr/bin/env python3
"""
Simple MCP Client Test for News Instagram MCP Server
Tests the MCP server via subprocess communication
"""

import asyncio
import json
import subprocess
import sys
import time
from typing import Dict, Any

class MCPClientTester:
    def __init__(self, server_command: list):
        self.server_command = server_command
        self.process = None
        
    async def start_server(self):
        """Start the MCP server process"""
        print("🚀 Starting MCP server...")
        self.process = subprocess.Popen(
            self.server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        
        # Give the server a moment to start
        await asyncio.sleep(2)
        
        if self.process.poll() is not None:
            stderr = self.process.stderr.read()
            raise Exception(f"Server failed to start: {stderr}")
            
        print("✅ Server started successfully")
    
    def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request to the server"""
        request_json = json.dumps(request) + "\n"
        
        print(f"📤 Sending: {request['method']}")
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise Exception("No response from server")
            
        try:
            response = json.loads(response_line.strip())
            print(f"📥 Response: {response.get('result', {}).get('type', 'N/A')}")
            return response
        except json.JSONDecodeError as e:
            print(f"❌ Failed to decode response: {response_line}")
            raise e
    
    def test_initialize(self):
        """Test server initialization"""
        print("\n🔧 Testing initialization...")
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {
                        "listChanged": True
                    },
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = self.send_request(request)
        
        if "result" in response:
            server_info = response["result"]
            print(f"✅ Server: {server_info.get('serverInfo', {}).get('name', 'Unknown')}")
            print(f"✅ Protocol: {server_info.get('protocolVersion', 'Unknown')}")
            
            # Send initialized notification
            initialized_notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {}
            }
            request_json = json.dumps(initialized_notification) + "\n"
            self.process.stdin.write(request_json)
            self.process.stdin.flush()
            
            return True
        else:
            print(f"❌ Initialization failed: {response}")
            return False
    
    def test_list_tools(self):
        """Test listing available tools"""
        print("\n🛠️  Testing tools list...")
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = self.send_request(request)
        
        if "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool['name']}: {tool.get('description', 'No description')}")
            return True
        else:
            print(f"❌ Failed to list tools: {response}")
            return False
    
    def test_list_resources(self):
        """Test listing available resources"""
        print("\n📚 Testing resources list...")
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {}
        }
        
        response = self.send_request(request)
        
        if "result" in response and "resources" in response["result"]:
            resources = response["result"]["resources"]
            print(f"✅ Found {len(resources)} resources:")
            for resource in resources:
                print(f"   - {resource['uri']}: {resource.get('description', 'No description')}")
            return True
        else:
            print(f"❌ Failed to list resources: {response}")
            return False
    
    def test_tool_call(self):
        """Test calling a simple tool"""
        print("\n⚙️ Testing tool call (get_analytics)...")
        request = {
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
        
        response = self.send_request(request)
        
        if "result" in response:
            print("✅ Tool call successful")
            content = response["result"].get("content", [])
            if content:
                print(f"   Response length: {len(str(content))}")
            return True
        else:
            print(f"❌ Tool call failed: {response}")
            return False
    
    def stop_server(self):
        """Stop the MCP server"""
        if self.process:
            print("\n🛑 Stopping server...")
            self.process.terminate()
            self.process.wait()
            print("✅ Server stopped")

async def main():
    """Main test function"""
    print("🧪 MCP Client Testing")
    print("=" * 50)
    
    # Test configuration
    server_command = [sys.executable, "main.py", "--stdio"]
    
    tester = MCPClientTester(server_command)
    
    try:
        # Start server
        await tester.start_server()
        
        # Run tests
        tests_passed = 0
        total_tests = 4
        
        if tester.test_initialize():
            tests_passed += 1
            
        if tester.test_list_tools():
            tests_passed += 1
            
        if tester.test_list_resources():
            tests_passed += 1
            
        if tester.test_tool_call():
            tests_passed += 1
        
        # Summary
        print("\n" + "=" * 50)
        print(f"🎯 Test Results: {tests_passed}/{total_tests} passed")
        
        if tests_passed == total_tests:
            print("🎉 All tests passed! MCP server is working correctly.")
            return True
        else:
            print("❌ Some tests failed. Check the output above.")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    finally:
        tester.stop_server()

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
