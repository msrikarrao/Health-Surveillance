# 🚀 QUICK START - Python ML Integration

## ⚡ Get Started in 3 Minutes!

```
┌─────────────────────────────────────────────────────────────┐
│  SMART HEALTH SURVEILLANCE SYSTEM - PYTHON ML EDITION       │
│  Random Forest Model for Disease Outbreak Prediction        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites Check

```bash
# Check Node.js (need v18+)
node --version

# Check Python (need 3.8+)
python --version

# Check MongoDB (should be running)
mongod --version
```

✅ All installed? Let's go!

---

## 🎯 3-Step Setup

### STEP 1: Install Python Dependencies (30 seconds)
```bash
cd backend/ml-service
pip install -r requirements.txt
```

**What it installs:**
- Flask (web framework)
- scikit-learn (ML library)
- NumPy, Pandas (data processing)

---

### STEP 2: Start All Services (1 minute)

#### Option A: Windows (Easiest)
```bash
cd backend
start-all.bat
```
✅ This starts both Python ML and Node.js automatically!

#### Option B: Manual (All Platforms)
```bash
# Terminal 1: Python ML Service
cd backend/ml-service
python app.py
# ✅ ML Service running on http://localhost:5001

# Terminal 2: Node.js Backend
cd backend
npm run dev
# ✅ Backend running on http://localhost:5000

# Terminal 3: Frontend
cd frontend
npm run dev
# ✅ Frontend running on http://localhost:3000
```

---

### STEP 3: Test It! (1 minute)

#### Test Python Service
```bash
cd backend/ml-service
python test_service.py
```

**Expected Output:**
```
Testing Python ML Service...
==================================================
✅ Health Check: {'status': 'healthy'}

📊 Prediction Result:
{
  "riskLevel": "HIGH",
  "confidenceScore": 87,
  "predictedDisease": "Cholera outbreak"
}
```

#### Test via Dashboard
1. Open browser: **http://localhost:3000**
2. Login: `official@test.com` / `password123`
3. Click "Submit Report" → Add health data
4. Go to Dashboard → Click "Run AI Prediction"
5. 🎉 See ML-powered risk assessment!

---

## 🎨 Visual Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR BROWSER                             │
│              http://localhost:3000                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 NEXT.JS FRONTEND                            │
│  • Login Page    • Dashboard    • Submit Report            │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              NODE.JS BACKEND (Port 5000)                    │
│  • Authentication  • Data Aggregation  • API Routes        │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP POST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         🐍 PYTHON ML SERVICE (Port 5001) 🐍                 │
│                                                             │
│  ┌───────────────────────────────────────────────┐         │
│  │      Random Forest Classifier                 │         │
│  │      • 100 Decision Trees                     │         │
│  │      • 6 Features → 3 Risk Levels             │         │
│  │      • Confidence Scoring                     │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  Input: Symptoms, Sanitation, Rainfall, Villages           │
│  Output: Risk Level, Confidence, Disease, Explanation      │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              MONGODB (Port 27017)                           │
│  • Users  • Health Reports  • Predictions                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Quick Tests

### Test 1: Python Service Health
```bash
curl http://localhost:5001/health
```
**Expected:** `{"status": "healthy", "service": "ML Prediction Service"}`

### Test 2: Make a Prediction
```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"symptomCounts":{"diarrhea":20,"vomiting":10,"fever":6},"villageCount":3,"lowSanitationCount":2,"highRainfallCount":1}'
```

**Expected:**
```json
{
  "riskLevel": "HIGH",
  "confidenceScore": 87,
  "predictedDisease": "Cholera outbreak",
  "explanation": "ML Analysis: 20 diarrhea, 10 vomiting cases. 3 villages affected."
}
```

### Test 3: Full Integration
1. Submit 10 health reports via dashboard
2. Click "Run AI Prediction"
3. See color-coded risk card:
   - 🟢 GREEN = LOW risk
   - 🟡 YELLOW = MEDIUM risk
   - 🔴 RED = HIGH risk

---

## 🔄 Switch AI Providers

Want to use Gemini instead of Python ML?

**Edit `backend/.env`:**
```env
# Use Python ML (Default)
AI_PROVIDER=python

# OR use Gemini API
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key_here

# OR use OpenAI API
AI_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

**Restart Node.js backend** - that's it!

---

## 📁 Project Structure

```
TBP/
├── backend/
│   ├── ml-service/              ⭐ NEW!
│   │   ├── app.py              # Flask server
│   │   ├── model.py            # Random Forest
│   │   ├── requirements.txt    # Dependencies
│   │   ├── test_service.py     # Tests
│   │   └── README.md           # Docs
│   ├── services/
│   │   └── aiService.js        # ✏️ Updated
│   ├── .env                    # ✏️ Updated
│   └── start-all.bat           # ⭐ NEW!
├── frontend/
│   └── (unchanged)
├── PYTHON_ML_SETUP.md          # ⭐ NEW!
├── PYTHON_INTEGRATION_SUMMARY.md  # ⭐ NEW!
├── ARCHITECTURE_WITH_PYTHON.md    # ⭐ NEW!
├── PYTHON_ML_CHECKLIST.md         # ⭐ NEW!
├── IMPLEMENTATION_COMPLETE.md     # ⭐ NEW!
└── README.md                   # ✏️ Updated
```

**Legend:**
- ⭐ NEW! = Newly created
- ✏️ Updated = Modified existing file

---

## 🎯 What You Get

### Machine Learning Features
✅ Random Forest with 100 trees  
✅ 6 input features analyzed  
✅ 3 risk levels (LOW/MEDIUM/HIGH)  
✅ Confidence scoring (0-100%)  
✅ Disease prediction  
✅ Explanation generation  

### Architecture Benefits
✅ Microservice design  
✅ Scalable (deploy services separately)  
✅ Fast (< 500ms predictions)  
✅ Offline capable (no API needed)  
✅ Free (no API costs)  
✅ Customizable (retrain model)  

### Integration Features
✅ Seamless Node.js integration  
✅ Fallback to Gemini/OpenAI  
✅ Easy provider switching  
✅ Production ready  
✅ Error handling  
✅ CORS enabled  

---

## 🐛 Troubleshooting

### Python service won't start?
```bash
# Check Python version
python --version  # Need 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Try running directly
python app.py
```

### "Module not found" error?
```bash
pip install flask flask-cors scikit-learn numpy pandas
```

### Node.js can't connect to Python?
1. Check Python service: `curl http://localhost:5001/health`
2. Verify `.env` has: `PYTHON_ML_URL=http://localhost:5001`
3. Check firewall settings

### Port already in use?
```bash
# Find process using port 5001 (Windows)
netstat -ano | findstr :5001

# Kill process
taskkill /PID <process_id> /F
```

---

## 📚 Documentation

| File | Description |
|------|-------------|
| **[PYTHON_ML_SETUP.md](PYTHON_ML_SETUP.md)** | Complete setup guide |
| **[PYTHON_INTEGRATION_SUMMARY.md](PYTHON_INTEGRATION_SUMMARY.md)** | Integration details |
| **[ARCHITECTURE_WITH_PYTHON.md](ARCHITECTURE_WITH_PYTHON.md)** | Architecture diagrams |
| **[PYTHON_ML_CHECKLIST.md](PYTHON_ML_CHECKLIST.md)** | Verification checklist |
| **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** | Final summary |
| **[backend/ml-service/README.md](backend/ml-service/README.md)** | ML service docs |

---

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Python service starts (`python app.py`)
- [ ] Health check works (`curl http://localhost:5001/health`)
- [ ] Test script passes (`python test_service.py`)
- [ ] Node.js backend connects to Python
- [ ] Dashboard shows ML predictions
- [ ] Risk levels display correctly

---

## 🎉 You're Done!

Your Smart Health Surveillance System now uses **Machine Learning** for outbreak predictions!

**What's Running:**
- 🐍 Python ML Service (port 5001) - Random Forest model
- 🟢 Node.js Backend (port 5000) - API server
- ⚛️ Next.js Frontend (port 3000) - Dashboard
- 🍃 MongoDB (port 27017) - Database

**Test it now:**
1. Open http://localhost:3000
2. Login and submit health reports
3. Click "Run AI Prediction"
4. See ML-powered risk assessment! 🎯

---

## 🚀 Next Steps

### For Demo
- Submit diverse health reports
- Show different risk levels
- Explain ML confidence scores
- Demonstrate real-time predictions

### For Production
- Deploy Python service to Railway/Render
- Deploy Node.js to Railway/Render
- Deploy Frontend to Vercel
- Use MongoDB Atlas
- Set up monitoring

### For Improvement
- Add more training data
- Include more features
- Try different ML algorithms
- Implement model retraining
- Add prediction logging

---

**🎊 CONGRATULATIONS!**

**You've successfully integrated Python Machine Learning into your health surveillance system!**

**Status: READY FOR DEMO & DEPLOYMENT** ✨

---

**Built for SIH 2025**  
**Team: Sree Harsha, Jassmitha, Jaabily Srilekha**  
**Tech Stack: Next.js + Node.js + Python + MongoDB + scikit-learn**
