'use client';
import { useEffect, useState } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';

export default function PageTransitionLoader() {
  const [loading, setLoading] = useState(false);
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    setLoading(true);
    const timer = setTimeout(() => setLoading(false), 150);
    return () => clearTimeout(timer);
  }, [pathname, searchParams]);

  if (!loading) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="relative flex items-center justify-center">
        <span className="absolute w-24 h-24 rounded-full bg-indigo-400/20 animate-ping" style={{ animationDuration: '1.4s' }} />
        <span className="absolute w-16 h-16 rounded-full bg-indigo-400/25 animate-ping" style={{ animationDuration: '1s' }} />
        <img
          src="/logo.svg"
          alt="Loading"
          className="w-14 h-14 relative z-10"
          style={{ animation: 'logo-pulse 1.4s ease-in-out infinite' }}
        />
      </div>
      <p className="mt-4 text-sm font-semibold text-indigo-500 dark:text-indigo-400 tracking-widest uppercase animate-pulse">
        Loading...
      </p>
    </div>
  );
}
