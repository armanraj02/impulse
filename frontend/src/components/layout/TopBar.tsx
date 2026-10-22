import React, { useEffect, useState } from 'react';
import { Menu, Search, RefreshCw, Server, AlertCircle } from 'lucide-react';
import { getHealth } from '../../services/api';

interface TopBarProps {
  onMenuClick: () => void;
}

const TopBar: React.FC<TopBarProps> = ({ onMenuClick }) => {
  const [apiStatus, setApiStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');
  
  const checkApi = async () => {
    setApiStatus('checking');
    try {
      await getHealth();
      setApiStatus('connected');
    } catch (e) {
      setApiStatus('disconnected');
    }
  };

  useEffect(() => {
    checkApi();
    const interval = setInterval(checkApi, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 sm:px-6 z-10">
      <div className="flex items-center gap-4">
        <button className="lg:hidden text-slate-500 hover:text-slate-700" onClick={onMenuClick}>
          <Menu className="w-6 h-6" />
        </button>
        <div className="relative hidden sm:block">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input 
            type="text" 
            placeholder="Search students, courses..." 
            className="pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 w-64"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-200 bg-slate-50">
          {apiStatus === 'checking' && <RefreshCw className="w-3.5 h-3.5 text-slate-400 animate-spin" />}
          {apiStatus === 'connected' && <Server className="w-3.5 h-3.5 text-emerald-500" />}
          {apiStatus === 'disconnected' && <AlertCircle className="w-3.5 h-3.5 text-rose-500" />}
          <span className="text-xs font-medium text-slate-600">
            {apiStatus === 'checking' ? 'Checking API...' : apiStatus === 'connected' ? 'API Connected' : 'API Unavailable'}
          </span>
        </div>
        
        <button onClick={checkApi} className="p-2 text-slate-400 hover:text-brand-600 transition-colors" title="Refresh Data">
          <RefreshCw className="w-5 h-5" />
        </button>
        
        <div className="w-8 h-8 rounded-full bg-brand-100 flex items-center justify-center text-brand-700 font-semibold text-sm border border-brand-200">
          AD
        </div>
      </div>
    </header>
  );
};

export default TopBar;
