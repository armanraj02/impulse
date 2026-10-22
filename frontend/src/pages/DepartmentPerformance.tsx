import React, { useEffect, useState } from 'react';
import { getOverview, getDepartmentsPerformance } from '../services/api';
import type { OverviewData, DepartmentPerformanceExtended } from '../types/api';
import { LoadingState, ErrorState } from '../components/common/States';
import KpiCard from '../components/common/KpiCard';
import { Users, AlertTriangle, GraduationCap, CalendarCheck, MessageSquare, Building2, RefreshCw } from 'lucide-react';
import DepartmentComparisonChart from '../components/charts/DepartmentComparisonChart';
import RiskByDepartmentChart from '../components/charts/RiskByDepartmentChart';
import DepartmentSummaryTable from '../components/tables/DepartmentSummaryTable';

const DepartmentPerformance: React.FC = () => {
  const [overview, setOverview] = useState<OverviewData | null>(null);
  const [deptData, setDeptData] = useState<DepartmentPerformanceExtended[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [lastRefreshed, setLastRefreshed] = useState<Date>(new Date());

  const fetchData = async () => {
    setLoading(true);
    setError(false);
    try {
      const [overviewRes, deptRes] = await Promise.all([
        getOverview(),
        getDepartmentsPerformance()
      ]);
      setOverview(overviewRes);
      setDeptData(deptRes);
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

  if (loading && (!overview || !deptData)) return <LoadingState />;
  if (error && (!overview || !deptData)) return <ErrorState onRetry={fetchData} />;

  const safeOverview = overview || {
    total_students: 0,
    students_at_risk: 0,
    average_academic_performance: 0,
    average_attendance: 0,
    average_feedback_rating: 0,
    total_insights: 0,
    total_departments: 0,
    total_courses: 0
  };

  const safeDeptData = deptData || [];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Department Performance</h1>
          <p className="text-sm text-slate-500">Compare academic, attendance, feedback and risk indicators across departments.</p>
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
            title="Refresh Data"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <KpiCard 
          title="Total Departments" 
          value={safeOverview.total_departments.toLocaleString()} 
          icon={Building2} 
        />
        <KpiCard 
          title="Total Students" 
          value={safeOverview.total_students.toLocaleString()} 
          icon={Users} 
        />
        <KpiCard 
          title="Avg. Academic Performance" 
          value={`${safeOverview.average_academic_performance.toFixed(2)}%`} 
          icon={GraduationCap} 
        />
        <KpiCard 
          title="Avg. Attendance" 
          value={`${safeOverview.average_attendance.toFixed(2)}%`} 
          icon={CalendarCheck} 
        />
        <KpiCard 
          title="Students at Risk" 
          value={safeOverview.students_at_risk.toLocaleString()} 
          icon={AlertTriangle} 
          className="border-rose-100 bg-rose-50/10"
        />
        <KpiCard 
          title="Avg. Feedback Rating" 
          value={`${safeOverview.average_feedback_rating.toFixed(2)} / 5.0`} 
          icon={MessageSquare} 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <DepartmentComparisonChart />
        <RiskByDepartmentChart />
      </div>
      
      <div className="grid grid-cols-1 gap-6 mt-8">
        <DepartmentSummaryTable data={safeDeptData} />
      </div>
    </div>
  );
};

export default DepartmentPerformance;
