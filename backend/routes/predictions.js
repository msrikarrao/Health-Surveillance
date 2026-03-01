const express = require('express');
const HealthReport = require('../models/HealthReport');
const OutbreakPrediction = require('../models/OutbreakPrediction');
const aiService = require('../services/aiService');
const { auth } = require('../middleware/auth');

const router = express.Router();

router.post('/predict', auth, async (req, res) => {
  try {
    const { district } = req.body;
    if (!district) return res.status(400).json({ error: 'District is required' });

    const weekStart = new Date();
    weekStart.setDate(weekStart.getDate() - 7);
    const weekEnd = new Date();

    const reports = await HealthReport.find({
      district,
      date: { $gte: weekStart, $lte: weekEnd }
    });

    if (reports.length === 0) {
      return res.status(400).json({ error: 'No reports found for the past week' });
    }

    const aggregatedData = aggregateReports(reports);
    const prediction = await aiService.predictOutbreak(aggregatedData);

    const outbreakPrediction = new OutbreakPrediction({
      district,
      weekStart,
      weekEnd,
      riskLevel: prediction.riskLevel,
      confidenceScore: prediction.confidenceScore,
      predictedDisease: prediction.predictedDisease,
      explanation: prediction.explanation,
      totalCases: aggregatedData.totalCases,
      affectedVillages: aggregatedData.villages,
      dataSnapshot: aggregatedData
    });

    await outbreakPrediction.save();
    res.json(outbreakPrediction);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/predictions', auth, async (req, res) => {
  try {
    const { district, limit = 10 } = req.query;
    
    const query = district ? { district } : {};
    
    const predictions = await OutbreakPrediction.find(query)
      .sort({ createdAt: -1 })
      .limit(parseInt(limit));

    res.json(predictions);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

function aggregateReports(reports) {
  const symptomCounts = {};
  const villages = new Set();
  const waterSources = {};
  let totalCases = 0;
  let lowSanitation = 0;
  let highRainfall = 0;

  reports.forEach(report => {
    villages.add(report.villageName);
    totalCases += report.numberOfCasesReported;

    report.symptoms.forEach(symptom => {
      symptomCounts[symptom] = (symptomCounts[symptom] || 0) + report.numberOfCasesReported;
    });

    waterSources[report.waterSourceType] = (waterSources[report.waterSourceType] || 0) + 1;

    if (report.sanitationLevel === 'low') lowSanitation++;
    if (report.rainfallLevel === 'high') highRainfall++;
  });

  return {
    totalCases,
    villages: Array.from(villages),
    villageCount: villages.size,
    symptomCounts,
    waterSources,
    lowSanitationCount: lowSanitation,
    highRainfallCount: highRainfall,
    reportCount: reports.length,
    averageCasesPerReport: (totalCases / reports.length).toFixed(2)
  };
}

module.exports = router;
