# System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Next.js Frontend)                         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Login Page   │  │  Dashboard   │  │Submit Report │        │
│  │              │  │              │  │              │        │
│  │ - Email      │  │ - Statistics │  │ - Form       │        │
│  │ - Password   │  │ - AI Results │  │ - Validation │        │
│  │ - JWT Token  │  │ - Charts     │  │ - Submit     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │ REST API (Axios)
                         │ Authorization: Bearer {JWT}
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API SERVER                         │
│                    (Express.js + Node.js)                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    MIDDLEWARE LAYER                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │   CORS     │  │Rate Limiter│  │    JWT     │         │  │
│  │  │ Protection │  │100 req/15m │  │   Auth     │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      ROUTES LAYER                         │  │
│  │                                                           │  │
│  │  /api/auth/*          /api/report          /api/predict  │  │
│  │  ├─ POST /register    ├─ POST /report      ├─ POST /     │  │
│  │  └─ POST /login       └─ GET /reports      └─ GET /      │  │
│  │                                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    BUSINESS LOGIC                         │  │
│  │                                                           │  │
│  │  ┌─────────────────┐         ┌─────────────────┐        │  │
│  │  │  Joi Validation │         │   AI Service    │        │  │
│  │  │  - Schema check │         │  - Aggregation  │        │  │
│  │  │  - Data types   │         │  - Prompt build │        │  │
│  │  └─────────────────┘         │  - API call     │        │  │
│  │                              │  - Parse JSON   │        │  │
│  │                              └─────────────────┘        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└────────────┬────────────────────────────────┬───────────────────┘
             │                                │
             ▼                                ▼
┌─────────────────────────┐    ┌─────────────────────────────────┐
│   MongoDB Database      │    │   External AI API               │
│                         │    │                                 │
│  ┌──────────────────┐   │    │  ┌──────────────────────────┐  │
│  │ users            │   │    │  │  Gemini API              │  │
│  │ - name           │   │    │  │  (Google AI)             │  │
│  │ - email          │   │    │  │                          │  │
│  │ - password       │   │    │  │  OR                      │  │
│  │ - role           │   │    │  │                          │  │
│  │ - district       │   │    │  │  OpenAI API              │  │
│  └──────────────────┘   │    │  │  (GPT-3.5/4)             │  │
│                         │    │  └──────────────────────────┘  │
│  ┌──────────────────┐   │    │                                 │
│  │ healthreports    │   │    │  Input: Aggregated health data  │
│  │ - villageName    │   │    │  Output: JSON prediction        │
│  │ - district       │   │    │  {                              │
│  │ - symptoms[]     │   │    │    riskLevel,                   │
│  │ - waterSource    │   │    │    confidenceScore,             │
│  │ - sanitation     │   │    │    predictedDisease,            │
│  │ - rainfall       │   │    │    explanation                  │
│  │ - date           │   │    │  }                              │
│  └──────────────────┘   │    └─────────────────────────────────┘
│                         │
│  ┌──────────────────┐   │
│  │ outbreakpredictions│ │
│  │ - district       │   │
│  │ - riskLevel      │   │
│  │ - confidence     │   │
│  │ - disease        │   │
│  │ - explanation    │   │
│  │ - weekStart/End  │   │
│  └──────────────────┘   │
└─────────────────────────┘
```

## Data Flow Sequence

### 1. User Authentication Flow
```
User → Login Form → POST /api/auth/login
                         ↓
                    Validate credentials
                         ↓
                    Generate JWT token
                         ↓
                    Return token + user data
                         ↓
                    Store in localStorage
                         ↓
                    Redirect to Dashboard
```

### 2. Health Report Submission Flow
```
User → Submit Report Form
         ↓
    Validate inputs (client-side)
         ↓
    POST /api/report + JWT token
         ↓
    Middleware: Verify JWT
         ↓
    Joi: Validate schema
         ↓
    Save to MongoDB (healthreports)
         ↓
    Return success response
         ↓
    Show success message
```

### 3. AI Prediction Flow
```
User clicks "Run AI Prediction"
         ↓
    POST /api/predict + JWT + district
         ↓
    Middleware: Verify JWT
         ↓
    Query MongoDB: Get reports (last 7 days)
         ↓
    Aggregate data:
    - Total cases
    - Symptom counts
    - Water sources
    - Sanitation levels
    - Rainfall patterns
         ↓
    Build AI prompt with aggregated data
         ↓
    Call Gemini/OpenAI API
         ↓
    Parse JSON response
         ↓
    Validate response format
         ↓
    Save to MongoDB (outbreakpredictions)
         ↓
    Return prediction to frontend
         ↓
    Display in RiskCard component
    (Color-coded: GREEN/YELLOW/RED)
```

## Component Hierarchy

```
App (layout.js)
│
├── Login Page (login/page.js)
│   └── Login Form
│
├── Dashboard (dashboard/page.js)
│   ├── Navbar
│   ├── Statistics Cards
│   │   ├── Total Cases
│   │   ├── Affected Villages
│   │   └── Reports Count
│   ├── RiskCard (AI Prediction)
│   │   ├── Risk Level Badge
│   │   ├── Confidence Score
│   │   ├── Predicted Disease
│   │   └── AI Explanation
│   ├── Symptom Chart (Recharts)
│   └── Village List
│
└── Submit Report (submit-report/page.js)
    ├── Navbar
    └── Report Form
        ├── Village Input
        ├── Age Input
        ├── Symptoms Checkboxes
        ├── Water Source Select
        ├── Cases Input
        ├── Sanitation Select
        ├── Rainfall Select
        └── Submit Button
```

## Security Layers

```
┌─────────────────────────────────────────┐
│         Request from Frontend           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Layer 1: CORS Protection           │
│      - Allow only frontend origin       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Layer 2: Rate Limiting             │
│      - Max 100 requests per 15 min      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Layer 3: JWT Authentication        │
│      - Verify token signature           │
│      - Check expiration                 │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Layer 4: Input Validation          │
│      - Joi schema validation            │
│      - Type checking                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Layer 5: Business Logic            │
│      - Process request                  │
└─────────────────────────────────────────┘
```

## Database Relationships

```
┌──────────────┐
│    users     │
│              │
│ _id (PK)     │◄─────────┐
│ email        │          │
│ password     │          │
│ role         │          │
│ district     │          │
└──────────────┘          │
                          │ reportedBy (FK)
                          │
                    ┌─────┴──────────┐
                    │ healthreports  │
                    │                │
                    │ _id (PK)       │
                    │ villageName    │
                    │ district       │
                    │ symptoms[]     │
                    │ date           │
                    │ reportedBy (FK)│
                    └────────────────┘
                          │
                          │ Aggregated by district + week
                          │
                    ┌─────▼──────────────┐
                    │ outbreakpredictions│
                    │                    │
                    │ _id (PK)           │
                    │ district           │
                    │ riskLevel          │
                    │ confidenceScore    │
                    │ predictedDisease   │
                    │ explanation        │
                    │ weekStart          │
                    │ weekEnd            │
                    │ dataSnapshot       │
                    └────────────────────┘
```

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                   │
│  Next.js 14 | React 18 | Tailwind CSS | Recharts       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    API LAYER                            │
│  Axios | REST | JSON | JWT Bearer Token                │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    APPLICATION LAYER                    │
│  Express.js | Node.js | Joi | bcryptjs                 │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    DATA LAYER                           │
│  MongoDB | Mongoose | Schema Validation                │
└─────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    EXTERNAL SERVICES                    │
│  Gemini API | OpenAI API | AI/ML Predictions           │
└─────────────────────────────────────────────────────────┘
```

---

**This architecture ensures:**
- ✅ Scalability (microservices-ready)
- ✅ Security (multi-layer protection)
- ✅ Maintainability (clear separation of concerns)
- ✅ Performance (optimized queries, caching-ready)
- ✅ Extensibility (easy to add features)
