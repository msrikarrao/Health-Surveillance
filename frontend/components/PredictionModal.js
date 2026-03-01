'use client';
import { useState, useEffect } from 'react';
import { reports, predictions } from '@/lib/api';

export default function PredictionModal({ isOpen, onClose, onPredict }) {
  const [villages, setVillages] = useState([]);
  const [selectedVillage, setSelectedVillage] = useState('all');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadVillages();
    }
  }, [isOpen]);

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
      await onPredict(village);
      onClose();
    } catch (error) {
      alert(error.response?.data?.error || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 w-96">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">Select Village for Prediction</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            ✕
          </button>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Village</label>
          <select
            value={selectedVillage}
            onChange={(e) => setSelectedVillage(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
          >
            <option value="all">All Villages</option>
            {villages.map(v => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
          >
            Cancel
          </button>
          <button
            onClick={handlePredict}
            disabled={loading}
            className="flex-1 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition"
          >
            {loading ? 'Analyzing...' : 'Predict Risk'}
          </button>
        </div>
      </div>
    </div>
  );
}
