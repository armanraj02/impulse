import React from 'react';

export const PlaceholderPage: React.FC<{ title: string }> = ({ title }) => (
  <div className="space-y-6">
    <div className="flex justify-between items-center mb-2">
      <h1 className="text-2xl font-bold text-slate-800">{title}</h1>
    </div>
    <div className="bg-white p-12 rounded-xl border border-slate-200 shadow-sm flex items-center justify-center">
      <p className="text-slate-400">This page will be implemented in Phase 3/4.</p>
    </div>
  </div>
);
