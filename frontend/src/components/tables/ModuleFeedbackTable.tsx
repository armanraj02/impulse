import React from 'react';
import type { ModuleFeedback } from '../../types/api';

interface Props {
  data: ModuleFeedback[];
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
}

const ModuleFeedbackTable: React.FC<Props> = ({ 
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
        <h3 className="font-semibold text-slate-800">Module Feedback</h3>
      </div>
      
      <div className="overflow-x-auto flex-1">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
            <tr>
              <th className="px-4 py-3">Module Name</th>
              <th className="px-4 py-3">Order</th>
              <th className="px-4 py-3 text-right">Responses</th>
              <th className="px-4 py-3 text-right">Average Rating</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {data.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-slate-500">
                  No modules found.
                </td>
              </tr>
            ) : (
              data.map((row) => (
                <tr key={row.module_id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-900">{row.module_name}</td>
                  <td className="px-4 py-3 text-slate-600">Module {row.module_order}</td>
                  <td className="px-4 py-3 text-right text-slate-600">{row.rating_responses}</td>
                  <td className="px-4 py-3 text-right font-medium">
                    <span className={`px-2 py-1 rounded-md ${
                      row.average_rating >= 4.0 ? 'bg-green-100 text-green-700' :
                      row.average_rating >= 3.0 ? 'bg-amber-100 text-amber-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {row.average_rating.toFixed(2)} / 5
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="p-4 border-t border-slate-200 flex items-center justify-between bg-slate-50">
        <div className="text-sm text-slate-600">
          Showing {Math.min((page - 1) * pageSize + 1, total)} to {Math.min(page * pageSize, total)} of {total} modules
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

export default ModuleFeedbackTable;
