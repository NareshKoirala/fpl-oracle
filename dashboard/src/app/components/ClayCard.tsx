import React from 'react';

interface ClayCardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  compact?: boolean;
}

export default function ClayCard({
  children,
  className = '',
  title,
  compact = false,
}: ClayCardProps) {
  const padding = compact ? 'p-4' : 'p-6';

  return (
    <div className={`clay-card ${padding} ${className}`}>
      {title && (
        <h2 className={`${compact ? 'text-lg' : 'text-2xl'} font-bold bg-gradient-to-r from-blue-700 to-cyan-600 bg-clip-text text-transparent ${compact ? 'mb-3' : 'mb-6'}`}>
          {title}
        </h2>
      )}
      {children}
    </div>
  );
}
