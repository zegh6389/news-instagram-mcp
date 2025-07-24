@echo off
echo ===================================================
echo  Instagram Cookie Authentication Setup
echo ===================================================
echo.

echo Step 1: Setting up Instagram session with your cookies...
python instagram_cookie_auth.py

echo.
echo ===================================================
echo  Setup Complete! 
echo ===================================================
echo.

echo Now testing your automation...
echo.

echo Step 2: Running automation test...
python deploy/manual_automation.py

echo.
echo ===================================================
echo  All Done!
echo ===================================================
echo.
echo Check the logs above for "Real Instagram client connected"
echo If you see any errors, check instagram_cookie_auth.log
echo.

pause
