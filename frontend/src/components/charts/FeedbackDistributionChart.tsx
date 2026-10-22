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
import type { ModuleFeedback } from '../../types/api';

interface Props {
  data: ModuleFeedback[];
}

const FeedbackDistributionChart: React.FC<Props> = ({ data }) => {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[400px] flex flex-col">
      <h3 className="text-base font-semibold text-slate-800 mb-6">Module Feedback Ratings</h3>
      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis 
              dataKey="module_name" 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
              domain={[0, 5]}
              tickFormatter={(value) => value.toFixed(1)}
            />
            <Tooltip 
              cursor={{ fill: '#f1f5f9' }}
              contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              formatter={(value: any) => {
                if (typeof value !== 'number') return [value, 'Average Rating'];
                return [`${value.toFixed(2)} / 5`, 'Average Rating'];
              }}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
            <Bar 
              name="Average Rating (out of 5)"
              dataKey="average_rating" 
              fill="#8b5cf6" 
              radius={[4, 4, 0, 0]}
              maxBarSize={40}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default FeedbackDistributionChart;
