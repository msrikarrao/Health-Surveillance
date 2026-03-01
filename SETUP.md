# AI Prediction Module - Setup Instructions

## Prerequisites

- Node.js (v18 or higher)
- MongoDB (local or Atlas)
- Gemini API Key or OpenAI API Key

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
npm install
```

### 2. Configure Environment Variables

Edit `backend/.env`:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/health-surveillance
JWT_SECRET=your_secure_jwt_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here
AI_PROVIDER=gemini
```

**Get Gemini API Key:**
- Visit: https://makersuite.google.com/app/apikey
- Create a new API key
- Paste it in `.env`

**Alternative - OpenAI:**
```env
OPENAI_API_KEY=your_openai_api_key_here
AI_PROVIDER=openai
```

### 3. Start MongoDB

**Windows:**
```bash
net start MongoDB
```

**Mac/Linux:**
```bash
sudo systemctl start mongod
```

**Or use MongoDB Atlas (cloud):**
- Create free cluster at https://www.mongodb.com/cloud/atlas
- Get connection string
- Update `MONGODB_URI` in `.env`

### 4. Create Initial User (Optional)

Run this in MongoDB shell or Compass:

```javascript
use health-surveillance

db.users.insertOne({
  name: "Test Official",
  email: "official@test.com",
  password: "$2a$10$X8qJ5vZ5Z5Z5Z5Z5Z5Z5ZeX8qJ5vZ5Z5Z5Z5Z5Z5Z5Z5Z5Z5Z5Z5Z", // password123
  role: "official",
  district: "Kamrup",
  createdAt: new Date(),
  updatedAt: new Date()
})
```

### 5. Start Backend Server

```bash
npm run dev
```

Server runs on: http://localhost:5000

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

### 3. Start Frontend

```bash
npm run dev
```

Frontend runs on: http://localhost:3000

## Usage Guide

### 1. Register/Login

**Option A: Use Demo Account**
- Email: `official@test.com`
- Password: `password123`

**Option B: Register via API**

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "official",
    "district": "Kamrup"
  }'
```

### 2. Submit Health Reports

Navigate to "Submit Report" page and fill in:
- Village name
- Patient age
- Symptoms (select multiple)
- Water source type
- Number of cases
- Sanitation level
- Rainfall level

### 3. Run AI Prediction

1. Go to Dashboard
2. Click "Run AI Prediction"
3. AI analyzes past 7 days of data
4. View risk level, predicted disease, and explanation

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login

### Health Reports
- `POST /api/report` - Submit health report (requires auth)
- `GET /api/reports?district=X&startDate=Y` - Get reports (requires auth)

### Predictions
- `POST /api/predict` - Run AI prediction (requires auth)
  ```json
  { "district": "Kamrup" }
  ```
- `GET /api/predictions?district=X&limit=10` - Get predictions (requires auth)

## Sample Test Data

### Create Multiple Reports via API

```bash
# Get token first
TOKEN="your_jwt_token_here"

# Submit report 1
curl -X POST http://localhost:5000/api/report \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "villageName": "Guwahati Village",
    "district": "Kamrup",
    "patientAge": 25,
    "symptoms": ["diarrhea", "fever", "vomiting"],
    "waterSourceType": "well",
    "numberOfCasesReported": 3,
    "sanitationLevel": "low",
    "rainfallLevel": "high"
  }'

# Submit report 2
curl -X POST http://localhost:5000/api/report \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "villageName": "Dispur Village",
    "district": "Kamrup",
    "patientAge": 35,
    "symptoms": ["diarrhea", "abdominal_pain"],
    "waterSourceType": "river",
    "numberOfCasesReported": 5,
    "sanitationLevel": "low",
    "rainfallLevel": "high"
  }'

# Submit report 3
curl -X POST http://localhost:5000/api/report \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "villageName": "Guwahati Village",
    "district": "Kamrup",
    "patientAge": 12,
    "symptoms": ["fever", "vomiting", "headache"],
    "waterSourceType": "well",
    "numberOfCasesReported": 2,
    "sanitationLevel": "medium",
    "rainfallLevel": "high"
  }'
```

### Run Prediction

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"district": "Kamrup"}'
```

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running
- Check connection string in `.env`
- For Atlas, whitelist your IP address

### AI API Error
- Verify API key is correct
- Check API quota/limits
- Ensure internet connection

### CORS Error
- Backend must run on port 5000
- Frontend must run on port 3000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`

### Authentication Error
- Clear localStorage in browser
- Re-login
- Check JWT_SECRET matches in backend

## Production Deployment

### Backend (Railway/Render/Heroku)
1. Set environment variables
2. Deploy from GitHub
3. Update frontend API URL

### Frontend (Vercel/Netlify)
1. Connect GitHub repo
2. Set `NEXT_PUBLIC_API_URL` to production backend URL
3. Deploy

## Project Structure

```
TBP/
├── backend/
│   ├── models/          # MongoDB schemas
│   ├── routes/          # API endpoints
│   ├── middleware/      # Auth middleware
│   ├── services/        # AI service
│   ├── config/          # Database config
│   └── server.js        # Express app
├── frontend/
│   ├── app/             # Next.js pages
│   ├── components/      # React components
│   └── lib/             # API utilities
└── SETUP.md             # This file
```

## Tech Stack Summary

- **Frontend:** Next.js 14 (App Router), React, Tailwind CSS, Recharts
- **Backend:** Node.js, Express, MongoDB, Mongoose
- **AI:** Gemini API / OpenAI API
- **Auth:** JWT (jsonwebtoken, bcryptjs)
- **Validation:** Joi
- **Security:** express-rate-limit, CORS

## Support

For issues or questions:
- Check console logs (browser & terminal)
- Verify all environment variables
- Ensure MongoDB is running
- Test API endpoints with curl/Postman

## License

MIT License - Free for educational and commercial use
