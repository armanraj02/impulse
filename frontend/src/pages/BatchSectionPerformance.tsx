import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getDepartments, getBatchesPerformance, getSectionsPerformance } from '../services/api';
import type { Department, BatchPerformanceExtended, SectionPerformanceExtended } from '../types/api';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';
import { RefreshCw } from 'lucide-react';
import BatchPerformanceChart from '../components/charts/BatchPerformanceChart';
import SectionPerformanceChart from '../components/charts/SectionPerformanceChart';
import BatchPerformanceTable from '../components/tables/BatchPerformanceTable';
import SectionPerformanceTable from '../components/tables/SectionPerformanceTable';

const BatchSectionPerformance: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const departmentIdParam = searchParams.get('department');
  const batchIdParam = searchParams.get('batch');

  const [departments, setDepartments] = useState<Department[]>([]);
  const [batches, setBatches] = useState<BatchPerformanceExtended[]>([]);
  const [sections, setSections] = useState<SectionPerformanceExtended[]>([]);
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    setError(false);
    try {
      const deptId = departmentIdParam ? parseInt(departmentIdParam, 10) : undefined;
      const batchId = batchIdParam ? parseInt(batchIdParam, 10) : undefined;

      const sectionParams: any = {};
      if (deptId) sectionParams.department_id = deptId;
      if (batchId) sectionParams.batch_id = batchId;

      const [depts, batchData, sectionData] = await Promise.all([
        departments.length === 0 ? getDepartments() : Promise.resolve(departments),
        getBatchesPerformance(deptId ? { department_id: deptId } : undefined),
        getSectionsPerformance(sectionParams)
      ]);

      if (departments.length === 0) setDepartments(depts);
      setBatches(batchData);
      setSections(sectionData);
    } catch (err) {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [departmentIdParam, batchIdParam]);

  const handleDepartmentChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    if (val) {
      setSearchParams({ department: val }); // Clear batch when department changes
    } else {
      setSearchParams({});
    }
  };

  const handleBatchChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    const newParams: any = {};
    if (departmentIdParam) newParams.department = departmentIdParam;
    if (val) newParams.batch = val;
    setSearchParams(newParams);
  };

  if (loading && departments.length === 0) return <LoadingState />;
  if (error && departments.length === 0) return <ErrorState onRetry={fetchData} />;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Batch & Section Performance</h1>
          <p className="text-sm text-slate-500">Identify performance differences across batches and sections.</p>
        </div>
        <div className="flex items-center gap-4">
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

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Department</label>
          <select 
            className="w-full bg-slate-50 border border-slate-200 text-slate-700 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={departmentIdParam || ''}
            onChange={handleDepartmentChange}
          >
            <option value="">All Departments</option>
            {departments.map(d => (
              <option key={d.department_id} value={d.department_id}>{d.department_name}</option>
            ))}
          </select>
        </div>
        
        <div className="flex-1">
          <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Batch</label>
          <select 
            className="w-full bg-slate-50 border border-slate-200 text-slate-700 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={batchIdParam || ''}
            onChange={handleBatchChange}
          >
            <option value="">All Batches</option>
            {batches.map(b => (
              <option key={b.batch_id} value={b.batch_id}>{b.batch_name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Content */}
      {loading ? (
        <LoadingState />
      ) : (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
            {batches.length > 0 ? (
              <BatchPerformanceChart data={batches} />
            ) : (
              <EmptyState message="No batch data available for the selected filters." />
            )}
            
            {sections.length > 0 ? (
              <SectionPerformanceChart data={sections} />
            ) : (
              <EmptyState message="No section data available for the selected filters." />
            )}
          </div>
          
          <div className="grid grid-cols-1 gap-6 mt-8">
            {batches.length > 0 && <BatchPerformanceTable data={batches} />}
            {sections.length > 0 && <SectionPerformanceTable data={sections} />}
          </div>
        </>
      )}
    </div>
  );
};

export default BatchSectionPerformance;
