export const offlineStorage = {
  saveReport: (report) => {
    const reports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
    reports.push({ ...report, timestamp: Date.now(), synced: false });
    localStorage.setItem('offlineReports', JSON.stringify(reports));
  },

  getUnsynced: () => {
    const reports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
    return reports.filter(r => !r.synced);
  },

  markSynced: (timestamp) => {
    const reports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
    const updated = reports.map(r => 
      r.timestamp === timestamp ? { ...r, synced: true } : r
    );
    localStorage.setItem('offlineReports', JSON.stringify(updated));
  },

  clearSynced: () => {
    const reports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
    const unsynced = reports.filter(r => !r.synced);
    localStorage.setItem('offlineReports', JSON.stringify(unsynced));
  }
};

export const registerServiceWorker = () => {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then(reg => console.log('Service Worker registered'))
        .catch(err => console.log('Service Worker registration failed:', err));
    });
  }
};
