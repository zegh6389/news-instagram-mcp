# 🇨🇦 Quick Start: Canadian Instagram Authentication

## Problem Solved
This setup resolves the "We stopped a suspicious login from the USA" issue by establishing trusted Instagram authentication from Milton, Ontario, Canada.

## 🚀 Quick Setup (Windows)

### Option 1: PowerShell Script (Recommended)
```powershell
# Run from project directory
.\setup_canadian_auth.ps1
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables (create .env file)
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# 3. Run Canadian authentication
python setup_canadian_auth.py

# 4. Test authentication
python test_canadian_auth.py
```

## ✅ What This Setup Does

1. **🍁 Canadian Device Profile**
   - Uses Samsung Galaxy S21 Canadian model (SM-G991W)
   - Sets Canadian locale (en_CA) and timezone (America/Toronto)
   - Configures Milton, Ontario location context

2. **🔐 Enhanced Authentication**
   - Maintains persistent sessions (30-day validity)
   - Implements Canadian-specific rate limiting
   - Uses location-aware error handling

3. **📱 Device Consistency**
   - Generates consistent device fingerprints
   - Maintains same device ID across sessions
   - Uses Canadian user agent strings

## 🎯 Expected Results

After successful setup:
- ✅ No more "suspicious login" messages
- ✅ Instagram recognizes Milton, Canada as trusted location
- ✅ Sessions persist without frequent re-authentication
- ✅ Automated posting works without location blocks

## 📋 Verification Steps

1. **Check Authentication Status**:
   ```bash
   python test_canadian_auth.py
   ```

2. **Verify Session Files**:
   - `sessions/your_username_session.json` - Instagram session
   - `sessions/your_username_device.json` - Canadian device profile

3. **Test Manual Posting**:
   ```bash
   python deploy/manual_automation.py
   ```

## 🔧 Troubleshooting

### Still Getting Blocked?
1. **Manual Browser Login First**:
   - Open Instagram.com in browser
   - Log in manually from this device
   - Stay logged in for 30+ minutes

2. **Check Email**:
   - Look for Instagram security notifications
   - Click "This was me" for Canada login attempts

3. **Mobile App Login**:
   - Install Instagram app on this device
   - Log in and browse normally
   - This establishes device trust

### Account Issues?
- Verify account isn't restricted/suspended
- Check if 2FA is enabled (may need to disable temporarily)
- Ensure phone number and email are verified

## 📊 Success Indicators

Look for these log messages:
```
✅ Valid session found for @username
🍁 Location context: Milton, Ontario, Canada
📱 Connected to Instagram as @username
```

## 🔄 Ongoing Maintenance

### Daily:
- Monitor authentication status
- Check for security emails

### Weekly:
- Verify session is still valid
- Review posting success rate

### Monthly:
- Log in manually to maintain trust
- Update device profile if needed

## 📞 Additional Support

If issues persist:
1. Read the full `CANADIAN_AUTH_GUIDE.md`
2. Check Instagram's recent policy changes
3. Verify your network consistently shows Canadian location
4. Consider using a VPN with a Canadian server in Milton/Toronto area

---

**Remember**: The key is establishing trust with Instagram from your actual Canadian location first, then maintaining that trust through consistent device and network usage.
