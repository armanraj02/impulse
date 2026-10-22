import React from 'react';
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
import type { SectionPerformanceExtended } from '../../types/api';

interface Props {
  data: SectionPerformanceExtended[];
}

const SectionPerformanceChart: React.FC<Props> = ({ data }) => {
  const chartData = data.length > 20 ? data.slice(0, 20) : data;

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[400px] flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-slate-800">Section Performance Comparison</h3>
        {data.length > 20 && (
          <span className="text-xs text-slate-500">Showing top 20 of {data.length} sections</span>
        )}
      </div>
      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis 
              dataKey="section_name" 
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

export default SectionPerformanceChart;
