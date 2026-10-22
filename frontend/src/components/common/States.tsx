import React from 'react';
import { Loader2 } from 'lucide-react';

export const LoadingState: React.FC<{ message?: string }> = ({ message = "Loading analytics..." }) => (
  <div className="flex flex-col items-center justify-center p-12 text-slate-400">
    <Loader2 className="w-8 h-8 animate-spin text-brand-500 mb-4" />
    <p className="text-sm font-medium">{message}</p>
  </div>
);

import { AlertCircle, RefreshCw } from 'lucide-react';

export const ErrorState: React.FC<{ message?: string, onRetry?: () => void }> = ({ 
  message = "Unable to connect to the analytics service.", 
  onRetry 
}) => (
  <div className="flex flex-col items-center justify-center p-12 text-slate-500 border border-rose-100 bg-rose-50/50 rounded-xl">
    <AlertCircle className="w-10 h-10 text-rose-500 mb-4" />
    <h3 className="text-lg font-semibold text-slate-800 mb-2">Something went wrong</h3>
    <p className="text-sm text-center mb-6 max-w-md">{message}</p>
    {onRetry && (
      <button 
        onClick={onRetry}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors shadow-sm"
      >
        <RefreshCw className="w-4 h-4" />
        Retry
      </button>
    )}
  </div>
);

import { Inbox } from 'lucide-react';

export const EmptyState: React.FC<{ message?: string }> = ({ 
  message = "No data available for the selected filters." 
}) => (
  <div className="flex flex-col items-center justify-center p-12 text-slate-400 border border-slate-100 bg-slate-50/50 rounded-xl border-dashed">
    <Inbox className="w-12 h-12 text-slate-300 mb-4" />
    <h3 className="text-base font-medium text-slate-600 mb-1">No Results Found</h3>
    <p className="text-sm text-center">{message}</p>
  </div>
);
