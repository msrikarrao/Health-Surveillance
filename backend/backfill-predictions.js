require('dotenv').config();
const mongoose = require('mongoose');
const connectDB = require('./middleware/config/db');
const HealthReport = require('./models/HealthReport');
const aiService = require('./services/aiService');

async function backfill() {
  await connectDB();
  console.log('Connected to DB');

  const reports = await HealthReport.find({ 'prediction.riskLevel': { $exists: false } });
  console.log(`Found ${reports.length} reports without predictions`);

  let success = 0, failed = 0;

  for (const report of reports) {
    try {
      const symptomList = ['diarrhea', 'fever', 'vomiting', 'jaundice', 'abdominal_pain', 'nausea', 'headache'];
      const symptomCounts = {};
      symptomList.forEach(s => {
        symptomCounts[s] = report.symptoms.includes(s) ? 1 : 0;
      });

      const predictionInput = {
        symptomCounts,
        sanitationLevel: report.sanitationLevel,
        rainfallLevel: report.rainfallLevel,
        waterSourceType: report.waterSourceType,
        patientAge: report.patientAge,
        villageCount: 1,
        totalReports: 1,
        ...(report.waterQuality && { waterQuality: report.waterQuality })
      };

      const result = await aiService.predictOutbreak(predictionInput);

      await HealthReport.updateOne(
        { _id: report._id },
        {
          $set: {
            prediction: {
              riskLevel: result.riskLevel,
              confidenceScore: result.confidenceScore,
              predictedDisease: result.predictedDisease,
              explanation: result.explanation,
              riskScore: result.riskScore
            }
          }
        }
      );

      console.log(`✅ ${report.patientName} → ${result.riskLevel} (${result.predictedDisease})`);
      success++;
    } catch (err) {
      console.error(`❌ Failed for ${report.patientName}: ${err.message}`);
      failed++;
    }
  }

  console.log(`\nDone. Success: ${success}, Failed: ${failed}`);
  process.exit(0);
}

backfill().catch(err => {
  console.error(err);
  process.exit(1);
});
