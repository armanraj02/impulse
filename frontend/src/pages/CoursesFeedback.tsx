import React, { useState, useEffect, useMemo } from 'react';
import { 
  BookOpen, 
  MessageSquare,
  Star,
  GraduationCap
} from 'lucide-react';
import KpiCard from '../components/common/KpiCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';
import CoursePerformanceChart from '../components/charts/CoursePerformanceChart';
import FeedbackDistributionChart from '../components/charts/FeedbackDistributionChart';
import CoursePerformanceTable from '../components/tables/CoursePerformanceTable';
import ModuleFeedbackTable from '../components/tables/ModuleFeedbackTable';
import InstructorFeedbackTable from '../components/tables/InstructorFeedbackTable';
import { 
  getDepartments,
  getCoursesPerformance,
  getFeedback,
  getModuleFeedback,
  getInstructorFeedback
} from '../services/api';
import type { 
  Department,
  Course,
  FeedbackSummary,
  ModuleFeedback,
  InstructorFeedback
} from '../types/api';

const CoursesFeedback: React.FC = () => {
  // Filters
  const [departmentId, setDepartmentId] = useState<number | ''>('');
  const [courseId, setCourseId] = useState<number | ''>('');
  
  // Data States
  const [departments, setDepartments] = useState<Department[]>([]);
  const [coursesFilterList, setCoursesFilterList] = useState<Course[]>([]);
  
  // Overall Feedback Summary
  const [feedbackSummary, setFeedbackSummary] = useState<FeedbackSummary | null>(null);

  // Pagination & Data states for Tables/Charts
  const [coursesPage, setCoursesPage] = useState(1);
  const [coursesData, setCoursesData] = useState<{items: Course[], total: number}>({items: [], total: 0});
  
  const [modulesPage, setModulesPage] = useState(1);
  const [modulesData, setModulesData] = useState<{items: ModuleFeedback[], total: number}>({items: [], total: 0});
  
  const [instructorsPage, setInstructorsPage] = useState(1);
  const [instructorsData, setInstructorsData] = useState<{items: InstructorFeedback[], total: number}>({items: [], total: 0});

  // UI States
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Fetch initial filters
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const deps = await getDepartments();
        setDepartments(deps);
        const overall = await getFeedback();
        setFeedbackSummary(overall);
      } catch (err: any) {
        setError(err.message || 'Failed to load initial data');
      }
    };
    fetchInitialData();
  }, []);

  // Fetch Courses for filter dropdown based on department
  useEffect(() => {
    const fetchFilterCourses = async () => {
      try {
        // Fetch a large page to populate dropdown (we could also rely on a specific endpoint if we had one)
        const params: any = { page: 1, page_size: 100 };
        if (departmentId !== '') params.department_id = departmentId;
        const res = await getCoursesPerformance(params);
        setCoursesFilterList(res.items);
      } catch (e) {
        console.error('Failed to fetch courses for filter');
      }
    };
    fetchFilterCourses();
  }, [departmentId]);

  // Main data fetcher
  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      setError(null);
      try {
        const cParams: any = { page: coursesPage, page_size: 10 };
        if (departmentId !== '') cParams.department_id = departmentId;
        if (courseId !== '') cParams.course_id = courseId;
        
        const mParams: any = { page: modulesPage, page_size: 10 };
        if (courseId !== '') mParams.course_id = courseId;

        const iParams: any = { page: instructorsPage, page_size: 10 };

        const [coursesRes, modulesRes, instructorsRes] = await Promise.all([
          getCoursesPerformance(cParams),
          getModuleFeedback(mParams),
          getInstructorFeedback(iParams)
        ]);

        setCoursesData({ items: coursesRes.items, total: coursesRes.total });
        setModulesData({ items: modulesRes.items, total: modulesRes.total });
        setInstructorsData({ items: instructorsRes.items, total: instructorsRes.total });
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [departmentId, courseId, coursesPage, modulesPage, instructorsPage]);

  const handleResetFilters = () => {
    setDepartmentId('');
    setCourseId('');
    setCoursesPage(1);
    setModulesPage(1);
    setInstructorsPage(1);
  };

  // KPIs
  const avgCourseAcademic = useMemo(() => {
    if (!coursesData.items.length) return 0;
    const sum = coursesData.items.reduce((acc, curr) => acc + curr.average_assessment_percentage, 0);
    return sum / coursesData.items.length;
  }, [coursesData.items]);

  if (loading && !coursesData.items.length) {
    return <LoadingState message="Loading Course & Feedback Intelligence..." />;
  }

  if (error && !coursesData.items.length) {
    return <ErrorState message={error} onRetry={handleResetFilters} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Course & Feedback Intelligence</h1>
          <p className="text-slate-500 mt-1">Course performance, feedback quality, module ratings and instructor feedback.</p>
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
              setCourseId('');
              setCoursesPage(1);
              setModulesPage(1);
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
          <label className="block text-sm font-medium text-slate-700 mb-1">Course</label>
          <select
            value={courseId}
            onChange={(e) => {
              setCourseId(e.target.value === '' ? '' : Number(e.target.value));
              setCoursesPage(1);
              setModulesPage(1);
            }}
            className="w-full rounded-lg border-slate-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm"
          >
            <option value="">All Courses</option>
            {coursesFilterList.map((c) => (
              <option key={c.course_id} value={c.course_id}>{c.course_name} ({c.course_code})</option>
            ))}
          </select>
        </div>
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
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KpiCard
          title="Average Course Academic %"
          value={`${avgCourseAcademic.toFixed(1)}%`}
          icon={GraduationCap}
        />
        <KpiCard
          title="Average Feedback Rating"
          value={`${feedbackSummary?.average_rating?.toFixed(2) || '0.00'} / 5`}
          icon={Star}
        />
        <KpiCard
          title="Total Feedback Responses"
          value={feedbackSummary?.total_rating_responses?.toLocaleString() || '0'}
          icon={MessageSquare}
        />
        <KpiCard
          title="Courses Listed"
          value={coursesData.total.toLocaleString()}
          icon={BookOpen}
        />
      </div>

      {/* Course Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 h-[450px]">
          <CoursePerformanceTable 
            data={coursesData.items} 
            page={coursesPage} 
            pageSize={10} 
            total={coursesData.total} 
            onPageChange={setCoursesPage} 
          />
        </div>
        <div className="h-[450px]">
          {coursesData.items.length > 0 ? (
            <CoursePerformanceChart data={coursesData.items} />
          ) : (
            <EmptyState message="No courses available. Try adjusting your filters." />
          )}
        </div>
      </div>

      {/* Feedback Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 h-[450px]">
          {modulesData.items.length > 0 ? (
            <FeedbackDistributionChart data={modulesData.items} />
          ) : (
             <EmptyState message="No module feedback available. Try adjusting your filters." />
          )}
        </div>
        <div className="lg:col-span-2 h-[450px]">
          <ModuleFeedbackTable 
            data={modulesData.items} 
            page={modulesPage} 
            pageSize={10} 
            total={modulesData.total} 
            onPageChange={setModulesPage} 
          />
        </div>
      </div>

      {/* Instructors Section */}
      <div className="grid grid-cols-1 gap-6">
        <div className="h-[450px]">
          <InstructorFeedbackTable 
            data={instructorsData.items} 
            page={instructorsPage} 
            pageSize={10} 
            total={instructorsData.total} 
            onPageChange={setInstructorsPage} 
          />
        </div>
      </div>

    </div>
  );
};

export default CoursesFeedback;
