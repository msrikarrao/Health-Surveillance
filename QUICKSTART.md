# 🚀 QUICK START GUIDE

## Step 1: Install Backend Dependencies

```bash
cd backend
npm install
```

## Step 2: Configure Backend

1. Get Gemini API Key from: https://makersuite.google.com/app/apikey
2. Edit `backend/.env` and add your API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

## Step 3: Start MongoDB

**Windows:**
```bash
net start MongoDB
```

**Mac/Linux:**
```bash
sudo systemctl start mongod
```

**Don't have MongoDB?** Use MongoDB Atlas (free cloud):
- Sign up at https://www.mongodb.com/cloud/atlas
- Create cluster → Get connection string
- Update `MONGODB_URI` in `backend/.env`

## Step 4: Start Backend

```bash
cd backend
npm run dev
```

✅ Backend running at: http://localhost:5000

## Step 5: Install Frontend Dependencies

Open NEW terminal:

```bash
cd frontend
npm install
```

## Step 6: Start Frontend

```bash
npm run dev
```

✅ Frontend running at: http://localhost:3000

## Step 7: Test the Application

1. Open browser: http://localhost:3000
2. Login with demo credentials:
   - Email: `official@test.com`
   - Password: `password123`

**First time?** Register a new account instead.

3. Submit 5-10 health reports via "Submit Report" page
4. Go to Dashboard
5. Click "Run AI Prediction"
6. View AI-generated outbreak risk analysis!

## 📊 Sample Data for Testing

Use these values when submitting reports:

**Report 1:**
- Village: Guwahati Village
- Age: 25
- Symptoms: diarrhea, fever, vomiting
- Water Source: well
- Cases: 3
- Sanitation: low
- Rainfall: high

**Report 2:**
- Village: Dispur Village
- Age: 35
- Symptoms: diarrhea, abdominal_pain
- Water Source: river
- Cases: 5
- Sanitation: low
- Rainfall: high

**Report 3:**
- Village: Guwahati Village
- Age: 12
- Symptoms: fever, vomiting
- Water Source: well
- Cases: 2
- Sanitation: medium
- Rainfall: high

Submit at least 5 reports, then run AI prediction!

## 🔧 Troubleshooting

**"Cannot connect to MongoDB"**
→ Start MongoDB service or use MongoDB Atlas

**"AI prediction failed"**
→ Check your Gemini API key in `backend/.env`

**"Please authenticate"**
→ Login again, token may have expired

**Port already in use**
→ Kill process or change port in `.env` files

## 🎯 What to Expect

After running AI prediction, you'll see:
- **Risk Level:** LOW / MEDIUM / HIGH (color-coded)
- **Confidence Score:** 0-100%
- **Predicted Disease:** e.g., "Cholera outbreak"
- **AI Explanation:** Why this prediction was made
- **Charts:** Symptom distribution and affected villages

## 📱 Features

✅ JWT Authentication
✅ Health Report Submission
✅ AI-Powered Outbreak Prediction (Gemini/OpenAI)
✅ Real-time Dashboard
✅ Weekly Trend Analysis
✅ Risk Level Classification
✅ Responsive Design

## 🔐 Default Credentials

**Email:** official@test.com  
**Password:** password123  
**District:** Kamrup

## 📚 Full Documentation

See `SETUP.md` for complete setup instructions, API documentation, and deployment guide.

---

**Need Help?** Check console logs in browser (F12) and terminal for error messages.
