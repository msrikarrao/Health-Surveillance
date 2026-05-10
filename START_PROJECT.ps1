# Smart Health Surveillance System - Complete Project Startup
# This script starts all required services: Backend, ML Service, and Frontend

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 SMART HEALTH SURVEILLANCE SYSTEM - PROJECT STARTUP" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan

# Create new windows for each service
Write-Host "`n📋 Starting Services..."

# 1. ML Service (Port 5001)
Write-Host "`n1️⃣  Starting ML Service (Advanced Model with Multi-Source Data)..." -ForegroundColor Yellow
$mlProcess = Start-Process powershell -ArgumentList {
    cd "E:\Srikar\TBP\TBP\backend\ml-service"
    Write-Host "🤖 ML Service: Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt --quiet
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
    Write-Host "`n🚀 Starting Flask ML Service on port 5001..." -ForegroundColor Green
    Write-Host "   - Model: Gradient Boosting Classifier" -ForegroundColor Gray
    Write-Host "   - Features: 24 (from 5 data sources)" -ForegroundColor Gray
    Write-Host "   - Data: ASHA + Seasonal + IoT + Water Infrastructure" -ForegroundColor Gray
    python app.py
} -PassThru

# Wait a moment
Start-Sleep -Seconds 3

# 2. Backend Server (Port 3000 or 8000)
Write-Host "`n2️⃣  Starting Backend Server..." -ForegroundColor Yellow
$backendProcess = Start-Process powershell -ArgumentList {
    cd "E:\Srikar\TBP\TBP\backend"
    Write-Host "🔧 Backend: Checking dependencies..." -ForegroundColor Cyan
    
    if (Test-Path "package.json") {
        npm install --silent
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
        Write-Host "`n🚀 Starting Node.js Backend Server..." -ForegroundColor Green
        npm start
    } else {
        Write-Host "⚠️  No package.json found in backend" -ForegroundColor Yellow
    }
} -PassThru

# Wait a moment
Start-Sleep -Seconds 3

# 3. Frontend (Port 3001 or 3000)
Write-Host "`n3️⃣  Starting Frontend Application..." -ForegroundColor Yellow
$frontendProcess = Start-Process powershell -ArgumentList {
    cd "E:\Srikar\TBP\TBP\frontend"
    Write-Host "⚛️  Frontend: Checking dependencies..." -ForegroundColor Cyan
    
    if (Test-Path "package.json") {
        npm install --silent
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
        Write-Host "`n🚀 Starting React Frontend..." -ForegroundColor Green
        npm start
    } else {
        Write-Host "⚠️  No package.json found in frontend" -ForegroundColor Yellow
    }
} -PassThru

# Summary
Write-Host "`n" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "✅ ALL SERVICES STARTED" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "`n📍 Service URLs:"
Write-Host "   • ML Service:   http://localhost:5001" -ForegroundColor Blue
Write-Host "   • Backend:      http://localhost:3000 (or 8000)" -ForegroundColor Blue
Write-Host "   • Frontend:     http://localhost:3001 (or 3000)" -ForegroundColor Blue

Write-Host "`n📊 ML Model Features (24 total):"
Write-Host "   ✓ Health Symptoms (6): diarrhea, vomiting, fever, headache, fatigue, nausea" -ForegroundColor Gray
Write-Host "   ✓ ASHA Workers (4): vaccination, awareness, outbreaks, reports" -ForegroundColor Gray
Write-Host "   ✓ Seasonal (4): season, humidity, rainfall, disease_risk" -ForegroundColor Gray
Write-Host "   ✓ IoT Water (5): turbidity, pH, bacteria, nitrate, chlorine" -ForegroundColor Gray
Write-Host "   ✓ Water Source (5): risk_score, maintenance, chlorination, age, village_count" -ForegroundColor Gray

Write-Host "`n🧪 Quick Test:"
Write-Host "   curl -X GET http://localhost:5001/health" -ForegroundColor Gray

Write-Host "`n🛑 To Stop: Close these PowerShell windows or press Ctrl+C" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
