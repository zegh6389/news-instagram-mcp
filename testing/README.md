# Testing Directory

This directory contains all testing and debugging scripts for the news-instagram-mcp system.

## Test Files

### Core System Tests
- `test_content_scraping.py` - Tests news scraping from all sources
- `test_mcp_publish.py` - Tests publishing through MCP server
- `test_single_article.py` - Tests individual article processing

### Debug Tools
- `debug_globalnews.py` - Debugging tool for Global News scraping issues

## Running Tests

### Full System Test
```bash
cd testing
python test_mcp_publish.py
```

### Content Scraping Test
```bash
cd testing  
python test_content_scraping.py
```

### Individual Article Test
```bash
cd testing
python test_single_article.py
```

## Test Status
✅ All tests passing as of July 24, 2025
✅ System ready for production use
✅ Demo mode working correctly

## Notes
- All tests use demo/simulation mode
- No real Instagram credentials required for testing
- Tests verify end-to-end functionality
