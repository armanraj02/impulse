import React, { useEffect, useState } from 'react';
import { getOverview } from '../services/api';
import type { OverviewData } from '../types/api';
import { LoadingState, ErrorState } from '../components/common/States';
import KpiCard from '../components/common/KpiCard';
import { Users, AlertTriangle, GraduationCap, CalendarCheck, MessageSquare, Lightbulb, RefreshCw } from 'lucide-react';
import DepartmentPerformanceChart from '../components/charts/DepartmentPerformanceChart';
import RiskDistributionChart from '../components/charts/RiskDistributionChart';
import CoursePerformanceChart from '../components/charts/CoursePerformanceChart';
import InsightsTable from '../components/tables/InsightsTable';

const ExecutiveOverview: React.FC = () => {
  const [data, setData] = useState<OverviewData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [lastRefreshed, setLastRefreshed] = useState<Date>(new Date());

  const fetchData = async () => {
    setLoading(true);
    setError(false);
    try {
      const overview = await getOverview();
      setData(overview);
      setLastRefreshed(new Date());
    } catch (err) {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading && !data) return <LoadingState />;
  if (error && !data) return <ErrorState onRetry={fetchData} />;
  
  // Create a safe default data object in case data is null but we are rendering
  const safeData = data || {
    total_students: 0,
    students_at_risk: 0,
    average_academic_performance: 0,
    average_attendance: 0,
    average_feedback_rating: 0,
    total_insights: 0,
    total_departments: 0,
    total_courses: 0
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Executive Overview</h1>
          <p className="text-sm text-slate-500">Academic performance, attendance, feedback and risk intelligence</p>
        </div>
        <div className="flex items-center gap-4 text-sm text-slate-500">
          <div className="text-right">
            <span className="block font-medium text-slate-700">Reporting Period</span>
            <span>Up to {lastRefreshed.toLocaleDateString()}</span>
          </div>
          <button 
            onClick={fetchData}
            disabled={loading}
            className="p-2 bg-white border border-slate-200 rounded-md hover:bg-slate-50 transition-colors disabled:opacity-50"
            title="Refresh Overview"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <KpiCard 
          title="Total Students" 
          value={safeData.total_students.toLocaleString()} 
          icon={Users} 
        />
        <KpiCard 
          title="Students at Risk" 
          value={safeData.students_at_risk.toLocaleString()} 
          icon={AlertTriangle} 
          className="border-rose-100 bg-rose-50/10"
        />
        <KpiCard 
          title="Avg. Academic Performance" 
          value={`${safeData.average_academic_performance.toFixed(2)}%`} 
          icon={GraduationCap} 
        />
        <KpiCard 
          title="Avg. Attendance" 
          value={`${safeData.average_attendance.toFixed(2)}%`} 
          icon={CalendarCheck} 
        />
        <KpiCard 
          title="Avg. Feedback Rating" 
          value={`${safeData.average_feedback_rating.toFixed(2)} / 5.0`} 
          icon={MessageSquare} 
        />
        <KpiCard 
          title="Generated Insights" 
          value={safeData.total_insights.toLocaleString()} 
          icon={Lightbulb} 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <DepartmentPerformanceChart />
        <RiskDistributionChart />
      </div>
      
      <div className="grid grid-cols-1 gap-6 mt-8">
        <CoursePerformanceChart data={[]} />
      </div>
      
      <div className="grid grid-cols-1 gap-6 mt-8">
        <InsightsTable />
      </div>
    </div>
  );
};

export default ExecutiveOverview;
