import React from 'react';
import type { DepartmentPerformanceExtended } from '../../types/api';
import { useNavigate } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';

interface Props {
  data: DepartmentPerformanceExtended[];
}

const DepartmentSummaryTable: React.FC<Props> = ({ data }) => {
  const navigate = useNavigate();

  const handleRowClick = (departmentId: number) => {
    navigate(`/batches-sections?department=${departmentId}`);
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="px-6 py-5 border-b border-slate-200">
        <h3 className="text-base font-semibold text-slate-800">Department Summary</h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[800px]">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <th className="px-6 py-3">Department</th>
              <th className="px-6 py-3 text-right">Students</th>
              <th className="px-6 py-3 text-right">Academic %</th>
              <th className="px-6 py-3 text-right">Attendance %</th>
              <th className="px-6 py-3 text-right">Risk Count</th>
              <th className="px-6 py-3 text-center">Status</th>
              <th className="px-6 py-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {data.map((dept) => {
              // Calculate status
              let statusText = 'Healthy';
              let statusStyle = 'bg-emerald-100 text-emerald-700';
              
              if (dept.average_assessment_percentage < 60 || dept.average_attendance_percentage < 70) {
                statusText = 'Attention Required';
                statusStyle = 'bg-rose-100 text-rose-700';
              } else if (dept.average_assessment_percentage < 75 || dept.average_attendance_percentage < 85) {
                statusText = 'Monitor';
                statusStyle = 'bg-amber-100 text-amber-700';
              }

              return (
                <tr 
                  key={dept.department_id} 
                  className="hover:bg-slate-50 transition-colors cursor-pointer group"
                  onClick={() => handleRowClick(dept.department_id)}
                >
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-slate-900">{dept.department_name}</div>
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700">
                    {dept.total_students.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700 font-medium">
                    {dept.average_assessment_percentage.toFixed(2)}%
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700 font-medium">
                    {dept.average_attendance_percentage.toFixed(2)}%
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-slate-700">
                    {dept.students_at_risk > 0 ? (
                      <span className="text-rose-600 font-medium">{dept.students_at_risk.toLocaleString()}</span>
                    ) : (
                      <span className="text-slate-500">0</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusStyle}`}>
                      {statusText}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-blue-600 transition-colors inline-block" />
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

export default DepartmentSummaryTable;
