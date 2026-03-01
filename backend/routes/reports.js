const express = require('express');
const Joi = require('joi');
const HealthReport = require('../models/HealthReport');
const { auth } = require('../middleware/auth');

const router = express.Router();

const reportSchema = Joi.object({
  villageName: Joi.string().required(),
  district: Joi.string().required(),
  patientAge: Joi.number().min(0).max(120).required(),
  symptoms: Joi.array().items(Joi.string().valid('diarrhea', 'fever', 'vomiting', 'jaundice', 'abdominal_pain', 'nausea', 'headache')).min(1).required(),
  date: Joi.date().default(Date.now),
  waterSourceType: Joi.string().valid('well', 'river', 'tank', 'pipeline').required(),
  numberOfCasesReported: Joi.number().min(1).default(1),
  sanitationLevel: Joi.string().valid('low', 'medium', 'high').required(),
  rainfallLevel: Joi.string().valid('low', 'medium', 'high').required()
});

router.post('/report', auth, async (req, res) => {
  try {
    const { error, value } = reportSchema.validate(req.body);
    if (error) return res.status(400).json({ error: error.details[0].message });

    const report = new HealthReport({
      ...value,
      reportedBy: req.user._id
    });

    await report.save();
    res.status(201).json(report);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/reports', auth, async (req, res) => {
  try {
    const { district, startDate, endDate, limit = 100 } = req.query;
    
    const query = {};
    if (district) query.district = district;
    if (startDate || endDate) {
      query.date = {};
      if (startDate) query.date.$gte = new Date(startDate);
      if (endDate) query.date.$lte = new Date(endDate);
    }

    const reports = await HealthReport.find(query)
      .sort({ date: -1 })
      .limit(parseInt(limit))
      .populate('reportedBy', 'name email');

    res.json(reports);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
