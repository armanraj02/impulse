import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import type { Course } from '../../types/api';

interface Props {
  data: Course[];
}

const CourseAcademicChart: React.FC<Props> = ({ data }) => {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[400px] flex flex-col">
      <h3 className="text-base font-semibold text-slate-800 mb-6">Course Academic Performance</h3>
      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
            <XAxis 
              type="number"
              domain={[0, 100]}
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
              tickFormatter={(value) => `${value}%`}
            />
            <YAxis 
              dataKey="course_code" 
              type="category"
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
              width={100}
            />
            <Tooltip 
              cursor={{ fill: '#f1f5f9' }}
              contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              formatter={(value: any) => {
                if (typeof value !== 'number') return [value, 'Academic'];
                return [`${value.toFixed(1)}%`, 'Academic'];
              }}
              labelFormatter={(label, payload) => {
                const item = payload?.[0]?.payload;
                return item ? `${item.course_name} (${label})` : label;
              }}
            />
            <Bar 
              name="Academic"
              dataKey="average_assessment_percentage" 
              fill="#3b82f6" 
              radius={[0, 4, 4, 0]}
              maxBarSize={30}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default CourseAcademicChart;
