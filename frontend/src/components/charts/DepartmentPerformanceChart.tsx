import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { getDepartments } from '../../services/api';
import type { Department } from '../../types/api';
import { LoadingState, ErrorState, EmptyState } from '../common/States';

const DepartmentPerformanceChart: React.FC = () => {
  const [data, setData] = useState<Department[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    setError(false);
    try {
      const response = await getDepartments();
      // Sort by performance descending
      const sorted = response.sort((a, b) => b.average_assessment_percentage - a.average_assessment_percentage);
      setData(sorted);
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
  if (!data || data.length === 0) return <EmptyState message="No department data available." />;

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[400px] flex flex-col">
      <h3 className="text-base font-semibold text-slate-800 mb-6">Department Academic Performance</h3>
      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis 
              dataKey="department_name" 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 12 }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 12 }}
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip 
              cursor={{ fill: '#f1f5f9' }}
              contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              formatter={(value: any) => [`${value}%`, 'Academic Performance']}
            />
            <Bar 
              dataKey="average_assessment_percentage" 
              radius={[4, 4, 0, 0]}
              maxBarSize={50}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.average_assessment_percentage >= 75 ? '#3b82f6' : entry.average_assessment_percentage >= 60 ? '#f59e0b' : '#ef4444'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default DepartmentPerformanceChart;
