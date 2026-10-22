import React from 'react';
import type { Student } from '../../types/api';

interface Props {
  data: Student[];
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
}

const AcademicPerformanceTable: React.FC<Props> = ({ 
  data, 
  page, 
  pageSize, 
  total, 
  onPageChange 
}) => {
  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-full">
      <div className="p-4 border-b border-slate-200">
        <h3 className="font-semibold text-slate-800">Student Academic Performance</h3>
      </div>
      
      <div className="overflow-x-auto flex-1">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
            <tr>
              <th className="px-4 py-3">Student</th>
              <th className="px-4 py-3">Department</th>
              <th className="px-4 py-3">Batch</th>
              <th className="px-4 py-3">Academic %</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {data.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-slate-500">
                  No students found for the selected criteria.
                </td>
              </tr>
            ) : (
              data.map((row) => {
                const isConcern = (row.average_assessment_percentage || 0) < 50;
                return (
                  <tr key={row.student_id} className="hover:bg-slate-50">
                    <td className="px-4 py-3">
                      <div className="font-medium text-slate-900">{row.student_name}</div>
                      <div className="text-slate-500 text-xs">{row.usn}</div>
                    </td>
                    <td className="px-4 py-3 text-slate-600">{row.branch_name}</td>
                    <td className="px-4 py-3 text-slate-600">{row.batch_name}</td>
                    <td className="px-4 py-3 text-slate-600 font-medium">
                      {(row.average_assessment_percentage || 0).toFixed(2)}%
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium ${
                        isConcern ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700'
                      }`}>
                        {isConcern ? 'Academic Concern' : 'Healthy'}
                      </span>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      <div className="p-4 border-t border-slate-200 flex items-center justify-between bg-slate-50">
        <div className="text-sm text-slate-600">
          Showing {Math.min((page - 1) * pageSize + 1, total)} to {Math.min(page * pageSize, total)} of {total} students
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page === 1}
            className="px-3 py-1 text-sm bg-white border border-slate-200 rounded-md disabled:opacity-50 hover:bg-slate-50 transition-colors"
          >
            Previous
          </button>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages}
            className="px-3 py-1 text-sm bg-white border border-slate-200 rounded-md disabled:opacity-50 hover:bg-slate-50 transition-colors"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default AcademicPerformanceTable;
