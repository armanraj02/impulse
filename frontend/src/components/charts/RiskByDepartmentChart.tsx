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
import { getDepartmentRiskDistribution } from '../../services/api';
import { LoadingState, ErrorState, EmptyState } from '../common/States';

const COLORS: Record<string, string> = {
  'HIGH': '#ef4444',
  'MEDIUM': '#f59e0b',
  'LOW': '#3b82f6',
  'NONE': '#10b981',
  'Unknown': '#94a3b8'
};

const RiskByDepartmentChart: React.FC = () => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [categories, setCategories] = useState<string[]>([]);

  const fetchData = async () => {
    setLoading(true);
    setError(false);
    try {
      const response = await getDepartmentRiskDistribution();
      
      // Transform data for stacked bar chart: [{ department_name: 'CSE', HIGH: 10, LOW: 50 }, ...]
      const deptMap: Record<string, any> = {};
      const catSet = new Set<string>();
      
      response.forEach(item => {
        if (!deptMap[item.department_name]) {
          deptMap[item.department_name] = { department_name: item.department_name };
        }
        deptMap[item.department_name][item.category] = item.count;
        catSet.add(item.category);
      });
      
      setData(Object.values(deptMap));
      setCategories(Array.from(catSet));
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

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-[400px] flex flex-col">
      <h3 className="text-base font-semibold text-slate-800 mb-6">Department Risk Overview</h3>
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
            />
            <Tooltip 
              cursor={{ fill: '#f1f5f9' }}
              contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
            {categories.map((category) => (
              <Bar 
                key={category}
                dataKey={category} 
                stackId="a" 
                fill={COLORS[category] || COLORS['Unknown']} 
                maxBarSize={50}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default RiskByDepartmentChart;
