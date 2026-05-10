# 🏗️ System Architecture with Python ML

## Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                          │
│                    Next.js 14 (Port 3000)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Login Page   │  │  Dashboard   │  │Submit Report │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND LAYER (Node.js)                    │
│                    Express.js (Port 5000)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Auth Routes  │  │Report Routes │  │Predict Routes│         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │           AI Service (aiService.js)              │          │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │          │
│  │  │Python ML   │  │Gemini API  │  │OpenAI API  │ │          │
│  │  │(Default)   │  │(Optional)  │  │(Optional)  │ │          │
│  │  └─────┬──────┘  └────────────┘  └────────────┘ │          │
│  └────────┼─────────────────────────────────────────┘          │
└───────────┼─────────────────────────────────────────────────────┘
            │ HTTP POST
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PYTHON ML SERVICE LAYER                       │
│                    Flask (Port 5001)                            │
│  ┌──────────────────────────────────────────────────┐          │
│  │              app.py (Flask Server)               │          │
│  │  ┌────────────────┐      ┌────────────────┐     │          │
│  │  │ /health        │      │ /predict       │     │          │
│  │  │ Health Check   │      │ ML Prediction  │     │          │
│  │  └────────────────┘      └────────┬───────┘     │          │
│  └─────────────────────────────────────┼────────────┘          │
│                                        ▼                        │
│  ┌──────────────────────────────────────────────────┐          │
│  │         model.py (OutbreakPredictor)             │          │
│  │                                                   │          │
│  │  ┌─────────────────────────────────────────┐    │          │
│  │  │   Random Forest Classifier              │    │          │
│  │  │   • 100 Decision Trees                  │    │          │
│  │  │   • 6 Input Features                    │    │          │
│  │  │   • 3 Output Classes (LOW/MED/HIGH)     │    │          │
│  │  └─────────────────────────────────────────┘    │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
            │
            │ Returns Prediction
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                             │
│                   MongoDB (Port 27017)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │    Users     │  │HealthReports │  │ Predictions  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Prediction Request

```
1. User clicks "Run AI Prediction" on Dashboard
   │
   ▼
2. Frontend sends POST /api/predict to Node.js Backend
   │
   ▼
3. Node.js queries MongoDB for last 7 days of health reports
   │
   ▼
4. Node.js aggregates data:
   • Symptom counts (diarrhea, vomiting, fever)
   • Village count
   • Sanitation levels
   • Rainfall levels
   │
   ▼
5. Node.js sends aggregated data to Python ML Service
   POST http://localhost:5001/predict
   {
     "symptomCounts": {"diarrhea": 20, "vomiting": 10, "fever": 6},
     "villageCount": 3,
     "lowSanitationCount": 2,
     "highRainfallCount": 1
   }
   │
   ▼
6. Python Flask receives request
   │
   ▼
7. Random Forest Model processes 6 features
   • Feature extraction
   • Model prediction
   • Probability calculation
   │
   ▼
8. Python returns prediction
   {
     "riskLevel": "HIGH",
     "confidenceScore": 87,
     "predictedDisease": "Cholera outbreak",
     "explanation": "ML Analysis: 20 diarrhea, 10 vomiting cases..."
   }
   │
   ▼
9. Node.js saves prediction to MongoDB (OutbreakPrediction collection)
   │
   ▼
10. Node.js returns prediction to Frontend
   │
   ▼
11. Dashboard displays color-coded risk card
    • GREEN (LOW) / YELLOW (MEDIUM) / RED (HIGH)
    • Confidence score
    • Disease prediction
    • Explanation
```

---

## Component Responsibilities

### Frontend (Next.js)
- User authentication (JWT)
- Health report submission form
- Dashboard visualization (charts, cards)
- API communication with backend

### Backend (Node.js/Express)
- REST API endpoints
- JWT authentication & authorization
- MongoDB data operations
- Request validation (Joi)
- AI service orchestration
- Rate limiting & CORS

### Python ML Service (Flask)
- ML model hosting
- Feature extraction
- Random Forest predictions
- Confidence scoring
- REST API for predictions

### Database (MongoDB)
- User accounts storage
- Health reports storage
- Prediction history storage
- Indexing for fast queries

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND                                                    │
│ • Next.js 14 (React 18)                                     │
│ • Tailwind CSS                                              │
│ • Recharts (data visualization)                             │
│ • Axios (HTTP client)                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ BACKEND                                                     │
│ • Node.js + Express.js                                      │
│ • JWT (jsonwebtoken)                                        │
│ • bcryptjs (password hashing)                               │
│ • Joi (validation)                                          │
│ • Mongoose (MongoDB ODM)                                    │
│ • express-rate-limit                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ML SERVICE                                                  │
│ • Python 3.8+                                               │
│ • Flask (web framework)                                     │
│ • Flask-CORS                                                │
│ • scikit-learn (Random Forest)                              │
│ • NumPy (numerical computing)                               │
│ • Pandas (data manipulation)                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ DATABASE                                                    │
│ • MongoDB (NoSQL database)                                  │
│ • Collections: users, healthreports, outbreakpredictions    │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION DEPLOYMENT                    │
└─────────────────────────────────────────────────────────────┘

Frontend (Vercel/Netlify)
    ↓
Backend (Railway/Render/Heroku)
    ↓
Python ML Service (Railway/Render - Separate Container)
    ↓
MongoDB Atlas (Cloud Database)
```

---

## Security Features

```
┌─────────────────────────────────────────────────────────────┐
│ SECURITY LAYERS                                             │
├─────────────────────────────────────────────────────────────┤
│ 1. JWT Authentication (7-day expiry)                        │
│ 2. Password Hashing (bcryptjs, 10 rounds)                   │
│ 3. Role-Based Access Control (official, admin)              │
│ 4. Input Validation (Joi schemas)                           │
│ 5. Rate Limiting (100 requests/15 min)                      │
│ 6. CORS Protection (whitelist origins)                      │
│ 7. Environment Variables (.env)                             │
│ 8. HTTPS in Production                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Scalability Features

```
┌─────────────────────────────────────────────────────────────┐
│ SCALABILITY DESIGN                                          │
├─────────────────────────────────────────────────────────────┤
│ • Microservice Architecture (Node.js + Python separate)     │
│ • Stateless API (JWT tokens, no sessions)                   │
│ • Database Indexing (MongoDB indexes on date, district)     │
│ • Horizontal Scaling (multiple instances possible)          │
│ • Caching Ready (can add Redis)                             │
│ • Load Balancer Ready                                       │
│ • Container Ready (Docker support)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## ML Model Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ MACHINE LEARNING PIPELINE                                   │
└─────────────────────────────────────────────────────────────┘

Raw Health Data
    ↓
Feature Engineering
    • Symptom counts (diarrhea, vomiting, fever)
    • Environmental factors (sanitation, rainfall)
    • Geographic data (village count)
    ↓
Feature Vector [6 dimensions]
    ↓
Random Forest Classifier
    • 100 Decision Trees
    • Majority Voting
    • Probability Estimation
    ↓
Prediction Output
    • Risk Level (LOW/MEDIUM/HIGH)
    • Confidence Score (0-100%)
    • Disease Type
    • Explanation
    ↓
Store in Database + Display on Dashboard
```

---

**Architecture designed for:**
- ✅ High availability
- ✅ Easy maintenance
- ✅ Horizontal scaling
- ✅ Security best practices
- ✅ ML model flexibility
