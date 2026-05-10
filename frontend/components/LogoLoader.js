'use client';

export default function LogoLoader({ fullScreen = false }) {
  return (
    <div className={`flex flex-col items-center justify-center gap-4 ${fullScreen ? 'fixed inset-0 z-50 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900' : 'py-12'}`}>
      <div className="relative flex items-center justify-center">
        {/* Ripple rings */}
        <span className="absolute w-24 h-24 rounded-full bg-indigo-400/20 animate-ping" style={{ animationDuration: '1.4s' }} />
        <span className="absolute w-16 h-16 rounded-full bg-indigo-400/25 animate-ping" style={{ animationDuration: '1s' }} />
        {/* Logo */}
        <img
          src="/logo.svg"
          alt="Loading"
          className="w-14 h-14 relative z-10"
          style={{ animation: 'logo-pulse 1.4s ease-in-out infinite' }}
        />
      </div>
      <p className="text-sm font-semibold text-indigo-500 dark:text-indigo-400 tracking-widest uppercase animate-pulse">
        Loading...
      </p>
    </div>
  );
}
