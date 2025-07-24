# 🤖 Claude Desktop Integration Guide

## Setting Up News Instagram MCP Server with Claude Desktop

### Prerequisites
✅ Claude Desktop app installed  
✅ News Instagram MCP Server tested and working  
✅ Environment variables configured  

---

### Step 1: Find Your Claude Desktop Config File

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**  
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Add MCP Server Configuration

Open the config file and add this configuration:

```json
{
  "mcpServers": {
    "news-instagram-mcp": {
      "command": "python",
      "args": [
        "G:/cursor/news-instagram-mcp/main.py",
        "--stdio"
      ],
      "env": {
        "INSTAGRAM_USERNAME": "awais_zegham",
        "INSTAGRAM_PASSWORD": "your_actual_password_here",
        "GEMINI_API_KEY": "your_actual_api_key_here",
        "DATABASE_URL": "sqlite:///G:/cursor/news-instagram-mcp/news_instagram.db",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Step 3: Update Environment Variables

Replace the placeholder values with your actual credentials:

1. **INSTAGRAM_PASSWORD**: Your Instagram account password
2. **GEMINI_API_KEY**: Your Google Gemini API key

### Step 4: Restart Claude Desktop

1. Close Claude Desktop completely
2. Restart the application
3. Look for MCP server connection status

---

### Step 5: Test the Integration

Once Claude Desktop restarts, you should see your MCP server connected. Try these commands:

#### Available Tools:
- **scrape_news** - Scrape latest news from CBC, Global News, CTV
- **analyze_content** - Analyze articles for content and categorization
- **generate_post** - Create Instagram post from news article
- **schedule_post** - Schedule post for later publishing
- **publish_post** - Publish Instagram post immediately  
- **get_analytics** - View statistics and analytics

#### Available Resources:
- **news://articles/recent** - View recently scraped articles
- **news://posts/scheduled** - Check scheduled posts
- **news://analytics/daily** - Daily performance metrics
- **news://config/sources** - News source configuration

---

### Example Usage in Claude Desktop

```
Hi Claude! Can you help me scrape some recent news and create an Instagram post?

1. Use the scrape_news tool to get latest CBC news
2. Analyze the content to find the most engaging story
3. Generate an Instagram post with an appropriate image template
```

---

### Troubleshooting

#### MCP Server Not Connecting:
1. Check file paths are correct (use forward slashes `/` even on Windows)
2. Verify Python is accessible from command line
3. Ensure all environment variables are set correctly
4. Check Claude Desktop logs for error messages

#### Permission Issues:
1. Make sure Claude Desktop has permission to run Python
2. Verify file paths are accessible
3. Try running the server manually first: `python main.py --stdio`

#### Environment Variables:
1. Double-check API keys are valid
2. Ensure Instagram credentials are correct
3. Test database path is writable

---

### Security Notes

⚠️ **Important**: Your configuration file contains sensitive credentials!

1. Keep the config file secure
2. Don't share or commit it to version control
3. Consider using environment variables instead of hardcoded values
4. Regularly rotate API keys and passwords

---

### Alternative Configuration (Using System Environment Variables)

If you prefer not to store credentials in the config file:

```json
{
  "mcpServers": {
    "news-instagram-mcp": {
      "command": "python",
      "args": [
        "G:/cursor/news-instagram-mcp/main.py",
        "--stdio"
      ]
    }
  }
}
```

Then set your environment variables at the system level.

---

### Success Indicators

✅ Claude Desktop shows MCP server as "Connected"  
✅ You can see available tools when typing commands  
✅ News scraping and Instagram posting work correctly  
✅ No error messages in Claude Desktop logs  

---

**🎉 Once configured, you'll have a powerful AI assistant that can automatically scrape news, analyze content, and create Instagram posts for you!**
