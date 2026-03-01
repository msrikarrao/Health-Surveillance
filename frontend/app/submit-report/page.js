'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { reports } from '@/lib/api';
import Navbar from '@/components/Navbar';

export default function SubmitReportPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    villageName: '',
    district: '',
    patientAge: '',
    symptoms: [],
    waterSourceType: 'well',
    numberOfCasesReported: 1,
    sanitationLevel: 'medium',
    rainfallLevel: 'medium'
  });

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      router.push('/login');
    } else {
      const parsed = JSON.parse(userData);
      setUser(parsed);
      setFormData(prev => ({ ...prev, district: parsed.district }));
    }
  }, [router]);

  const symptomOptions = ['diarrhea', 'fever', 'vomiting', 'jaundice', 'abdominal_pain', 'nausea', 'headache'];

  const handleSymptomToggle = (symptom) => {
    setFormData(prev => ({
      ...prev,
      symptoms: prev.symptoms.includes(symptom)
        ? prev.symptoms.filter(s => s !== symptom)
        : [...prev.symptoms, symptom]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    setLoading(true);

    try {
      await reports.submit(formData);
      setSuccess(true);
      setFormData({
        villageName: '',
        district: user.district,
        patientAge: '',
        symptoms: [],
        waterSourceType: 'well',
        numberOfCasesReported: 1,
        sanitationLevel: 'medium',
        rainfallLevel: 'medium'
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit report');
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar user={user} />
      
      <div className="max-w-3xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Submit Health Report</h1>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Village Name</label>
              <input
                type="text"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                value={formData.villageName}
                onChange={(e) => setFormData({ ...formData, villageName: e.target.value })}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">District</label>
              <input
                type="text"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-100"
                value={formData.district}
                readOnly
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Patient Age</label>
            <input
              type="number"
              required
              min="0"
              max="120"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              value={formData.patientAge}
              onChange={(e) => setFormData({ ...formData, patientAge: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Symptoms (select all that apply)</label>
            <div className="grid grid-cols-2 gap-2">
              {symptomOptions.map(symptom => (
                <label key={symptom} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.symptoms.includes(symptom)}
                    onChange={() => handleSymptomToggle(symptom)}
                    className="w-4 h-4 text-indigo-600"
                  />
                  <span className="text-sm capitalize">{symptom.replace('_', ' ')}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Water Source</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                value={formData.waterSourceType}
                onChange={(e) => setFormData({ ...formData, waterSourceType: e.target.value })}
              >
                <option value="well">Well</option>
                <option value="river">River</option>
                <option value="tank">Tank</option>
                <option value="pipeline">Pipeline</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Number of Cases</label>
              <input
                type="number"
                required
                min="1"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                value={formData.numberOfCasesReported}
                onChange={(e) => setFormData({ ...formData, numberOfCasesReported: e.target.value })}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Sanitation Level</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                value={formData.sanitationLevel}
                onChange={(e) => setFormData({ ...formData, sanitationLevel: e.target.value })}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Rainfall Level</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                value={formData.rainfallLevel}
                onChange={(e) => setFormData({ ...formData, rainfallLevel: e.target.value })}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">{error}</div>
          )}

          {success && (
            <div className="bg-green-50 text-green-600 p-3 rounded-lg text-sm">Report submitted successfully!</div>
          )}

          <button
            type="submit"
            disabled={loading || formData.symptoms.length === 0}
            className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition"
          >
            {loading ? 'Submitting...' : 'Submit Report'}
          </button>
        </form>
      </div>
    </div>
  );
}
