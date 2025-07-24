#!/usr/bin/env python3
"""Minimal MCP Server Test"""

import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

def create_test_server():
    """Create a minimal test MCP server"""
    server = Server("test-server")
    
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="test_tool",
                description="A simple test tool",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "A test message"
                        }
                    }
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "test_tool":
            message = arguments.get("message", "Hello World!")
            return [TextContent(type="text", text=f"Test response: {message}")]
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    return server

async def main():
    """Run the test server"""
    server = create_test_server()
    
    # Run with stdio
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
