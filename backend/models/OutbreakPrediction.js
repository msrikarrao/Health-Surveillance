const mongoose = require('mongoose');

const outbreakPredictionSchema = new mongoose.Schema({
  district: { type: String, required: true },
  weekStart: { type: Date, required: true },
  weekEnd: { type: Date, required: true },
  riskLevel: { type: String, enum: ['LOW', 'MEDIUM', 'HIGH'], required: true },
  confidenceScore: { type: Number, min: 0, max: 100, required: true },
  predictedDisease: { type: String, required: true },
  explanation: { type: String, required: true },
  totalCases: { type: Number, required: true },
  affectedVillages: [String],
  dataSnapshot: { type: Object }
}, { timestamps: true });

module.exports = mongoose.model('OutbreakPrediction', outbreakPredictionSchema);
