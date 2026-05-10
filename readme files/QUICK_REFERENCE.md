# ⚡ Quick Reference Guide
## Smart Health Surveillance System

**Purpose:** One-page reference for common tasks and commands  
**Audience:** Developers, DevOps, QA

---

## 🚀 Quick Start (5 minutes)

### Setup
```bash
# Backend
cd backend && npm install
cd ml-service && pip install -r requirements.txt
cd ..

# Frontend
cd ../frontend && npm install
```

### Seed Database
```bash
cd backend
npm run seed
```

### Run Services
```bash
# Terminal 1: Python ML
cd backend/ml-service && python app.py

# Terminal 2: Node Backend
cd backend && npm run dev

# Terminal 3: Frontend
cd frontend && npm run dev
```

### Access Application
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5000
- **ML Service:** http://localhost:5001
- **Login:** `official@test.com` / `password123`

---

## 📂 Key Files Reference

| File | Purpose | Edit For |
|------|---------|----------|
| `backend/server.js` | Express server | Server config |
| `backend/models/HealthReport.js` | Report schema | Data structure |
| `backend/routes/predictions.js` | Prediction API | Prediction logic |
| `backend/ml-service/model.py` | ML model | Model training |
| `frontend/app/dashboard/page.js` | Dashboard | UI changes |
| `frontend/lib/api.js` | API client | API calls |
| `.env` | Environment variables | Config |

---

## 🔑 Environment Variables

### Backend (.env)
```env
MONGODB_URI=mongodb://localhost:27017/health_surveillance_db
JWT_SECRET=your-secret-key
AI_PROVIDER=python
PYTHON_ML_URL=http://localhost:5001
PORT=5000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Python ML (.env)
```env
PORT=5001
DEBUG=true
```

---

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/register   - Create user
POST   /api/auth/login      - Login user
```

### Health Reports
```
POST   /api/report          - Submit report
GET    /api/reports         - Get reports (filtered)
```

### Predictions
```
POST   /api/predict         - Generate prediction
GET    /api/predictions     - Get predictions
```

### Health Check
```
GET    /api/health          - Backend health
GET    /api/ml-health       - ML service health
```

---

## 🧪 Testing Commands

### Quick Tests
```bash
# Seed data
npm run seed

# Test ML service
cd backend/ml-service && python test_service.py

# Test API
curl http://localhost:5000/api/health
```

### Full Test
1. Open http://localhost:3000
2. Login: `official@test.com` / `password123`
3. Submit report
4. Run AI prediction
5. Verify dashboard

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| MongoDB won't connect | Start MongoDB: `mongod` |
| Port 5000 in use | Kill process: `lsof -i :5000` or change PORT in .env |
| ML service not responding | Check Python running on 5001: `python app.py` |
| Frontend not loading | Clear cache: `npm cache clean --force` |
| JWT token expired | Login again |
| Prediction fails | Check ML service health: http://localhost:5001/health |

---

## 📊 Database Queries

### MongoDB CLI
```javascript
// Connect
mongosh

// Switch database
use health_surveillance_db

// View collections
show collections

// Check data
db.users.find()
db.healthreports.find({district: "Assam"})
db.outbreakpredictions.find({}).sort({_id: -1}).limit(1)

// Count records
db.healthreports.countDocuments()

// Clear collection
db.healthreports.deleteMany({})
```

---

## 🚢 Deployment Quick Commands

### Docker
```bash
# Build
docker build -t my-app ./backend

# Run
docker run -p 5000:5000 my-app

# Docker Compose
docker-compose up -d
docker-compose down
```

### Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up

# View logs
railway logs
```

### Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# View logs
vercel logs
```

---

## 📝 Git Commands

### Commit Changes
```bash
git add .
git commit -m "Feature: Add new feature"
git push origin main
```

### Branch Management
```bash
git checkout -b feature/new-feature
git commit -m "Changes"
git push origin feature/new-feature
# Then create pull request
```

### View History
```bash
git log --oneline
git diff HEAD~1
git show <commit-hash>
```

---

## 🔒 Security Checklist

- [ ] No hardcoded credentials in code
- [ ] All secrets in .env files
- [ ] JWT token being used for auth
- [ ] Passwords hashed (bcrypt)
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Input validation active
- [ ] SSL/TLS in production

---

## 📚 Documentation Map

| Document | Read For |
|----------|----------|
| README.md | Project overview |
| QUICKSTART.md | 5-minute setup |
| SETUP.md | Detailed setup |
| ARCHITECTURE.md | System design |
| PROBLEM_STATEMENT_MAPPING.md | Requirements |
| TESTING_AND_VERIFICATION_GUIDE.md | Testing steps |
| PRODUCTION_DEPLOYMENT_GUIDE.md | Production setup |
| PROJECT_STATUS_REPORT.md | Project status |

---

## 🎯 Feature Status

| Feature | Status | Endpoint |
|---------|--------|----------|
| Health Report | ✅ Complete | POST /api/report |
| User Auth | ✅ Complete | POST /api/auth/login |
| AI Prediction | ✅ Complete | POST /api/predict |
| Dashboard | ✅ Complete | http://localhost:3000/dashboard |
| Real Alerts | ✅ Complete | Dashboard display |
| Mobile UI | ✅ Complete | All pages |
| Water Sensors | ⚠️ Ready | Schema prepared |
| Email Alerts | ⚠️ Ready | Service ready |

---

## 💡 Common Tasks

### Add New API Endpoint
1. Create route in `backend/routes/`
2. Add schema validation in route
3. Test with curl
4. Document in API section

### Add New Database Field
1. Update schema in `backend/models/`
2. Add migration if needed
3. Update validation schemas
4. Update frontend form
5. Test with test data

### Deploy to Production
1. Follow PRODUCTION_DEPLOYMENT_GUIDE.md
2. Set environment variables
3. Run tests
4. Deploy backend
5. Deploy frontend
6. Verify endpoints

---

## 🔗 Useful Links

- **MongoDB Docs:** https://docs.mongodb.com
- **Express Docs:** https://expressjs.com
- **Next.js Docs:** https://nextjs.org/docs
- **Python Docs:** https://python.org/docs
- **scikit-learn:** https://scikit-learn.org

---

## 📞 Quick Help

**For Setup Issues:**
→ See QUICKSTART.md or SETUP.md

**For Testing:**
→ See TESTING_AND_VERIFICATION_GUIDE.md

**For Deployment:**
→ See PRODUCTION_DEPLOYMENT_GUIDE.md

**For Architecture:**
→ See ARCHITECTURE.md

**For Requirements:**
→ See PROBLEM_STATEMENT_MAPPING.md

---

**Last Updated:** April 2026  
**Version:** 1.0  
**Status:** ✅ Production-Ready
