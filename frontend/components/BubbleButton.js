'use client';
import { useState, useCallback } from 'react';

export default function BubbleButton({ children, className = '', disabled = false, onClick, type = 'button' }) {
  const [bubbles, setBubbles] = useState([]);

  const spawnBubbles = useCallback((e) => {
    if (disabled) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const newBubbles = Array.from({ length: 8 }, (_, i) => ({
      id: Date.now() + i,
      x,
      y,
      size: 6 + Math.random() * 14,
      tx: (Math.random() - 0.5) * 80,
      ty: -(20 + Math.random() * 60),
      opacity: 0.5 + Math.random() * 0.4,
    }));

    setBubbles(prev => [...prev, ...newBubbles]);
    setTimeout(() => {
      setBubbles(prev => prev.filter(b => !newBubbles.find(nb => nb.id === b.id)));
    }, 700);
  }, [disabled]);

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      onMouseEnter={spawnBubbles}
      className={`relative overflow-hidden ${className}`}
    >
      {bubbles.map(b => (
        <span
          key={b.id}
          className="pointer-events-none absolute rounded-full bg-white"
          style={{
            left: b.x,
            top: b.y,
            width: b.size,
            height: b.size,
            opacity: b.opacity,
            transform: 'translate(-50%, -50%)',
            animation: `bubble-float 0.7s ease-out forwards`,
            '--tx': `${b.tx}px`,
            '--ty': `${b.ty}px`,
          }}
        />
      ))}
      {children}
    </button>
  );
}
