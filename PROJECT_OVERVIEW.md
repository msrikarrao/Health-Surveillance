# AI Prediction Module - Project Overview

## 🎯 Project Summary

A full-stack **Smart Health Surveillance and Early Warning System** that uses AI to predict water-borne disease outbreaks in rural communities.

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Next.js       │         │   Express.js    │         │   Gemini/       │
│   Frontend      │ ◄─────► │   Backend       │ ◄─────► │   OpenAI API    │
│   (Port 3000)   │   REST  │   (Port 5000)   │   HTTP  │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   MongoDB       │
                            │   Database      │
                            └─────────────────┘
```

## 📁 Project Structure

```
TBP/
├── backend/                    # Node.js + Express API
│   ├── config/
│   │   └── db.js              # MongoDB connection
│   ├── models/
│   │   ├── User.js            # User authentication model
│   │   ├── HealthReport.js    # Health data model
│   │   └── OutbreakPrediction.js  # AI prediction results
│   ├── routes/
│   │   ├── auth.js            # Login/Register endpoints
│   │   ├── reports.js         # Health report CRUD
│   │   └── predictions.js     # AI prediction endpoints
│   ├── middleware/
│   │   └── auth.js            # JWT authentication
│   ├── services/
│   │   └── aiService.js       # AI API integration (Gemini/OpenAI)
│   ├── .env                   # Environment variables
│   ├── server.js              # Express app entry point
│   ├── seed.js                # Database seeding script
│   └── package.json
│
├── frontend/                   # Next.js 14 (App Router)
│   ├── app/
│   │   ├── login/
│   │   │   └── page.js        # Login page
│   │   ├── dashboard/
│   │   │   └── page.js        # Main dashboard with AI predictions
│   │   ├── submit-report/
│   │   │   └── page.js        # Health report submission form
│   │   ├── layout.js          # Root layout
│   │   ├── page.js            # Home page (redirects)
│   │   └── globals.css        # Tailwind CSS
│   ├── components/
│   │   ├── Navbar.js          # Navigation component
│   │   └── RiskCard.js        # AI prediction display
│   ├── lib/
│   │   └── api.js             # Axios API client
│   ├── .env.local             # Frontend environment
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── next.config.js
│
├── QUICKSTART.md              # Quick start guide
├── SETUP.md                   # Detailed setup instructions
├── test-data.json             # Sample test data
└── README.md                  # Project documentation
```

## 🔄 Data Flow

### 1. Health Report Submission
```
User → Submit Report Form → POST /api/report → MongoDB (HealthReport)
```

### 2. AI Prediction Process
```
User clicks "Run AI Prediction"
    ↓
GET /api/reports (last 7 days)
    ↓
Aggregate data (symptom counts, villages, water sources)
    ↓
POST /api/predict
    ↓
AI Service formats prompt
    ↓
Call Gemini/OpenAI API
    ↓
Parse JSON response
    ↓
Save to MongoDB (OutbreakPrediction)
    ↓
Display on Dashboard (RiskCard component)
```

## 🧠 AI Prediction Logic

### Input Data (Aggregated Weekly)
```javascript
{
  totalCases: 32,
  villages: ["Guwahati Village", "Dispur Village", "Beltola Village"],
  villageCount: 3,
  symptomCounts: {
    diarrhea: 18,
    fever: 12,
    vomiting: 10,
    abdominal_pain: 8
  },
  waterSources: {
    well: 4,
    river: 2,
    tank: 2
  },
  lowSanitationCount: 5,
  highRainfallCount: 6,
  reportCount: 8
}
```

### AI Prompt Template
```
You are a public health epidemiologist analyzing rural disease data.

Here is weekly aggregated health data in JSON format:
{aggregated_data}

Analyze patterns and detect outbreak risk.

Respond ONLY in this JSON format:
{
  "riskLevel": "LOW | MEDIUM | HIGH",
  "confidenceScore": number,
  "predictedDisease": "string",
  "explanation": "short explanation"
}
```

### Output
```javascript
{
  riskLevel: "HIGH",
  confidenceScore: 87,
  predictedDisease: "Cholera outbreak",
  explanation: "High cluster of diarrhea and vomiting cases in villages with contaminated water sources during monsoon season with poor sanitation."
}
```

## 🔐 Authentication Flow

```
1. User registers/logs in → POST /api/auth/login
2. Backend validates credentials
3. JWT token generated (7-day expiry)
4. Token stored in localStorage
5. All API requests include: Authorization: Bearer {token}
6. Middleware validates token on protected routes
```

## 📊 Database Schema

### User Collection
```javascript
{
  name: String,
  email: String (unique),
  password: String (hashed),
  role: "official" | "admin",
  district: String,
  createdAt: Date,
  updatedAt: Date
}
```

### HealthReport Collection
```javascript
{
  villageName: String,
  district: String,
  patientAge: Number,
  symptoms: [String],
  date: Date,
  waterSourceType: "well" | "river" | "tank" | "pipeline",
  numberOfCasesReported: Number,
  sanitationLevel: "low" | "medium" | "high",
  rainfallLevel: "low" | "medium" | "high",
  reportedBy: ObjectId (ref: User),
  createdAt: Date,
  updatedAt: Date
}
```

### OutbreakPrediction Collection
```javascript
{
  district: String,
  weekStart: Date,
  weekEnd: Date,
  riskLevel: "LOW" | "MEDIUM" | "HIGH",
  confidenceScore: Number (0-100),
  predictedDisease: String,
  explanation: String,
  totalCases: Number,
  affectedVillages: [String],
  dataSnapshot: Object,
  createdAt: Date,
  updatedAt: Date
}
```

## 🎨 Frontend Components

### Pages
- **Login Page** (`/login`) - JWT authentication
- **Dashboard** (`/dashboard`) - AI predictions, charts, statistics
- **Submit Report** (`/submit-report`) - Health data collection form

### Components
- **Navbar** - Navigation with user info and logout
- **RiskCard** - Color-coded AI prediction display (GREEN/YELLOW/RED)

### Charts (Recharts)
- Bar chart showing symptom distribution
- Weekly trend analysis

## 🔧 Key Features

✅ **JWT Authentication** - Secure login for health officials  
✅ **Health Report Submission** - Multi-symptom data collection  
✅ **AI-Powered Predictions** - Gemini/OpenAI integration  
✅ **Risk Classification** - LOW/MEDIUM/HIGH with confidence scores  
✅ **Real-time Dashboard** - Weekly statistics and trends  
✅ **Responsive Design** - Tailwind CSS, mobile-friendly  
✅ **Input Validation** - Joi schema validation  
✅ **Rate Limiting** - API protection (100 req/15min)  
✅ **Error Handling** - Comprehensive error messages  

## 🚀 Deployment Checklist

### Backend (Railway/Render/Heroku)
- [ ] Set environment variables (MONGODB_URI, JWT_SECRET, GEMINI_API_KEY)
- [ ] Connect MongoDB Atlas
- [ ] Deploy from GitHub
- [ ] Test API endpoints

### Frontend (Vercel/Netlify)
- [ ] Set NEXT_PUBLIC_API_URL to production backend
- [ ] Connect GitHub repo
- [ ] Deploy
- [ ] Test authentication flow

## 🧪 Testing Strategy

### Manual Testing
1. Register new user
2. Submit 5-10 health reports
3. Run AI prediction
4. Verify risk level and explanation
5. Check dashboard charts

### API Testing (Postman/curl)
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"official@test.com","password":"password123"}'

# Submit Report
curl -X POST http://localhost:5000/api/report \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{...report_data...}'

# Run Prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"district":"Kamrup"}'
```

## 📈 Performance Considerations

- **Rate Limiting**: 100 requests per 15 minutes
- **Database Indexing**: Index on `district`, `date` fields
- **AI API Caching**: Consider caching predictions for same data
- **Pagination**: Limit reports to 100 per query
- **Lazy Loading**: Charts load only when data available

## 🔒 Security Features

- Password hashing (bcryptjs)
- JWT token authentication
- CORS protection
- Input validation (Joi)
- Rate limiting
- Environment variable protection
- No sensitive data in frontend

## 🌐 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📝 Environment Variables

### Backend (.env)
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/health-surveillance
JWT_SECRET=your_secure_secret
GEMINI_API_KEY=your_api_key
AI_PROVIDER=gemini
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

## 🎓 Learning Resources

- **Next.js 14**: https://nextjs.org/docs
- **Express.js**: https://expressjs.com/
- **MongoDB**: https://www.mongodb.com/docs/
- **Gemini API**: https://ai.google.dev/docs
- **Tailwind CSS**: https://tailwindcss.com/docs

## 👥 Team Roles

- **Backend Development**: Express API, MongoDB, AI integration
- **Frontend Development**: Next.js, React components, UI/UX
- **AI/ML**: Prompt engineering, prediction logic
- **Documentation**: Setup guides, API docs

## 📞 Support

For issues:
1. Check console logs (browser F12 + terminal)
2. Verify environment variables
3. Test API endpoints individually
4. Check MongoDB connection
5. Verify AI API key and quota

---

**Built with ❤️ for SIH 2025 - Smart Health Surveillance System**
