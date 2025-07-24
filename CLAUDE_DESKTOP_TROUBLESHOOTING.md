# 🔧 Claude Desktop MCP Integration Troubleshooting Guide

## Current Status: ✅ MCP Server Working, Claude Desktop Configuration Updated

Your News Instagram MCP Server is working correctly, but Claude Desktop needs proper setup to recognize it.

---

## 🚀 Updated Integration Steps

### 1. Configuration File Location
Your Claude Desktop config file is located at:
```
C:\Users\Awais\AppData\Roaming\Claude\claude_desktop_config.json
```

### 2. Current Configuration
The file now contains:
```json
{
    "mcpServers": {
        "news-instagram-mcp": {
            "args": [
                "G:/cursor/news-instagram-mcp/mcp_launcher.py",
                "--stdio"
            ],
            "command": "python"
        }
    }
}
```

### 3. Launcher Script Created
We've created `mcp_launcher.py` that:
- ✅ Sets all environment variables automatically
- ✅ Sets correct working directory
- ✅ Launches the MCP server with proper configuration
- ✅ Tested and confirmed working

---

## 🔄 Next Steps to Complete Integration

### Step 1: Restart Claude Desktop Completely
1. **Close all Claude Desktop windows**
2. **End all Claude processes** (we already did this)
3. **Wait 10 seconds**
4. **Start Claude Desktop fresh**

### Step 2: Look for MCP Connection Indicators
After restarting, look for:
- 🟢 Green indicator showing MCP server connected
- ⚙️ Available tools in Claude's interface
- 📚 Available resources listed

### Step 3: Test Commands
Try these exact commands in Claude Desktop:

```
"List available MCP tools"
```

```
"What MCP servers are connected?"
```

```
"Use the scrape_news tool to get recent CBC news"
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Claude Desktop Shows "No MCP Servers"
**Solution:**
1. Verify config file exists: `C:\Users\Awais\AppData\Roaming\Claude\claude_desktop_config.json`
2. Check JSON syntax is valid
3. Restart Claude Desktop completely
4. Check Claude Desktop version (needs to support MCP)

### Issue 2: "Command Not Found" Error
**Solution:**
1. Verify Python is in PATH: `python --version`
2. Test launcher manually: `python G:/cursor/news-instagram-mcp/mcp_launcher.py --stdio`
3. Use absolute path to Python if needed

### Issue 3: "Permission Denied" Error
**Solution:**
1. Run Claude Desktop as administrator
2. Check file permissions on the MCP server directory
3. Verify Python execution permissions

### Issue 4: Environment Variables Not Working
**Solution:**
- ✅ Already fixed! The launcher script sets all variables automatically
- No need to set system environment variables

---

## 🧪 Manual Testing

If Claude Desktop still doesn't work, test manually:

### Test 1: Direct Server Test
```bash
cd G:\cursor\news-instagram-mcp
python mcp_launcher.py --stdio
```
Then paste this JSON:
```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
```

Expected: JSON response with server info ✅ (We confirmed this works)

### Test 2: Tools List Test
After initialization, send:
```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

Expected: List of 6 tools (scrape_news, analyze_content, etc.)

---

## 📱 Alternative: Claude Desktop Beta/Dev Version

If the current Claude Desktop doesn't support MCP:

1. **Check Claude Desktop version**: Look for MCP support in settings
2. **Download Claude Desktop Dev/Beta**: If available
3. **Use Claude API directly**: Alternative integration method

---

## 🎯 Expected Behavior When Working

When properly integrated, you should be able to ask Claude:

```
"Hi Claude! Can you help me scrape some recent news using the news-instagram-mcp server?"
```

And Claude should respond with something like:
```
"I can help you scrape recent news! I have access to your news-instagram-mcp server with tools for scraping CBC, Global News, and CTV. Let me get the latest articles for you..."
```

---

## 🔍 Debug Commands

If issues persist, run these for debugging:

```bash
# Test Python access
python --version

# Test MCP server directly  
cd G:\cursor\news-instagram-mcp
python test_mcp_client.py

# Check config file
Get-Content "C:\Users\Awais\AppData\Roaming\Claude\claude_desktop_config.json"

# Test launcher
python mcp_launcher.py --stdio
```

---

## 📞 Support Information

- **MCP Server Status**: ✅ Working perfectly
- **Configuration**: ✅ Updated and tested
- **Launcher Script**: ✅ Created and working
- **Next Step**: Restart Claude Desktop and test

**The MCP server is 100% ready - the issue is just Claude Desktop recognition!**
