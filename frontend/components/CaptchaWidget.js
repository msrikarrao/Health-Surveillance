'use client';
import { useEffect, useRef, useState, useCallback } from 'react';

const CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const LENGTH = 6;

function generateCode() {
  return Array.from({ length: LENGTH }, () => CHARS[Math.floor(Math.random() * CHARS.length)]).join('');
}

function drawCaptcha(canvas, code) {
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  // Gradient background
  const grad = ctx.createLinearGradient(0, 0, W, H);
  grad.addColorStop(0, '#eef2ff');
  grad.addColorStop(1, '#f5f3ff');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);

  // Noise lines
  for (let i = 0; i < 5; i++) {
    ctx.strokeStyle = `hsla(${Math.random() * 360},70%,65%,0.5)`;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(Math.random() * W, Math.random() * H);
    ctx.bezierCurveTo(Math.random() * W, Math.random() * H, Math.random() * W, Math.random() * H, Math.random() * W, Math.random() * H);
    ctx.stroke();
  }

  // Noise dots
  for (let i = 0; i < 35; i++) {
    ctx.fillStyle = `hsla(${Math.random() * 360},60%,55%,0.6)`;
    ctx.beginPath();
    ctx.arc(Math.random() * W, Math.random() * H, 1.5, 0, Math.PI * 2);
    ctx.fill();
  }

  // Characters
  const colors = ['#4338ca', '#7c3aed', '#be185d', '#0369a1', '#047857'];
  const charW = W / (LENGTH + 1);
  for (let i = 0; i < code.length; i++) {
    ctx.save();
    ctx.font = `bold ${26 + Math.random() * 6}px 'Georgia', serif`;
    ctx.fillStyle = colors[i % colors.length];
    ctx.shadowColor = 'rgba(0,0,0,0.15)';
    ctx.shadowBlur = 2;
    const x = charW * (i + 0.65);
    const y = H / 2 + 9;
    ctx.translate(x, y);
    ctx.rotate((Math.random() - 0.5) * 0.45);
    ctx.fillText(code[i], 0, 0);
    ctx.restore();
  }
}

export default function CaptchaWidget({ onVerify }) {
  const canvasRef = useRef(null);
  const [code, setCode] = useState('');
  const [input, setInput] = useState('');
  const [error, setError] = useState(false);
  const [success, setSuccess] = useState(false);

  const refresh = useCallback(() => {
    const newCode = generateCode();
    setCode(newCode);
    setInput('');
    setError(false);
    setSuccess(false);
    onVerify(false);
  }, [onVerify]);

  useEffect(() => { refresh(); }, []);

  useEffect(() => {
    if (canvasRef.current && code) drawCaptcha(canvasRef.current, code);
  }, [code]);

  const handleChange = (e) => {
    const val = e.target.value.toUpperCase();
    setInput(val);
    if (val.length === LENGTH) {
      const valid = val === code;
      setError(!valid);
      setSuccess(valid);
      onVerify(valid);
      if (!valid) setTimeout(refresh, 900);
    } else {
      setError(false);
      setSuccess(false);
      onVerify(false);
    }
  };

  return (
    <div className="rounded-xl border border-indigo-100 dark:border-indigo-900 bg-indigo-50/40 dark:bg-indigo-950/20 p-3 space-y-3">
      {/* Label */}
      <p className="text-xs font-semibold text-indigo-500 dark:text-indigo-400 uppercase tracking-wider">Security Verification</p>

      {/* Canvas + Refresh */}
      <div className="flex items-center gap-3">
        <canvas
          ref={canvasRef}
          width={190}
          height={58}
          className="rounded-lg border border-indigo-200 dark:border-indigo-800 shadow-sm select-none flex-shrink-0"
          style={{ userSelect: 'none' }}
        />
        {/* Refresh icon button */}
        <button
          type="button"
          onClick={refresh}
          title="Refresh CAPTCHA"
          className="flex items-center justify-center w-9 h-9 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 hover:bg-indigo-500 dark:hover:bg-indigo-600 hover:shadow-[0_0_12px_rgba(99,102,241,0.5)] hover:scale-110 active:scale-95 transition-all duration-200 flex-shrink-0 group"
        >
          <svg className="w-4 h-4 text-indigo-600 dark:text-indigo-300 group-hover:text-white transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      {/* Input */}
      <div className="relative">
        <input
          type="text"
          value={input}
          onChange={handleChange}
          maxLength={LENGTH}
          placeholder="Enter code above"
          autoComplete="off"
          className={`w-full px-4 py-2.5 rounded-lg border-2 text-sm font-mono tracking-[0.3em] uppercase transition-colors duration-200 focus:outline-none focus:ring-0
            ${success
              ? 'border-green-400 bg-green-50 dark:bg-green-950/30 text-green-700 dark:text-green-300'
              : error
              ? 'border-red-400 bg-red-50 dark:bg-red-950/30 text-red-700 dark:text-red-300'
              : 'border-indigo-200 dark:border-indigo-800 bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-100 focus:border-indigo-400'
            }`}
        />
        {/* Status icon */}
        {success && (
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-green-500 text-lg">✓</span>
        )}
        {error && (
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-red-500 text-lg">✗</span>
        )}
      </div>

      {error && <p className="text-red-500 dark:text-red-400 text-xs">Incorrect code — a new CAPTCHA has been generated.</p>}
      {success && <p className="text-green-600 dark:text-green-400 text-xs">✓ Verified successfully!</p>}
    </div>
  );
}
