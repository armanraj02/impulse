import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { getDepartmentsPerformance } from '../../services/api';
import type { DepartmentPerformanceExtended } from '../../types/api';
import { LoadingState, ErrorState, EmptyState } from '../common/States';

const DepartmentComparisonChart: React.FC = () => {
  const [data, setData] = useState<DepartmentPerformanceExtended[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    setError(false);
    try {
      const response = await getDepartmentsPerformance();
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
  if (!data || data.length === 0) return <EmptyState message="No department data available." />;

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[400px] flex flex-col">
      <h3 className="text-base font-semibold text-slate-800 mb-6">Department Comparison (Academic vs Attendance)</h3>
      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis 
              dataKey="department_name" 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip 
              cursor={{ fill: '#f1f5f9' }}
              contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              formatter={(value: any, name: any) => [`${value}%`, name === 'average_assessment_percentage' ? 'Academic' : 'Attendance']}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
            <Bar 
              name="Academic"
              dataKey="average_assessment_percentage" 
              fill="#3b82f6" 
              radius={[4, 4, 0, 0]}
              maxBarSize={40}
            />
            <Bar 
              name="Attendance"
              dataKey="average_attendance_percentage" 
              fill="#10b981" 
              radius={[4, 4, 0, 0]}
              maxBarSize={40}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default DepartmentComparisonChart;
