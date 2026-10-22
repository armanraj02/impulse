import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import type { RiskDistribution } from '../../types/api';

interface StudentRiskDistributionChartProps {
  data: RiskDistribution[];
}

const COLORS: Record<string, string> = {
  'High Risk': '#ef4444', // red-500
  'Attendance Risk': '#f59e0b', // amber-500
  'Academic Risk': '#fbbf24', // amber-400
  'No Risk': '#10b981', // emerald-500
  'Unknown': '#9ca3af' // gray-400
};

export const StudentRiskDistributionChart: React.FC<StudentRiskDistributionChartProps> = ({ data }) => {
  // Ensure we sort data so high risk is first, no risk last
  const sortedData = [...data].sort((a, b) => {
    const order: Record<string, number> = {
      'High Risk': 0,
      'Attendance Risk': 1,
      'Academic Risk': 2,
      'No Risk': 3,
    };
    return (order[a.category] ?? 4) - (order[b.category] ?? 4);
  });

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex flex-col h-[350px]">
      <h3 className="text-sm font-bold text-gray-700 uppercase tracking-wider mb-4">Risk Distribution</h3>
      <div className="flex-1 w-full h-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={sortedData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={2}
              dataKey="count"
              nameKey="category"
            >
              {sortedData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.category] || COLORS['Unknown']} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value: any, name: any, props: any) => [
                `${value} students (${props.payload.percentage}%)`, 
                String(name).toUpperCase()
              ]}
            />
            <Legend 
              verticalAlign="bottom" 
              height={36} 
              formatter={(value) => <span className="text-xs font-semibold text-gray-700">{value.toUpperCase()}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
