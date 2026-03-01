'use client';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Navbar({ user }) {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/login');
  };

  return (
    <nav className="bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 text-white shadow-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 sm:gap-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-white/20 backdrop-blur rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                  <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                </svg>
              </div>
              <h1 className="text-lg sm:text-xl font-bold">Health Surveillance</h1>
            </div>
            <button className="sm:hidden text-white" onClick={() => document.getElementById('mobile-menu').classList.toggle('hidden')}>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
          
          <div id="mobile-menu" className="hidden sm:flex flex-col sm:flex-row items-start sm:items-center gap-3 sm:gap-6">
            <div className="flex flex-col sm:flex-row gap-2 sm:gap-4 w-full sm:w-auto">
              <Link href="/dashboard" className="px-4 py-2 rounded-lg hover:bg-white/20 transition-all duration-200 font-medium text-sm sm:text-base backdrop-blur">
                📊 Dashboard
              </Link>
              <Link href="/submit-report" className="px-4 py-2 rounded-lg hover:bg-white/20 transition-all duration-200 font-medium text-sm sm:text-base backdrop-blur">
                📝 Submit Report
              </Link>
              {(user.role === 'district_officer' || user.role === 'admin') && (
                <Link href="/prediction" className="px-4 py-2 rounded-lg hover:bg-white/20 transition-all duration-200 font-medium text-sm sm:text-base backdrop-blur flex items-center gap-2">
                  🔮 Predict Risk
                </Link>
              )}
            </div>
            
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 w-full sm:w-auto pt-3 sm:pt-0 border-t sm:border-t-0 border-white/20">
              <div className="flex items-center gap-2 bg-white/10 backdrop-blur px-3 py-2 rounded-lg">
                <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center text-sm font-bold">
                  {user.name.charAt(0).toUpperCase()}
                </div>
                <div className="text-sm">
                  <div className="font-semibold">{user.name}</div>
                  <div className="text-xs text-white/80">{user.role}</div>
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="w-full sm:w-auto bg-white/20 backdrop-blur px-4 py-2 rounded-lg hover:bg-white/30 transition-all duration-200 text-sm font-medium"
              >
                🚪 Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
