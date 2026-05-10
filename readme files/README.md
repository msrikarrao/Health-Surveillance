
# Smart Health Surveillance and Early Warning System

## 🎯 Problem Statement

This project proposes the development of a **Smart Health Surveillance and Early Warning System** that can detect, monitor, and help prevent outbreaks of water-borne diseases in vulnerable communities.

The system will:

* Collect health data from local clinics, ASHA workers, and community volunteers via mobile apps or SMS.
* Use AI/ML models to detect patterns and predict potential outbreaks based on symptoms, water quality reports, and seasonal trends.
* Integrate with water testing kits or IoT sensors to monitor water source contamination (e.g., turbidity, pH, bacterial presence).
* Provide real-time alerts to district health officials and local governance bodies.
* Include a multilingual mobile interface for community reporting and awareness campaigns.
* Offer dashboards for health departments to visualize hotspots, track interventions, and allocate resources.

---

## 🏥 Background

Water-borne diseases such as **diarrhea, cholera, typhoid, and hepatitis A** are widespread in rural and tribal areas of the Northeastern Region (NER), especially during monsoon seasons.

Challenges include:

* Contaminated water sources and poor sanitation infrastructure.
* Delayed medical response due to difficult terrain and remote villages.
* Limited real-time monitoring and data-driven decision-making.

A proactive system is needed to provide **early detection and quick response** to health threats.

---

## ✅ Implemented Solution

We have developed a **full-stack AI-powered health surveillance platform** that combines:

* **Mobile-Friendly Web App:** For data collection and community reporting
* **Python ML Engine:** Random Forest model for outbreak prediction
* **AI/ML Engine:** Detects outbreak patterns using Gemini/OpenAI API (alternative)
* **Real-time Dashboard:** Visualizes hotspots, risk levels, and health interventions
* **JWT Authentication:** Secure login for health officials
* **RESTful API:** Scalable backend architecture

---

## 🚀 Quick Start

### Prerequisites
- Node.js (v18+)
- Python (3.8+)
- MongoDB (local or Atlas)
- pip (Python package manager)

### Installation

```bash
# 1. Install backend dependencies
cd backend
npm install

# 2. Install Python ML service
cd ml-service
pip install -r requirements.txt
cd ..

# 3. Configure environment
# backend/.env is already configured for Python ML

# 4. Seed database with test data
npm run seed

# 5. Start both services (Windows)
start-all.bat

# OR start manually:
# Terminal 1: cd ml-service && python app.py
# Terminal 2: npm run dev

# 6. In a new terminal, install frontend dependencies
cd ../frontend
npm install

# 7. Start frontend (port 3000)
npm run dev
```

### Access the Application

1. Open browser: **http://localhost:3000**
2. Login with demo credentials:
   - **Email:** official@test.com
   - **Password:** password123
3. Submit health reports via "Submit Report" page
4. Click "Run AI Prediction" on Dashboard to see AI analysis

---

## 📁 Project Structure

```
TBP/
├── backend/              # Node.js + Express API
│   ├── ml-service/      # Python Flask ML service
│   │   ├── app.py      # Flask server
│   │   ├── model.py    # Random Forest model
│   │   └── requirements.txt
│   ├── models/          # MongoDB schemas
│   ├── routes/          # API endpoints
│   ├── services/        # AI integration
│   └── server.js        # Express app
├── frontend/            # Next.js 14 app
│   ├── app/            # Pages (login, dashboard, submit-report)
│   ├── components/     # React components
│   └── lib/            # API client
├── QUICKSTART.md       # Quick start guide
├── SETUP.md            # Detailed setup instructions
├── ARCHITECTURE.md     # System architecture diagrams
└── PROJECT_OVERVIEW.md # Complete documentation
```

---

## 🎯 Key Features

### ✅ Health Data Collection
- Multi-symptom reporting (diarrhea, fever, vomiting, jaundice, etc.)
- Water source tracking (well, river, tank, pipeline)
- Sanitation and rainfall level monitoring
- Village-level data aggregation

### ✅ AI-Powered Outbreak Prediction
- **Random Forest ML Model** (scikit-learn) - Primary prediction engine
- Weekly data analysis using Python microservice
- Alternative: Gemini/OpenAI API for natural language explanations
- Risk classification: **LOW** 🟢 | **MEDIUM** 🟡 | **HIGH** 🔴
- Confidence scoring (0-100%)
- Disease prediction (cholera, typhoid, hepatitis A, etc.)
- Feature importance analysis

### ✅ Real-time Dashboard
- Total cases (7-day window)
- Affected villages count
- Top symptoms bar chart (Recharts)
- Color-coded risk cards
- Historical predictions

### ✅ Security & Validation
- JWT authentication (7-day expiry)
- Password hashing (bcryptjs)
- Input validation (Joi schemas)
- Rate limiting (100 requests/15 min)
- CORS protection

---

## 🧠 How AI Prediction Works

1. **Data Collection:** System aggregates health reports from past 7 days
2. **Pattern Analysis:** Counts symptom frequency, water sources, sanitation levels
3. **ML Processing:** Node.js sends data to Python Flask service (port 5001)
4. **Random Forest Prediction:** Model analyzes 6 features and predicts risk level
5. **Risk Assessment:** Returns risk level, confidence score, and predicted disease
6. **Visualization:** Results displayed on dashboard with color-coded risk cards

**Architecture Flow:**
```
Frontend → Node.js Backend → Python ML Service (Random Forest) → Response
```

**Sample AI Response:**
```json
{
  "riskLevel": "HIGH",
  "confidenceScore": 87,
  "predictedDisease": "Cholera outbreak",
  "explanation": "High cluster of diarrhea cases in villages with contaminated water sources during monsoon season."
}
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js 14, React 18, Tailwind CSS |
| Backend | Node.js, Express.js |
| ML Service | Python, Flask, scikit-learn |
| ML Model | Random Forest Classifier |
| Database | MongoDB, Mongoose |
| Alternative AI | Gemini API / OpenAI API |
| Authentication | JWT, bcryptjs |
| Validation | Joi |
| Charts | Recharts |
| HTTP Client | Axios |

---

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Health Reports
- `POST /api/report` - Submit health report (auth required)
- `GET /api/reports?district=X&startDate=Y` - Get reports (auth required)

### Predictions
- `POST /api/predict` - Run AI prediction (auth required)
- `GET /api/predictions?district=X` - Get predictions (auth required)

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture diagrams
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete technical documentation
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details

---

## 🧪 Testing

### Automated Database Seeding
```bash
cd backend
npm run seed
```
This creates:
- Test user (official@test.com / password123)
- 8 sample health reports
- Ready for AI prediction

### Manual Testing
1. Login with demo credentials
2. Submit 5-10 health reports
3. Run AI prediction on dashboard
4. Verify risk level and explanation

---

## 🌐 Deployment

### Backend (Railway/Render/Heroku)
1. Set environment variables (MONGODB_URI, JWT_SECRET, GEMINI_API_KEY)
2. Deploy from GitHub
3. Update frontend API URL

### Frontend (Vercel/Netlify)
1. Set `NEXT_PUBLIC_API_URL` to production backend
2. Deploy from GitHub
3. Test authentication flow

---

## 👥 Team Members

* **Sree Harsha Chilukuri** – Team Lead, Backend Development (3rd Year, CSE-Core)
* **Jassmitha Jammu** – Dataset Creation, AI Model for Prediction (3rd Year, CSE-AIML)
* **Jaabily Srilekha** – Complete Figma Design & Documentation (3rd Year, CSE-Core)

### Helping Hands

* **Shreya Dutta** – Figma (2nd Year, CSE-Core)
* **Arjun Likith** – Documentation (2nd Year, ECE)

---

## 🎓 What We Built

✅ **30+ files** of production-ready code  
✅ **Full-stack application** (Frontend + Backend + Python ML)  
✅ **Random Forest ML model** for outbreak prediction  
✅ **Microservice architecture** (Node.js + Python)  
✅ **Complete documentation** (5+ markdown files)  
✅ **Database seeding** for instant testing  
✅ **Responsive design** for mobile/tablet/desktop  
✅ **Security best practices** (JWT, validation, rate limiting)  
✅ **Multiple AI providers** (Python ML, Gemini, OpenAI)  

---

## 🔧 Troubleshooting

**MongoDB connection error?**
→ Start MongoDB service or use MongoDB Atlas

**Python ML service not starting?**
→ Install dependencies: `pip install -r requirements.txt`

**ML prediction fails?**
→ Check Python service is running on port 5001

**Want to use Gemini instead?**
→ Change `AI_PROVIDER=gemini` in `backend/.env`

**Authentication error?**
→ Clear localStorage and login again

**Port already in use?**
→ Change PORT in `.env` files

---

## 📞 Support

For issues or questions:
1. Check console logs (browser F12 + terminal)
2. Verify environment variables
3. Review documentation files
4. Test API endpoints with Postman/curl

---

## 📄 License

MIT License - Free for educational and commercial use

---

## 🏆 Project Status

✅ **Backend:** 100% Complete  
✅ **Frontend:** 100% Complete  
✅ **AI Integration:** 100% Complete  
✅ **Documentation:** 100% Complete  
✅ **Testing:** Ready for demo  
✅ **Deployment:** Production-ready  

---

**🚀 Built for SIH 2025 - Smart Health Surveillance System**  
**Status: COMPLETE & READY FOR DEPLOYMENT**

---

## 🌟 Screenshots

### Login Page
Clean authentication interface with JWT token generation

### Dashboard
- Real-time statistics (total cases, affected villages)
- Color-coded AI risk predictions (GREEN/YELLOW/RED)
- Interactive symptom charts
- Weekly trend analysis

### Submit Report
- Multi-symptom selection
- Water source tracking
- Sanitation and rainfall monitoring
- Instant validation

---

**Site available at localhost:3000 after setup**