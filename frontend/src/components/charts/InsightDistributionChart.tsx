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
import type { InsightDistributionItem } from '../../types/api';
import { EmptyState } from '../common/States';

interface InsightDistributionChartProps {
  data: InsightDistributionItem[];
}

export const InsightDistributionChart: React.FC<InsightDistributionChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-[300px] flex items-center justify-center">
        <EmptyState message="No insights have been generated yet." />
      </div>
    );
  }

  // Transform data to group by insight_type, with entity_types as bars if there are multiple.
  // Or simpler: Just map to `{ name: \`\${item.insight_type} - \${item.entity_type}\`, count: item.count }`
  const formattedData = data.map(item => ({
    name: `${item.insight_type} (${item.entity_type})`,
    count: item.count
  }));

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={formattedData}
          margin={{ top: 20, right: 30, left: 0, bottom: 20 }}
          layout="vertical"
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
          <XAxis type="number" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis 
            dataKey="name" 
            type="category" 
            stroke="#64748b" 
            fontSize={12} 
            tickLine={false} 
            axisLine={false} 
            width={120} 
          />
          <Tooltip
            cursor={{ fill: '#f8fafc' }}
            contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
          />
          <Legend wrapperStyle={{ paddingTop: '10px' }} />
          <Bar 
            dataKey="count" 
            name="Insights"
            fill="#3b82f6" 
            radius={[0, 4, 4, 0]} 
            barSize={32}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
