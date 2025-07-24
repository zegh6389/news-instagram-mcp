#!/usr/bin/env python3
"""
Test script to verify the demo publisher works through MCP server
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.mcp_server import NewsInstagramMCPServer

async def test_publish_through_mcp():
    """Test publishing through the MCP server"""
    
    print('🧪 Testing Instagram Publishing through MCP Server')
    print('=' * 50)
    
    try:
        server = NewsInstagramMCPServer()
        
        # Check what type of publisher we have
        publisher_type = type(server.instagram_publisher).__name__
        print(f"📱 Publisher Type: {publisher_type}")
        
        # Try to publish post 8 (if it exists)
        print('\n📤 Attempting to publish post ID 8...')
        result = await server._publish_post_tool({
            'post_id': 8,
            'caption_override': '🧪 Test post through MCP server! This demonstrates the news-instagram-mcp system working end-to-end. #TestPost #MCPDemo #NewsAutomation'
        })
        
        print('✅ Publish Result:')
        for content in result:
            print(content.text)
            
        # Try to publish post 9
        print('\n📤 Attempting to publish post ID 9...')
        result = await server._publish_post_tool({
            'post_id': 9,
            'caption_override': '⚾ Sports update from the MCP news system! Automated content generation working perfectly. #Sports #BaseballNews #MCPDemo'
        })
        
        print('✅ Publish Result:')
        for content in result:
            print(content.text)
            
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_publish_through_mcp())
