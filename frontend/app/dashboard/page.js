'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { reports, predictions } from '@/lib/api';
import Navbar from '@/components/Navbar';
import RiskCard from '@/components/RiskCard';
import PredictionModal from '@/components/PredictionModal';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [reportsData, setReportsData] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [stats, setStats] = useState({ totalCases: 0, villages: [], topSymptoms: [], waterSources: [], trendData: [] });
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [districts, setDistricts] = useState([]);
  const [showPredictionModal, setShowPredictionModal] = useState(false);

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
        startDate: weekAgo.toISOString()
      });
      setReportsData(reportsRes.data);
      calculateStats(reportsRes.data);

      const uniqueDistricts = [...new Set(reportsRes.data.map(r => r.district))];
      setDistricts(uniqueDistricts);

      const predictionsRes = await predictions.getAll({ limit: 10 });
      setPredictions(predictionsRes.data);
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

    const waterSourceCounts = {};
    data.forEach(r => {
      waterSourceCounts[r.waterSourceType] = (waterSourceCounts[r.waterSourceType] || 0) + r.numberOfCasesReported;
    });
    const waterSources = Object.entries(waterSourceCounts).map(([name, value]) => ({ name, value }));

    const trendData = [];
    for (let i = 6; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];
      const dayCases = data.filter(r => r.date?.split('T')[0] === dateStr)
        .reduce((sum, r) => sum + r.numberOfCasesReported, 0);
      trendData.push({ date: dateStr.slice(5), cases: dayCases });
    }

    setStats({ totalCases, villages: Array.from(villageSet), topSymptoms, waterSources, trendData });
  };

  const handlePredict = async (village) => {
    setLoading(true);
    try {
      const res = await predictions.predict(village);
      setPredictions(Array.isArray(res.data) ? res.data : [res.data]);
    } catch (error) {
      alert(error.response?.data?.error || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const exportToPDF = () => {
    window.print();
  };

  const exportToCSV = () => {
    const headers = ['Village', 'District', 'Age', 'Symptoms', 'Water Source', 'Cases', 'Date'];
    const rows = reportsData.map(r => [
      r.villageName,
      r.district,
      r.patientAge,
      r.symptoms.join('; '),
      r.waterSourceType,
      r.numberOfCasesReported,
      new Date(r.date).toLocaleDateString()
    ]);
    const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `health-reports-${user.district}-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  useEffect(() => {
    if (autoRefresh && user) {
      const interval = setInterval(() => loadData(user), 300000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh, user]);

  useEffect(() => {
    const handleReportSubmitted = () => {
      if (user) loadData(user);
    };
    window.addEventListener('reportSubmitted', handleReportSubmitted);
    return () => window.removeEventListener('reportSubmitted', handleReportSubmitted);
  }, [user]);

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar user={user} />
      
      <div className="max-w-7xl mx-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">Dashboard - All Districts</h1>
          <div className="flex gap-3 items-center">
            <label className="flex items-center gap-2 text-sm text-gray-600">
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                className="w-4 h-4"
              />
              Auto-refresh (5 min)
            </label>
            <button
              onClick={exportToCSV}
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm"
            >
              Export CSV
            </button>
            <button
              onClick={exportToPDF}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition text-sm"
            >
              Print/PDF
            </button>
          </div>
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

        {predictions.length > 0 && (
          <div className="space-y-4 mb-6">
            {predictions.map((prediction, idx) => (
              <RiskCard key={idx} prediction={prediction} />
            ))}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">7-Day Trend</h2>
            {stats.trendData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={stats.trendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" label={{ value: 'Date', position: 'insideBottom', offset: -5 }} />
                  <YAxis label={{ value: 'Cases', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="cases" stroke="#4f46e5" strokeWidth={2} name="Cases" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No data available</p>
            )}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Water Source Distribution</h2>
            {stats.waterSources.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={stats.waterSources}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {stats.waterSources.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#4f46e5', '#10b981', '#f59e0b', '#ef4444'][index % 4]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-gray-500">No data available</p>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Top Symptoms (Past Week)</h2>
          {stats.topSymptoms.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats.topSymptoms}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" label={{ value: 'Symptoms', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: 'Number of Cases', angle: -90, position: 'insideLeft' }} />
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
