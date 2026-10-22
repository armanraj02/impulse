import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

interface Props {
  totalStudents: number;
  studentsBelow50: number;
}

const COLORS: Record<string, string> = {
  'Healthy': '#10b981', // green
  'Academic Concern': '#f59e0b' // amber
};

const AcademicRiskDistributionChart: React.FC<Props> = ({ totalStudents, studentsBelow50 }) => {
  const healthyCount = Math.max(0, totalStudents - studentsBelow50);
  
  const data = [
    { category: 'Healthy', count: healthyCount, percentage: totalStudents > 0 ? ((healthyCount / totalStudents) * 100).toFixed(1) : 0 },
    { category: 'Academic Concern', count: studentsBelow50, percentage: totalStudents > 0 ? ((studentsBelow50 / totalStudents) * 100).toFixed(1) : 0 }
  ];

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[400px] flex flex-col relative">
      <h3 className="text-base font-semibold text-slate-800 mb-2">Academic Concern Distribution</h3>
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
                <Cell key={`cell-${index}`} fill={COLORS[entry.category] || '#94a3b8'} />
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
          <span className="text-3xl font-bold text-slate-800">{totalStudents}</span>
          <span className="text-xs text-slate-500 uppercase tracking-wider">Students</span>
        </div>
      </div>
    </div>
  );
};

export default AcademicRiskDistributionChart;
