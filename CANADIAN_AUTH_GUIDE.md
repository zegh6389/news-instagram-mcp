# Instagram Location Authentication Guide
## Resolving "Suspicious Login from USA" Issues for Milton, Canada

### 🚨 Problem Description
You're experiencing Instagram blocking login attempts with the message "We stopped a suspicious login from the USA" when trying to authenticate your MCP server from Milton, Ontario, Canada.

### 🇨🇦 Canadian Location Solution

This guide provides a comprehensive solution to establish trusted Instagram authentication from your Milton, Canada location.

## 🛠️ Implementation Steps

### Step 1: Set Up Environment Variables
Create a `.env` file in your project root with your credentials:

```bash
# Instagram Credentials
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# Location Context
LOCATION_CITY=Milton
LOCATION_PROVINCE=Ontario
LOCATION_COUNTRY=Canada
LOCATION_TIMEZONE=America/Toronto
```

### Step 2: Run Canadian Authentication Setup
Use our specialized Canadian authentication script:

```bash
python setup_canadian_auth.py
```

This script will:
- ✅ Configure Canadian device profile (Samsung Galaxy S21 Canadian model)
- ✅ Set Canadian locale (en_CA) and timezone (America/Toronto)
- ✅ Use Milton, Ontario location context
- ✅ Establish a trusted session from your location

### Step 3: Manual Instagram Login (IMPORTANT)
Before running automation, perform these manual steps:

1. **Web Browser Login**:
   - Open Instagram.com in your browser
   - Log in manually from the same device/network
   - Complete any security challenges
   - Stay logged in for at least 30 minutes

2. **Mobile App Login** (Recommended):
   - Install Instagram mobile app on the same device
   - Log in through the mobile app
   - Browse normally for 10-15 minutes
   - This establishes device trust

### Step 4: Handle Security Challenges

If you receive security emails or challenges:

#### Email Verification:
- Check email for "Login attempt from Canada" notifications
- Click "This was me" to approve the location
- Wait 10-15 minutes before retrying automation

#### SMS Verification:
- Ensure your phone number is verified on Instagram
- Respond to any SMS verification codes promptly

#### Two-Factor Authentication:
- If enabled, you may need to temporarily disable it
- Or implement 2FA code handling in your automation

### Step 5: Test Authentication
Run the test script to verify your setup:

```bash
python test_canadian_auth.py
```

## 🔧 Technical Implementation

### Enhanced Authentication Manager
The new `InstagramAuthManager` class provides:

- **Canadian Device Profile**: Uses Samsung Galaxy S21 Canadian model (SM-G991W)
- **Location Context**: Milton, Ontario, Canada with proper timezone
- **Session Persistence**: Maintains authentication for 30 days
- **Rate Limiting**: Increased delays to appear more human-like
- **Error Handling**: Specific guidance for location-based blocks

### Device Consistency
The system maintains consistent device fingerprinting:
- Same device ID across sessions
- Canadian user agent strings
- Proper Android version and app version
- Location-appropriate device model

## 🛡️ Security Best Practices

### 1. Gradual Activity Increase
Start with minimal posting frequency:
- Day 1: 1 post
- Day 2-3: 2 posts
- Week 1: 3 posts/day
- Week 2+: Up to 5 posts/day

### 2. Human-like Timing
Use Canadian time zones for posting:
- Morning: 8:00 AM ET
- Lunch: 12:00 PM ET
- Afternoon: 4:00 PM ET
- Evening: 7:00 PM ET
- Night: 9:00 PM ET

### 3. Content Localization
Include Canadian context in your posts:
- Use Canadian spelling (colour, centre, etc.)
- Include Canadian hashtags (#Canada, #Ontario, #Milton)
- Reference Canadian time zones (ET, PT)
- Use Canadian news sources

## 🚨 Troubleshooting Common Issues

### Issue: "Suspicious Activity" Block
**Solution**:
1. Wait 24 hours before retrying
2. Log in manually from browser/app
3. Verify email address and phone number
4. Check for account restrictions

### Issue: Challenge Required
**Solution**:
1. Complete challenges manually in browser
2. Use the same device for both manual and automated access
3. Maintain consistent IP address

### Issue: Session Expires Quickly
**Solution**:
1. Ensure session files are not being deleted
2. Check file permissions on session directory
3. Verify device consistency settings

### Issue: Rate Limiting
**Solution**:
1. Increase delays between actions
2. Reduce posting frequency
3. Use prime posting times only

## 📊 Monitoring and Maintenance

### Session Health Check
Run daily to verify authentication status:
```bash
python -c "from src.auth import InstagramAuthManager; print('✅ Authenticated' if InstagramAuthManager('username', 'password').is_authenticated() else '❌ Not authenticated')"
```

### Log Monitoring
Watch for these success indicators:
- `✅ Valid session found for @username`
- `🍁 Location context: Milton, Ontario, Canada`
- `📱 Connected to Instagram as @username`

### Warning Signs
Monitor logs for these issues:
- Location-based blocking messages
- Frequent session invalidation
- Challenge requirements
- Rate limit warnings

## 🎯 Success Metrics

You'll know the solution is working when:
- ✅ No more "suspicious login" messages
- ✅ Sessions persist for multiple days
- ✅ Posting automation runs without interruption
- ✅ No location-based authentication challenges
- ✅ Consistent posting schedule maintained

## 📞 Support

If you continue experiencing issues:

1. **Check Recent Changes**: Instagram frequently updates security measures
2. **Account Status**: Verify your account isn't restricted or shadow-banned
3. **Network Consistency**: Ensure you're always posting from the same network/location
4. **Manual Verification**: Periodically log in manually to maintain trust

## 🔄 Regular Maintenance

### Weekly Tasks:
- Verify session is still valid
- Check for new security emails
- Monitor posting success rate

### Monthly Tasks:
- Update device profile if needed
- Review and adjust posting schedule
- Clear old session files

### As Needed:
- Re-authenticate after Instagram app updates
- Adjust for Instagram policy changes
- Update Canadian device specifications

---

**Remember**: Instagram's security systems are designed to protect accounts. Working with them, rather than against them, ensures long-term success for your automation.
