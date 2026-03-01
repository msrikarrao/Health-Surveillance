# 🔐 Google OAuth Setup Guide

## Prerequisites

1. **Google Cloud Console Account**
2. **OAuth 2.0 Client ID**

---

## Step 1: Create Google OAuth Credentials

### 1. Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 2. Create a New Project (or select existing)
- Click "Select a project" → "New Project"
- Name: "Health Surveillance System"
- Click "Create"

### 3. Enable Google+ API
- Go to "APIs & Services" → "Library"
- Search for "Google+ API"
- Click "Enable"

### 4. Create OAuth Consent Screen
- Go to "APIs & Services" → "OAuth consent screen"
- Select "External" → Click "Create"
- Fill in:
  - App name: Health Surveillance System
  - User support email: your-email@gmail.com
  - Developer contact: your-email@gmail.com
- Click "Save and Continue"
- Skip Scopes → "Save and Continue"
- Add test users (your email) → "Save and Continue"

### 5. Create OAuth Client ID
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "OAuth client ID"
- Application type: "Web application"
- Name: "Health Surveillance Web Client"
- Authorized JavaScript origins:
  - http://localhost:3000
  - http://localhost:5000
- Authorized redirect URIs:
  - http://localhost:5000/api/auth/google/callback
  - http://localhost:3000/auth/callback
- Click "Create"

### 6. Copy Credentials
- Copy **Client ID** (looks like: xxxxx.apps.googleusercontent.com)
- Copy **Client Secret**

---

## Step 2: Install Dependencies

### Backend
```bash
cd backend
npm install passport passport-google-oauth20 express-session
```

### Frontend
```bash
cd frontend
npm install @react-oauth/google
```

---

## Step 3: Configure Environment Variables

### Backend `.env`
Add these lines:
```env
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_CALLBACK_URL=http://localhost:5000/api/auth/google/callback
SESSION_SECRET=your_random_session_secret_here
```

### Frontend `.env.local`
Add this line:
```env
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
```

---

## Step 4: Test Google Login

1. Start backend: `cd backend && npm run dev`
2. Start frontend: `cd frontend && npm run dev`
3. Go to: http://localhost:3000/login
4. Click "Sign in with Google"
5. Select your Google account
6. Should redirect to dashboard

---

## Troubleshooting

### Error: "redirect_uri_mismatch"
- Check authorized redirect URIs in Google Console
- Must exactly match: http://localhost:5000/api/auth/google/callback

### Error: "Access blocked"
- Add your email to test users in OAuth consent screen
- App must be in "Testing" mode

### Error: "Invalid client"
- Verify GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
- Check they match Google Console credentials

---

## Production Deployment

### Update Authorized Origins
Add your production URLs:
- https://yourdomain.com
- https://api.yourdomain.com

### Update Redirect URIs
- https://api.yourdomain.com/api/auth/google/callback
- https://yourdomain.com/auth/callback

### Update Environment Variables
- Set production GOOGLE_CALLBACK_URL
- Use secure SESSION_SECRET

---

## Security Notes

- ✅ Never commit `.env` files to Git
- ✅ Use different credentials for dev/prod
- ✅ Rotate secrets regularly
- ✅ Enable 2FA on Google account
- ✅ Monitor OAuth usage in Google Console

---

**🎉 Google OAuth is now configured!**
