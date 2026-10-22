import React from 'react';

export interface FilterOption {
  label: string;
  value: string | number;
}

interface FilterPanelProps {
  departments?: FilterOption[];
  batches?: FilterOption[];
  sections?: FilterOption[];
  riskCategories?: FilterOption[];
  
  selectedDepartment?: number;
  selectedBatch?: number;
  selectedSection?: number;
  selectedRisk?: string;
  searchQuery?: string;
  
  onDepartmentChange: (val?: number) => void;
  onBatchChange: (val?: number) => void;
  onSectionChange: (val?: number) => void;
  onRiskChange: (val?: string) => void;
  onSearchChange: (val: string) => void;
  
  onClearFilters: () => void;
}

export const FilterPanel: React.FC<FilterPanelProps> = ({
  departments = [],
  batches = [],
  sections = [],
  riskCategories = [],
  selectedDepartment,
  selectedBatch,
  selectedSection,
  selectedRisk,
  searchQuery,
  onDepartmentChange,
  onBatchChange,
  onSectionChange,
  onRiskChange,
  onSearchChange,
  onClearFilters
}) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 flex flex-wrap gap-4 items-end">
      
      {/* Department Filter */}
      {departments.length > 0 && (
        <div className="flex flex-col gap-1 min-w-[150px]">
          <label className="text-xs font-semibold text-gray-500 uppercase">Department</label>
          <select 
            className="border border-gray-200 rounded p-2 text-sm bg-gray-50"
            value={selectedDepartment || ''}
            onChange={(e) => onDepartmentChange(e.target.value ? Number(e.target.value) : undefined)}
          >
            <option value="">All Departments</option>
            {departments.map(d => (
              <option key={`dept-${d.value}`} value={d.value}>{d.label}</option>
            ))}
          </select>
        </div>
      )}

      {/* Batch Filter */}
      {batches.length > 0 && (
        <div className="flex flex-col gap-1 min-w-[150px]">
          <label className="text-xs font-semibold text-gray-500 uppercase">Batch</label>
          <select 
            className="border border-gray-200 rounded p-2 text-sm bg-gray-50 disabled:opacity-50"
            value={selectedBatch || ''}
            onChange={(e) => onBatchChange(e.target.value ? Number(e.target.value) : undefined)}
            disabled={!selectedDepartment}
          >
            <option value="">All Batches</option>
            {batches.map(b => (
              <option key={`batch-${b.value}`} value={b.value}>{b.label}</option>
            ))}
          </select>
        </div>
      )}

      {/* Section Filter */}
      {sections.length > 0 && (
        <div className="flex flex-col gap-1 min-w-[150px]">
          <label className="text-xs font-semibold text-gray-500 uppercase">Section</label>
          <select 
            className="border border-gray-200 rounded p-2 text-sm bg-gray-50 disabled:opacity-50"
            value={selectedSection || ''}
            onChange={(e) => onSectionChange(e.target.value ? Number(e.target.value) : undefined)}
            disabled={!selectedBatch}
          >
            <option value="">All Sections</option>
            {sections.map(s => (
              <option key={`sec-${s.value}`} value={s.value}>{s.label}</option>
            ))}
          </select>
        </div>
      )}

      {/* Risk Category Filter */}
      {riskCategories.length > 0 && (
        <div className="flex flex-col gap-1 min-w-[150px]">
          <label className="text-xs font-semibold text-gray-500 uppercase">Risk Category</label>
          <select 
            className="border border-gray-200 rounded p-2 text-sm bg-gray-50"
            value={selectedRisk || ''}
            onChange={(e) => onRiskChange(e.target.value || undefined)}
          >
            <option value="">All Categories</option>
            {riskCategories.map(r => (
              <option key={`risk-${r.value}`} value={r.value}>{r.label}</option>
            ))}
          </select>
        </div>
      )}

      {/* Search Filter */}
      <div className="flex flex-col gap-1 flex-grow min-w-[200px]">
        <label className="text-xs font-semibold text-gray-500 uppercase">Search Student/USN</label>
        <input 
          type="text" 
          placeholder="e.g. 4SF21CS001 or John Doe"
          className="border border-gray-200 rounded p-2 text-sm bg-gray-50 w-full"
          value={searchQuery || ''}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>

      <button 
        onClick={onClearFilters}
        className="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors text-sm font-medium"
      >
        Clear Filters
      </button>

    </div>
  );
};
