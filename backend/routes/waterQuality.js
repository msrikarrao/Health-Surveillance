const express = require('express');
const axios = require('axios');
const { auth } = require('../middleware/auth');

const router = express.Router();
const ML_URL = process.env.PYTHON_ML_URL || 'http://localhost:5001';

/**
 * POST /api/water-quality
 * Proxy to Python ML water quality model.
 * Body: { ph, Hardness, Solids, Chloramines, Sulfate,
 *         Conductivity, Organic_carbon, Trihalomethanes, Turbidity }
 */
router.post('/water-quality', auth, async (req, res) => {
  try {
    const response = await axios.post(`${ML_URL}/water-quality`, req.body, { timeout: 8000 });
    res.json(response.data);
  } catch (err) {
    const msg = err.response?.data?.error || err.message;
    res.status(500).json({ error: `Water quality service error: ${msg}` });
  }
});

module.exports = router;
