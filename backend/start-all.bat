@echo off
echo Starting Health Surveillance System with Python ML...
echo.

echo [1/2] Starting Python ML Service (port 5001)...
start "Python ML Service" cmd /k "cd ml-service && python app.py"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Node.js Backend (port 5000)...
start "Node.js Backend" cmd /k "npm run dev"

echo.
echo ✅ Both services starting...
echo.
echo Python ML Service: http://localhost:5001
echo Node.js Backend: http://localhost:5000
echo.
echo Press any key to stop all services...
pause > nul

taskkill /FI "WINDOWTITLE eq Python ML Service*" /T /F
taskkill /FI "WINDOWTITLE eq Node.js Backend*" /T /F
