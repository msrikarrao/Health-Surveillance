'use client';

export default function RiskCard({ prediction }) {
  const getRiskColor = (level) => {
    switch (level) {
      case 'LOW': return 'bg-green-100 border-green-500 text-green-800';
      case 'MEDIUM': return 'bg-yellow-100 border-yellow-500 text-yellow-800';
      case 'HIGH': return 'bg-red-100 border-red-500 text-red-800';
      default: return 'bg-gray-100 border-gray-500 text-gray-800';
    }
  };

  const getRiskIcon = (level) => {
    switch (level) {
      case 'LOW': return '✓';
      case 'MEDIUM': return '⚠';
      case 'HIGH': return '⚠';
      default: return '•';
    }
  };

  return (
    <div className={`rounded-lg shadow-lg p-6 mb-6 border-l-4 ${getRiskColor(prediction.riskLevel)}`}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <span className="text-3xl">{getRiskIcon(prediction.riskLevel)}</span>
            {prediction.riskLevel} RISK
          </h2>
          <p className="text-sm opacity-75 mt-1">
            Prediction generated on {new Date(prediction.createdAt).toLocaleString()}
          </p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold">{prediction.confidenceScore}%</div>
          <div className="text-sm opacity-75">Confidence</div>
        </div>
      </div>

      <div className="space-y-3">
        <div>
          <h3 className="font-semibold text-sm uppercase opacity-75">Predicted Disease</h3>
          <p className="text-lg font-medium">{prediction.predictedDisease}</p>
        </div>

        <div>
          <h3 className="font-semibold text-sm uppercase opacity-75">AI Analysis</h3>
          <p className="text-base leading-relaxed">{prediction.explanation}</p>
        </div>

        <div className="grid grid-cols-2 gap-4 pt-3 border-t border-current opacity-50">
          <div>
            <div className="text-sm opacity-75">Total Cases</div>
            <div className="text-xl font-bold">{prediction.totalCases}</div>
          </div>
          <div>
            <div className="text-sm opacity-75">Affected Villages</div>
            <div className="text-xl font-bold">{prediction.affectedVillages.length}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
