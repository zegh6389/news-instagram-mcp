# News Instagram MCP System - Clean Structure

## 🎯 Main Files
- `main.py` - Main application entry point
- `live_demo.py` - Live demonstration script
- `mcp_launcher.py` - MCP server launcher for Claude Desktop
- `requirements.txt` - Python dependencies

## 📁 Key Directories

### `/src/` - Core System Code
- `mcp_server.py` - MCP server implementation
- `config.py` - Configuration management
- `/scrapers/` - News scraping modules
- `/processors/` - Content analysis and processing
- `/publishers/` - Instagram publishing
- `/database/` - Database models and management
- `/editors/` - Visual editing and templates

### `/config/` - Configuration Files
- `news_sources.yaml` - News source configurations
- `instagram_config.yaml` - Instagram posting settings
- `template_config.yaml` - Visual template settings

### `/testing/` - All Test Files
- `test_content_scraping.py` - News scraping tests
- `test_mcp_publish.py` - Publishing tests  
- `test_single_article.py` - Individual article tests
- `debug_globalnews.py` - Debug tools
- Various integration tests

### `/templates/` - Visual Templates
- PNG template files for Instagram posts

## 🚀 System Status
✅ All redundant files moved to testing directory
✅ Clean project structure maintained
✅ All core functionality working
✅ Ready for production deployment

## 🔧 Quick Start
```bash
# Run live demo
python live_demo.py

# Run specific tests
cd testing
python test_mcp_publish.py
```

The system is now clean, organized, and fully functional!
