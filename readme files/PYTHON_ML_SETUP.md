# 🐍 Python ML Integration Guide

## ✅ What Was Added

Your project now includes a **Python Flask microservice** with **Random Forest ML model** for disease outbreak prediction!

### New Files Created:
```
backend/
├── ml-service/
│   ├── app.py              # Flask API server
│   ├── model.py            # Random Forest classifier
│   ├── requirements.txt    # Python dependencies
│   ├── test_service.py     # Test script
│   └── README.md           # ML service docs
├── start-all.bat           # Start both services (Windows)
└── services/
    └── aiService.js        # Updated with Python integration
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Python Dependencies
```bash
cd backend/ml-service
pip install -r requirements.txt
```

### Step 2: Start Python ML Service
```bash
python app.py
```
✅ Service runs on **http://localhost:5001**

### Step 3: Start Node.js Backend (New Terminal)
```bash
cd backend
npm run dev
```
✅ Backend runs on **http://localhost:5000**

---

## 🎯 How It Works

### Architecture:
```
Frontend (Next.js)
    ↓ HTTP Request
Node.js Backend (Express) - Port 5000
    ↓ HTTP Request
Python ML Service (Flask) - Port 5001
    ↓ Random Forest Model
Risk Prediction Response
```

### Data Flow:
1. User clicks "Run AI Prediction" on dashboard
2. Frontend sends request to Node.js `/api/predict`
3. Node.js aggregates health reports from MongoDB
4. Node.js sends data to Python service `http://localhost:5001/predict`
5. Python Random Forest model analyzes 6 features
6. Returns: `{riskLevel, confidenceScore, predictedDisease, explanation}`
7. Node.js saves prediction to MongoDB
8. Frontend displays color-coded risk card

---

## 🧪 Test the ML Service

### Option 1: Python Test Script
```bash
cd backend/ml-service
python test_service.py
```

### Option 2: cURL
```bash
curl http://localhost:5001/health

curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d "{\"symptomCounts\":{\"diarrhea\":20,\"vomiting\":10},\"villageCount\":3}"
```

### Option 3: Use the Dashboard
1. Start both services
2. Login to frontend (http://localhost:3000)
3. Submit health reports
4. Click "Run AI Prediction"

---

## 🔄 Switch Between AI Providers

Edit `backend/.env`:

```env
# Use Python ML (Random Forest) - DEFAULT
AI_PROVIDER=python
PYTHON_ML_URL=http://localhost:5001

# OR use Gemini API
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key_here

# OR use OpenAI API
AI_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

---

## 📊 ML Model Details

### Algorithm: Random Forest Classifier
- **Estimators:** 100 decision trees
- **Random State:** 42 (reproducible results)
- **Classes:** 3 (LOW=0, MEDIUM=1, HIGH=2)

### Input Features (6):
1. Diarrhea cases count
2. Vomiting cases count
3. Fever cases count
4. Low sanitation count
5. High rainfall count
6. Affected villages count

### Output:
```json
{
  "riskLevel": "HIGH",
  "confidenceScore": 87,
  "predictedDisease": "Cholera outbreak",
  "explanation": "ML Analysis: 20 diarrhea, 10 vomiting cases. 3 villages affected."
}
```

### Training Data:
Pre-trained on 10 synthetic outbreak patterns covering:
- Low risk scenarios (5-10 cases)
- Medium risk scenarios (12-18 cases)
- High risk scenarios (20-30 cases)

---

## 🛠️ Troubleshooting

### Python service won't start?
```bash
# Check Python version (need 3.8+)
python --version

# Install dependencies
pip install -r requirements.txt

# Try running directly
cd backend/ml-service
python app.py
```

### "Module not found" error?
```bash
pip install flask flask-cors scikit-learn numpy pandas
```

### Port 5001 already in use?
Edit `backend/ml-service/app.py`:
```python
app.run(host='0.0.0.0', port=5002, debug=True)  # Change port
```
Then update `backend/.env`:
```env
PYTHON_ML_URL=http://localhost:5002
```

### Node.js can't connect to Python?
1. Verify Python service is running: `curl http://localhost:5001/health`
2. Check firewall settings
3. Ensure `PYTHON_ML_URL` in `.env` is correct

---

## 🚀 Easy Start (Windows)

Just run:
```bash
cd backend
start-all.bat
```

This starts both services automatically!

---

## 📈 Future Enhancements

Want to improve the model? Edit `backend/ml-service/model.py`:

1. **Add more training data** in `_train_model()`
2. **Add more features** (jaundice, abdominal pain, etc.)
3. **Try different algorithms** (XGBoost, Gradient Boosting)
4. **Load real dataset** from CSV file
5. **Add model persistence** with joblib

Example:
```python
import joblib

# Save trained model
joblib.dump(self.model, 'outbreak_model.pkl')

# Load model
self.model = joblib.load('outbreak_model.pkl')
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Python service starts without errors
- [ ] Health endpoint responds: `http://localhost:5001/health`
- [ ] Node.js backend connects to Python service
- [ ] Dashboard shows ML predictions
- [ ] `.env` has `AI_PROVIDER=python`

---

## 🎓 What You Learned

✅ Microservice architecture (Node.js + Python)  
✅ Random Forest classification  
✅ Flask REST API development  
✅ Inter-service HTTP communication  
✅ ML model integration in production  
✅ Feature engineering for health data  

---

**🎉 Python ML integration complete!**  
**Your system now uses scikit-learn Random Forest for predictions.**
