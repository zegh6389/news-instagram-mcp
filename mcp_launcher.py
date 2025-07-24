#!/usr/bin/env python3
"""
MCP Server Launcher for Claude Desktop
This script ensures all environment variables are set and launches the MCP server
"""

import os
import sys
import asyncio
from pathlib import Path

def setup_environment():
    """Set up environment variables and paths"""
    # Set working directory to script location
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Set environment variables
    env_vars = {
        "INSTAGRAM_USERNAME": "awais_zegham",
        "INSTAGRAM_PASSWORD": "@Wadooha374549", 
        "GEMINI_API_KEY": "AIzaSyBr4u-XuKXY24e8q0JlJNP8BQN1YwBAQGQ",
        "DATABASE_URL": f"sqlite:///{script_dir}/news_instagram.db",
        "LOG_LEVEL": "INFO",
        "PYTHONPATH": str(script_dir),
        "PYTHONUNBUFFERED": "1"
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    # Add src to Python path
    src_path = script_dir / 'src'
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    return script_dir

async def main():
    """Main launcher function"""
    try:
        # Setup environment
        script_dir = setup_environment()
        
        # Import and run the main application
        from main import main as main_func
        await main_func()
        
    except Exception as e:
        print(f"Error launching MCP server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
