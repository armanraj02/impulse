import React, { useEffect, useState } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { getStudentRiskDistribution } from '../../services/api';
import type { RiskDistribution } from '../../types/api';
import { LoadingState, ErrorState, EmptyState } from '../common/States';

const COLORS: Record<string, string> = {
  'HIGH': '#ef4444',
  'MEDIUM': '#f59e0b',
  'LOW': '#3b82f6',
  'NONE': '#10b981',
  'Unknown': '#94a3b8'
};

const RiskDistributionChart: React.FC = () => {
  const [data, setData] = useState<RiskDistribution[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    setError(false);
    try {
      const response = await getStudentRiskDistribution();
      setData(response);
    } catch (err) {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState onRetry={fetchData} />;
  if (!data || data.length === 0) return <EmptyState message="No risk data available." />;

  const totalClassified = data.reduce((sum, item) => sum + item.count, 0);

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[400px] flex flex-col relative">
      <h3 className="text-base font-semibold text-slate-800 mb-2">Student Risk Distribution</h3>
      <div className="flex-1 w-full min-h-0 relative">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={80}
              outerRadius={110}
              paddingAngle={2}
              dataKey="count"
              nameKey="category"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.category] || COLORS['Unknown']} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value: any, name: any, props: any) => [
                `${value} students (${props.payload.percentage}%)`, 
                name
              ]}
              contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Legend verticalAlign="bottom" height={36} iconType="circle" />
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none pb-8">
          <span className="text-3xl font-bold text-slate-800">{totalClassified}</span>
          <span className="text-xs text-slate-500 uppercase tracking-wider">Students</span>
        </div>
      </div>
    </div>
  );
};

export default RiskDistributionChart;
