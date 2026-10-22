import React from 'react';
import type { StudentRiskExtended } from '../../types/api';

interface StudentRiskTableProps {
  students: StudentRiskExtended[];
}

export const StudentRiskTable: React.FC<StudentRiskTableProps> = ({ students }) => {
  const getBadgeStyle = (category: string) => {
    switch (category) {
      case 'High Risk':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'Attendance Risk':
      case 'Academic Risk':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'No Risk':
      default:
        return 'bg-green-100 text-green-800 border-green-200';
    }
  };

  const formatCategoryText = (category: string) => {
    return category.toUpperCase();
  };

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Batch</th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acad. %</th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Att. %</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Risk Category</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Risk Reason</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {students.map((student) => (
            <tr key={`student-${student.student_id}`} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex flex-col">
                  <span className="text-sm font-medium text-gray-900">{student.student_name}</span>
                  <span className="text-sm text-gray-500">{student.usn}</span>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {student.department_name}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {student.batch_name}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium">
                {student.academic_percentage !== null ? `${student.academic_percentage}%` : 'N/A'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium">
                {student.attendance_percentage !== null ? `${student.attendance_percentage}%` : 'N/A'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getBadgeStyle(student.risk_category)}`}>
                  {formatCategoryText(student.risk_category)}
                </span>
              </td>
              <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate" title={student.risk_reason}>
                {student.risk_reason}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
