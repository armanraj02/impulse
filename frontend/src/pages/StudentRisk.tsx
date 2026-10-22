import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  getStudentsRisk, 
  getStudentRiskDistribution, 
  getDepartments, 
  getBatchesPerformance, 
  getSectionsPerformance 
} from '../services/api';
import { Users, AlertTriangle, AlertCircle, Clock, CheckCircle } from 'lucide-react';
import type { 
  StudentRiskExtended, 
  RiskDistribution, 
  Department, 
  BatchPerformanceExtended, 
  SectionPerformanceExtended 
} from '../types/api';
import { FilterPanel } from '../components/common/FilterPanel';
import { StudentRiskTable } from '../components/tables/StudentRiskTable';
import { StudentRiskDistributionChart } from '../components/charts/StudentRiskDistributionChart';
import KpiCard from '../components/common/KpiCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';

export const StudentRisk: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  
  // URL States
  const page = parseInt(searchParams.get('page') || '1', 10);
  const departmentId = searchParams.get('department_id') ? parseInt(searchParams.get('department_id')!, 10) : undefined;
  const batchId = searchParams.get('batch_id') ? parseInt(searchParams.get('batch_id')!, 10) : undefined;
  const sectionId = searchParams.get('section_id') ? parseInt(searchParams.get('section_id')!, 10) : undefined;
  const riskCategory = searchParams.get('risk_category') || undefined;
  const searchQuery = searchParams.get('search') || undefined;
  
  // Data States
  const [students, setStudents] = useState<StudentRiskExtended[]>([]);
  const [totalStudents, setTotalStudents] = useState(0);
  const [distribution, setDistribution] = useState<RiskDistribution[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filter Options Data
  const [departments, setDepartments] = useState<Department[]>([]);
  const [batches, setBatches] = useState<BatchPerformanceExtended[]>([]);
  const [sections, setSections] = useState<SectionPerformanceExtended[]>([]);

  // Initial Data Load (Dropdowns + Distribution)
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [deptRes, distRes] = await Promise.all([
          getDepartments(),
          getStudentRiskDistribution()
        ]);
        setDepartments(deptRes);
        setDistribution(distRes);
      } catch (err) {
        console.error("Failed to load initial data", err);
      }
    };
    fetchInitialData();
  }, []);

  // Fetch batches when department changes
  useEffect(() => {
    const fetchBatches = async () => {
      if (!departmentId) {
        setBatches([]);
        return;
      }
      try {
        const b = await getBatchesPerformance({ department_id: departmentId });
        setBatches(b);
      } catch (err) {
        console.error("Failed to load batches", err);
      }
    };
    fetchBatches();
  }, [departmentId]);

  // Fetch sections when batch changes
  useEffect(() => {
    const fetchSections = async () => {
      if (!batchId || !departmentId) {
        setSections([]);
        return;
      }
      try {
        const s = await getSectionsPerformance({ department_id: departmentId, batch_id: batchId });
        setSections(s);
      } catch (err) {
        console.error("Failed to load sections", err);
      }
    };
    fetchSections();
  }, [departmentId, batchId]);

  // Main Data Load
  useEffect(() => {
    const fetchRiskData = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await getStudentsRisk(
          page, 
          10, 
          departmentId, 
          batchId, 
          sectionId, 
          riskCategory, 
          searchQuery
        );
        setStudents(res.items);
        setTotalStudents(res.total);
      } catch (err) {
        setError('Failed to fetch student risk data. Please try again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchRiskData();
  }, [page, departmentId, batchId, sectionId, riskCategory, searchQuery]);

  // Handlers
  const updateParams = (newParams: Record<string, string | null>) => {
    const current = Object.fromEntries(searchParams.entries());
    Object.entries(newParams).forEach(([key, value]) => {
      if (value === null) {
        delete current[key];
      } else {
        current[key] = value;
      }
    });
    setSearchParams(current);
  };

  const handleDepartmentChange = (val?: number) => {
    updateParams({
      department_id: val ? val.toString() : null,
      batch_id: null,
      section_id: null,
      page: '1'
    });
  };

  const handleBatchChange = (val?: number) => {
    updateParams({
      batch_id: val ? val.toString() : null,
      section_id: null,
      page: '1'
    });
  };

  const handleSectionChange = (val?: number) => {
    updateParams({
      section_id: val ? val.toString() : null,
      page: '1'
    });
  };

  const handleRiskChange = (val?: string) => {
    updateParams({
      risk_category: val || null,
      page: '1'
    });
  };

  const handleSearchChange = (val: string) => {
    updateParams({
      search: val || null,
      page: '1'
    });
  };

  const handleClearFilters = () => {
    setSearchParams({});
  };

  const getKpiValue = (cat: string) => {
    return distribution.find(d => d.category === cat)?.count || 0;
  };

  const totalAllStudents = distribution.reduce((sum, item) => sum + item.count, 0);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Student Risk Intelligence</h1>
          <p className="text-sm text-gray-500 mt-1">Identify and monitor students requiring academic or attendance attention.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <KpiCard title="Total Students" value={totalAllStudents} icon={Users} />
        <KpiCard title="High Risk" value={getKpiValue('High Risk')} icon={AlertTriangle} className="border-l-4 border-l-red-500" />
        <KpiCard title="Attendance Risk" value={getKpiValue('Attendance Risk')} icon={Clock} className="border-l-4 border-l-amber-500" />
        <KpiCard title="Academic Risk" value={getKpiValue('Academic Risk')} icon={AlertCircle} className="border-l-4 border-l-amber-400" />
        <KpiCard title="No Risk" value={getKpiValue('No Risk')} icon={CheckCircle} className="border-l-4 border-l-green-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <StudentRiskDistributionChart data={distribution} />
        </div>
        
        <div className="lg:col-span-3 space-y-4">
          <FilterPanel
            departments={departments.map(d => ({ label: d.department_name, value: d.department_id }))}
            batches={batches.map(b => ({ label: b.batch_name, value: b.batch_id }))}
            sections={sections.map(s => ({ label: s.section_name, value: s.section_id }))}
            riskCategories={[
              { label: 'High Risk', value: 'High Risk' },
              { label: 'Attendance Risk', value: 'Attendance Risk' },
              { label: 'Academic Risk', value: 'Academic Risk' },
              { label: 'No Risk', value: 'No Risk' },
            ]}
            selectedDepartment={departmentId}
            selectedBatch={batchId}
            selectedSection={sectionId}
            selectedRisk={riskCategory}
            searchQuery={searchQuery}
            onDepartmentChange={handleDepartmentChange}
            onBatchChange={handleBatchChange}
            onSectionChange={handleSectionChange}
            onRiskChange={handleRiskChange}
            onSearchChange={handleSearchChange}
            onClearFilters={handleClearFilters}
          />

          {loading ? (
            <LoadingState message="Loading risk intelligence data..." />
          ) : error ? (
            <ErrorState message={error} />
          ) : students.length === 0 ? (
            <EmptyState message="No students found matching the selected filters." />
          ) : (
            <>
              <StudentRiskTable students={students} />
              
              <div className="flex justify-between items-center bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                <span className="text-sm text-gray-500">
                  Showing {((page - 1) * 10) + 1} to {Math.min(page * 10, totalStudents)} of {totalStudents} students
                </span>
                <div className="flex space-x-2">
                  <button
                    disabled={page <= 1}
                    onClick={() => updateParams({ page: (page - 1).toString() })}
                    className="px-3 py-1 border border-gray-200 rounded text-sm disabled:opacity-50 hover:bg-gray-50"
                  >
                    Previous
                  </button>
                  <button
                    disabled={page * 10 >= totalStudents}
                    onClick={() => updateParams({ page: (page + 1).toString() })}
                    className="px-3 py-1 border border-gray-200 rounded text-sm disabled:opacity-50 hover:bg-gray-50"
                  >
                    Next
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
