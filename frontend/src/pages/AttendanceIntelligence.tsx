import React, { useState, useEffect } from 'react';
import { 
  Users, 
  CalendarCheck,
  AlertTriangle,
  BookOpen
} from 'lucide-react';
import KpiCard from '../components/common/KpiCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';
import AttendanceRiskDistributionChart from '../components/charts/AttendanceRiskDistributionChart';
import BatchAttendanceChart from '../components/charts/BatchAttendanceChart';
import AttendancePerformanceTable from '../components/tables/AttendancePerformanceTable';
import { 
  getDepartments,
  getAttendanceOverview,
  getAttendanceStudents,
  getBatchesPerformance
} from '../services/api';
import type { 
  Department,
  AttendanceOverview,
  Student,
  BatchPerformanceExtended
} from '../types/api';

const AttendanceIntelligence: React.FC = () => {
  // Filters
  const [departmentId, setDepartmentId] = useState<number | ''>('');
  const [batchId, setBatchId] = useState<number | ''>('');
  const [sectionId, setSectionId] = useState<number | ''>(''); // If sections could be fetched dynamically, we'd add that
  
  // Data States
  const [departments, setDepartments] = useState<Department[]>([]);
  const [batches, setBatches] = useState<BatchPerformanceExtended[]>([]);
  
  const [overview, setOverview] = useState<AttendanceOverview | null>(null);

  // Pagination & Data states for Tables
  const [studentsPage, setStudentsPage] = useState(1);
  const [studentsData, setStudentsData] = useState<{items: Student[], total: number}>({items: [], total: 0});
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const deps = await getDepartments();
        setDepartments(deps);
        const ov = await getAttendanceOverview();
        setOverview(ov);
      } catch (err: any) {
        setError(err.message || 'Failed to load initial data');
      }
    };
    fetchInitialData();
  }, []);

  useEffect(() => {
    const fetchBatches = async () => {
      try {
        const bParams: any = {};
        if (departmentId !== '') bParams.department_id = departmentId;
        const bData = await getBatchesPerformance(bParams);
        setBatches(bData);
      } catch (err) {
        console.error("Failed to load batches");
      }
    };
    fetchBatches();
  }, [departmentId]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      setError(null);
      try {
        const params: any = { page: studentsPage, page_size: 10 };
        if (departmentId !== '') params.department_id = departmentId;
        if (batchId !== '') params.batch_id = batchId;
        if (sectionId !== '') params.section_id = sectionId;

        const studentsRes = await getAttendanceStudents(params);
        setStudentsData({ items: studentsRes.items, total: studentsRes.total });
      } catch (err: any) {
        setError(err.message || 'Failed to load attendance data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [departmentId, batchId, sectionId, studentsPage]);

  const handleResetFilters = () => {
    setDepartmentId('');
    setBatchId('');
    setSectionId('');
    setStudentsPage(1);
  };

  if (loading && !studentsData.items.length && !overview) {
    return <LoadingState message="Loading Attendance Intelligence..." />;
  }

  if (error && !studentsData.items.length && !overview) {
    return <ErrorState message={error} onRetry={handleResetFilters} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Attendance Intelligence</h1>
          <p className="text-slate-500 mt-1">Attendance trends, risk distribution and performance across departments, courses and sections.</p>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-4 items-end">
        <div className="flex-1 w-full">
          <label className="block text-sm font-medium text-slate-700 mb-1">Department</label>
          <select
            value={departmentId}
            onChange={(e) => {
              setDepartmentId(e.target.value === '' ? '' : Number(e.target.value));
              setBatchId('');
              setSectionId('');
              setStudentsPage(1);
            }}
            className="w-full rounded-lg border-slate-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm"
          >
            <option value="">All Departments</option>
            {departments.map((d) => (
              <option key={d.department_id} value={d.department_id}>{d.department_name}</option>
            ))}
          </select>
        </div>
        <div className="flex-1 w-full">
          <label className="block text-sm font-medium text-slate-700 mb-1">Batch</label>
          <select
            value={batchId}
            onChange={(e) => {
              setBatchId(e.target.value === '' ? '' : Number(e.target.value));
              setSectionId('');
              setStudentsPage(1);
            }}
            className="w-full rounded-lg border-slate-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm"
          >
            <option value="">All Batches</option>
            {batches.map((b) => (
              <option key={b.batch_id} value={b.batch_id}>{b.batch_name}</option>
            ))}
          </select>
        </div>
        {/* We can omit section filter unless we fetch sections list, but adding input just in case */}
        <div className="flex-none">
          <button
            onClick={handleResetFilters}
            className="w-full sm:w-auto px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-lg text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition-colors"
          >
            Reset Filters
          </button>
        </div>
      </div>

      {/* KPIs */}
      {overview && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KpiCard
            title="Average Attendance %"
            value={`${overview.average_attendance.toFixed(1)}%`}
            icon={CalendarCheck}
          />
          <KpiCard
            title="Students Below 75%"
            value={overview.students_below_75.toLocaleString()}
            icon={AlertTriangle}
          />
          <KpiCard
            title="Total Students"
            value={overview.total_students.toLocaleString()}
            icon={Users}
          />
          <KpiCard
            title="Courses Analyzed"
            value={overview.total_courses_analyzed.toLocaleString()}
            icon={BookOpen}
          />
        </div>
      )}

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="h-[450px]">
          {overview ? (
            <AttendanceRiskDistributionChart 
              totalStudents={overview.total_students} 
              studentsBelow75={overview.students_below_75} 
            />
          ) : (
             <EmptyState message="No attendance data available." />
          )}
        </div>
        <div className="h-[450px]">
          {batches.length > 0 ? (
            <BatchAttendanceChart data={batches} />
          ) : (
            <EmptyState message="No batch data available." />
          )}
        </div>
      </div>

      {/* Table Section */}
      <div className="h-[500px]">
        <AttendancePerformanceTable 
          data={studentsData.items} 
          page={studentsPage} 
          pageSize={10} 
          total={studentsData.total} 
          onPageChange={setStudentsPage} 
        />
      </div>

    </div>
  );
};

export default AttendanceIntelligence;
