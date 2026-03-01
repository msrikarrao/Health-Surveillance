'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { reports, predictions } from '@/lib/api';
import Navbar from '@/components/Navbar';
import RiskCard from '@/components/RiskCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [reportsData, setReportsData] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [stats, setStats] = useState({ totalCases: 0, villages: [], topSymptoms: [] });

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      router.push('/login');
    } else {
      setUser(JSON.parse(userData));
      loadData(JSON.parse(userData));
    }
  }, [router]);

  const loadData = async (userData) => {
    try {
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);

      const reportsRes = await reports.getAll({
        district: userData.district,
        startDate: weekAgo.toISOString()
      });
      setReportsData(reportsRes.data);
      calculateStats(reportsRes.data);

      const predictionsRes = await predictions.getAll({ district: userData.district, limit: 1 });
      if (predictionsRes.data.length > 0) {
        setPrediction(predictionsRes.data[0]);
      }
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  const calculateStats = (data) => {
    const totalCases = data.reduce((sum, r) => sum + r.numberOfCasesReported, 0);
    const villageSet = new Set(data.map(r => r.villageName));
    
    const symptomCounts = {};
    data.forEach(r => {
      r.symptoms.forEach(s => {
        symptomCounts[s] = (symptomCounts[s] || 0) + r.numberOfCasesReported;
      });
    });

    const topSymptoms = Object.entries(symptomCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([name, value]) => ({ name: name.replace('_', ' '), value }));

    setStats({ totalCases, villages: Array.from(villageSet), topSymptoms });
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const res = await predictions.predict(user.district);
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
      
      <div className="max-w-7xl mx-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">Dashboard - {user.district}</h1>
          <button
            onClick={handlePredict}
            disabled={loading}
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition"
          >
            {loading ? 'Analyzing...' : 'Run AI Prediction'}
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm font-medium">Total Cases (7 days)</h3>
            <p className="text-3xl font-bold text-gray-800 mt-2">{stats.totalCases}</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm font-medium">Affected Villages</h3>
            <p className="text-3xl font-bold text-gray-800 mt-2">{stats.villages.length}</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm font-medium">Reports Submitted</h3>
            <p className="text-3xl font-bold text-gray-800 mt-2">{reportsData.length}</p>
          </div>
        </div>

        {prediction && <RiskCard prediction={prediction} />}

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Top Symptoms (Past Week)</h2>
          {stats.topSymptoms.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats.topSymptoms}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#4f46e5" name="Cases" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500">No data available</p>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Most Affected Villages</h2>
          <div className="space-y-2">
            {stats.villages.slice(0, 5).map((village, idx) => (
              <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="font-medium">{village}</span>
              </div>
            ))}
            {stats.villages.length === 0 && (
              <p className="text-gray-500">No villages reported yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
