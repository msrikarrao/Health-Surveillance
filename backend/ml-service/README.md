# Python ML Prediction Service

## 🤖 Random Forest Model for Outbreak Prediction

This microservice uses **scikit-learn Random Forest Classifier** to predict disease outbreak risk levels.

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
cd backend/ml-service
pip install -r requirements.txt
```

### 2. Start ML Service

```bash
python app.py
```

Service runs on **http://localhost:5001**

### 3. Test the Service

```bash
curl http://localhost:5001/health
```

## 📊 How It Works

### Input Features:
- Diarrhea cases count
- Vomiting cases count  
- Fever cases count
- Low sanitation count
- High rainfall count
- Affected villages count

### Output:
```json
{
  "riskLevel": "HIGH",
  "confidenceScore": 87,
  "predictedDisease": "Cholera outbreak",
  "explanation": "ML Analysis: 25 diarrhea, 12 vomiting cases. 3 villages affected."
}
```

## 🔄 Integration

Node.js backend automatically calls this service when `AI_PROVIDER=python` in `.env`

## 🎯 Model Details

- **Algorithm:** Random Forest Classifier
- **Estimators:** 100 trees
- **Classes:** LOW (0), MEDIUM (1), HIGH (2)
- **Training:** Pre-trained on outbreak patterns

## 🔧 Switch Between AI Providers

Edit `backend/.env`:
- `AI_PROVIDER=python` → Use Random Forest ML
- `AI_PROVIDER=gemini` → Use Gemini API
- `AI_PROVIDER=openai` → Use OpenAI API
