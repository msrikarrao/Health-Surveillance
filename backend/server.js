require('dotenv').config();
const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const connectDB = require('./middleware/config/db');

const authRoutes = require('./routes/auth');
const googleAuthRoutes = require('./routes/googleAuth');
const reportRoutes = require('./routes/reports');
const predictionRoutes = require('./routes/predictions');

const app = express();

connectDB();

app.use(cors());
app.use(express.json());

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use('/api/', limiter);

app.use('/api/auth', authRoutes);
app.use('/api/auth', googleAuthRoutes);
app.use('/api', reportRoutes);
app.use('/api', predictionRoutes);

app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Health Surveillance API is running' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
