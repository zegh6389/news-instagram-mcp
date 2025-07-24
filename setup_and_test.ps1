Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " Instagram Cookie Authentication Setup" -ForegroundColor Cyan  
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Setting up Instagram session with your cookies..." -ForegroundColor Yellow
python instagram_cookie_auth.py

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host " Setup Complete!" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Now testing your automation..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Step 2: Running automation test..." -ForegroundColor Yellow
python deploy/manual_automation.py

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host " All Done!" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Check the logs above for 'Real Instagram client connected'" -ForegroundColor White
Write-Host "If you see any errors, check instagram_cookie_auth.log" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to continue..."
