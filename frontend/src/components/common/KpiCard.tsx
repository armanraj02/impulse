import React from 'react';
import { cn } from '../layout/Sidebar';

interface KpiCardProps {
  title: string;
  value: string | number;
  icon: React.ElementType;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  className?: string;
}

const KpiCard: React.FC<KpiCardProps> = ({ title, value, icon: Icon, trend, className }) => {
  return (
    <div className={cn("bg-white p-6 rounded-xl border border-slate-200 shadow-sm", className)}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
          <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
          
          {trend && (
            <div className="mt-2 flex items-center gap-1.5 text-sm">
              <span className={cn("font-medium", trend.isPositive ? "text-emerald-600" : "text-rose-600")}>
                {trend.isPositive ? '+' : '-'}{Math.abs(trend.value)}%
              </span>
              <span className="text-slate-400">vs last period</span>
            </div>
          )}
        </div>
        <div className="p-3 bg-brand-50 rounded-lg">
          <Icon className="w-6 h-6 text-brand-600" />
        </div>
      </div>
    </div>
  );
};

export default KpiCard;
