import React, { useState } from 'react';
import type { SectionPerformanceExtended } from '../../types/api';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface Props {
  data: SectionPerformanceExtended[];
}

const SectionPerformanceTable: React.FC<Props> = ({ data }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;
  const totalPages = Math.max(1, Math.ceil(data.length / pageSize));
  const safePage = Math.min(currentPage, totalPages);
  const paginatedData = data.slice((safePage - 1) * pageSize, safePage * pageSize);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="px-6 py-5 border-b border-slate-200 flex justify-between items-center">
        <h3 className="text-base font-semibold text-slate-800">Section Performance</h3>
        <span className="text-xs text-slate-500 font-medium">Total: {data.length} sections</span>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[600px]">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <th className="px-6 py-3">Section</th>
              <th className="px-6 py-3 text-right">Students</th>
              <th className="px-6 py-3 text-right">Academic %</th>
              <th className="px-6 py-3 text-right">Attendance %</th>
              <th className="px-6 py-3 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {paginatedData.map((section) => {
              let statusText = 'Healthy';
              let statusStyle = 'bg-emerald-100 text-emerald-700';
              
              if (section.average_assessment_percentage < 60 || section.average_attendance_percentage < 70) {
                statusText = 'Attention Required';
                statusStyle = 'bg-rose-100 text-rose-700';
              } else if (section.average_assessment_percentage < 75 || section.average_attendance_percentage < 85) {
                statusText = 'Monitor';
                statusStyle = 'bg-amber-100 text-amber-700';
              }

              return (
                <tr key={section.section_id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-slate-900">{section.section_name}</div>
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700">
                    {section.total_students.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700 font-medium">
                    {section.average_assessment_percentage.toFixed(2)}%
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700 font-medium">
                    {section.average_attendance_percentage.toFixed(2)}%
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusStyle}`}>
                      {statusText}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between text-xs text-slate-600">
          <div>
            Showing {(safePage - 1) * pageSize + 1} to {Math.min(safePage * pageSize, data.length)} of {data.length} entries
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={safePage === 1}
              className="p-1 rounded border border-slate-200 bg-white hover:bg-slate-100 disabled:opacity-40"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span>Page {safePage} of {totalPages}</span>
            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={safePage === totalPages}
              className="p-1 rounded border border-slate-200 bg-white hover:bg-slate-100 disabled:opacity-40"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SectionPerformanceTable;
