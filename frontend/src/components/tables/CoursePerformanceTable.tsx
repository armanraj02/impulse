import React from 'react';
import type { Course } from '../../types/api';

interface Props {
  data: Course[];
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
}

const CoursePerformanceTable: React.FC<Props> = ({ 
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
        <h3 className="font-semibold text-slate-800">Course Performance</h3>
      </div>
      
      <div className="overflow-x-auto flex-1">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
            <tr>
              <th className="px-4 py-3">Course</th>
              <th className="px-4 py-3">Semester</th>
              <th className="px-4 py-3">Credits</th>
              <th className="px-4 py-3">Students Assessed</th>
              <th className="px-4 py-3">Academic %</th>
              <th className="px-4 py-3">Attendance %</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {data.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-slate-500">
                  No courses found for the selected criteria.
                </td>
              </tr>
            ) : (
              data.map((row) => (
                <tr key={row.course_id} className="hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <div className="font-medium text-slate-900">{row.course_name}</div>
                    <div className="text-slate-500 text-xs">{row.course_code}</div>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{row.semester}</td>
                  <td className="px-4 py-3 text-slate-600">{row.credits}</td>
                  <td className="px-4 py-3 text-slate-600">{row.students_assessed}</td>
                  <td className="px-4 py-3 text-slate-600 font-medium">
                    {row.average_assessment_percentage.toFixed(2)}%
                  </td>
                  <td className="px-4 py-3 text-slate-600 font-medium">
                    {row.average_attendance_percentage.toFixed(2)}%
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="p-4 border-t border-slate-200 flex items-center justify-between bg-slate-50">
        <div className="text-sm text-slate-600">
          Showing {Math.min((page - 1) * pageSize + 1, total)} to {Math.min(page * pageSize, total)} of {total} courses
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

export default CoursePerformanceTable;
