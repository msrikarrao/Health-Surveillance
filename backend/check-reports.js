require('dotenv').config();
const mongoose = require('mongoose');
const HealthReport = require('./models/HealthReport');

mongoose.connect(process.env.MONGODB_URI).then(async () => {
  const total = await HealthReport.countDocuments();
  const withPred = await HealthReport.countDocuments({ 'prediction.riskLevel': { $exists: true } });
  const withoutPred = await HealthReport.countDocuments({ 'prediction.riskLevel': { $exists: false } });
  console.log('Total reports:', total);
  console.log('With prediction:', withPred);
  console.log('Without prediction:', withoutPred);
  const sample = await HealthReport.findOne({}, 'patientName symptoms prediction');
  console.log('Sample:', JSON.stringify(sample, null, 2));
  process.exit(0);
});
