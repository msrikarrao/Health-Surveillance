'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { reports, predictions } from '@/lib/api';
import Navbar from '@/components/Navbar';
import RiskCard from '@/components/RiskCard';

export default function PredictionPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [villages, setVillages] = useState([]);
  const [selectedVillage, setSelectedVillage] = useState('all');
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      router.push('/login');
    } else {
      const parsed = JSON.parse(userData);
      setUser(parsed);
      loadVillages();
    }
  }, [router]);

  const loadVillages = async () => {
    try {
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      const res = await reports.getAll({ startDate: weekAgo.toISOString() });
      const uniqueVillages = [...new Set(res.data.map(r => r.villageName))];
      setVillages(uniqueVillages);
    } catch (error) {
      console.error('Failed to load villages:', error);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const village = selectedVillage === 'all' ? null : selectedVillage;
      const res = await predictions.predict(village);
      setPrediction(res.data);
    } catch (error) {
      alert(error.response?.data?.error || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar user={user} />
      
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">🔮 Risk Prediction</h1>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Select Village for Analysis</h2>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Village</label>
            <select
              value={selectedVillage}
              onChange={(e) => setSelectedVillage(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 text-lg"
            >
              <option value="all">All Villages</option>
              {villages.map(v => (
                <option key={v} value={v}>{v}</option>
              ))}
            </select>
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition font-semibold text-lg"
          >
            {loading ? '🔄 Analyzing Data...' : '🔮 Predict Risk'}
          </button>
        </div>

        {prediction && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Prediction Results</h2>
            <RiskCard prediction={prediction} />
          </div>
        )}

        {!prediction && !loading && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
            <p className="text-blue-800 text-lg">
              Select a village and click "Predict Risk" to analyze health data and detect potential outbreaks.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
