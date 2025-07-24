import json
import sys
from pathlib import Path

def validate_claude_config():
    """Validate Claude Desktop configuration file"""
    config_path = Path(r"C:\Users\Awais\AppData\Roaming\Claude\claude_desktop_config.json")
    
    print("🔍 Validating Claude Desktop Configuration")
    print("=" * 50)
    
    if not config_path.exists():
        print("❌ Configuration file does not exist!")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 File size: {len(content)} characters")
        print(f"📁 File path: {config_path}")
        
        # Try to parse JSON
        config = json.loads(content)
        print("✅ JSON syntax is valid")
        
        # Check structure
        if "mcpServers" in config:
            servers = config["mcpServers"]
            print(f"✅ Found mcpServers section with {len(servers)} servers")
            
            for server_name, server_config in servers.items():
                print(f"   - {server_name}: {server_config.get('command', 'No command')}")
                
                # Check required fields
                if "command" in server_config:
                    print(f"     ✅ Command: {server_config['command']}")
                else:
                    print(f"     ❌ Missing command")
                
                if "args" in server_config:
                    print(f"     ✅ Args: {len(server_config['args'])} arguments")
                else:
                    print(f"     ⚠️  No args specified")
        else:
            print("❌ No mcpServers section found")
            return False
        
        print("\n🎉 Configuration is valid!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Syntax Error: {e}")
        print(f"   Line {e.lineno}, Column {e.colno}")
        print(f"   Error: {e.msg}")
        
        # Show problematic area
        lines = content.split('\n')
        if e.lineno <= len(lines):
            print(f"\n📍 Problematic line:")
            print(f"   {e.lineno}: {lines[e.lineno-1]}")
            if e.colno > 0:
                print(f"        {' ' * (e.colno-1)}^")
        
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    validate_claude_config()
