import React from 'react';
import type { BatchPerformanceExtended } from '../../types/api';

interface Props {
  data: BatchPerformanceExtended[];
}

const BatchPerformanceTable: React.FC<Props> = ({ data }) => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="px-6 py-5 border-b border-slate-200">
        <h3 className="text-base font-semibold text-slate-800">Batch Performance</h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[600px]">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <th className="px-6 py-3">Batch Name</th>
              <th className="px-6 py-3 text-right">Students</th>
              <th className="px-6 py-3 text-right">Academic %</th>
              <th className="px-6 py-3 text-right">Attendance %</th>
              <th className="px-6 py-3 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {data.map((batch) => {
              let statusText = 'Healthy';
              let statusStyle = 'bg-emerald-100 text-emerald-700';
              
              if (batch.average_assessment_percentage < 60 || batch.average_attendance_percentage < 70) {
                statusText = 'Attention Required';
                statusStyle = 'bg-rose-100 text-rose-700';
              } else if (batch.average_assessment_percentage < 75 || batch.average_attendance_percentage < 85) {
                statusText = 'Monitor';
                statusStyle = 'bg-amber-100 text-amber-700';
              }

              return (
                <tr key={batch.batch_id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-slate-900">{batch.batch_name}</div>
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700">
                    {batch.total_students.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700 font-medium">
                    {batch.average_assessment_percentage.toFixed(2)}%
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700 font-medium">
                    {batch.average_attendance_percentage.toFixed(2)}%
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
    </div>
  );
};

export default BatchPerformanceTable;
