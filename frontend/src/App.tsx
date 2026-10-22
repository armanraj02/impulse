import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import ExecutiveOverview from './pages/ExecutiveOverview';
import DepartmentPerformance from './pages/DepartmentPerformance';
import BatchSectionPerformance from './pages/BatchSectionPerformance';
import CoursesFeedback from './pages/CoursesFeedback';
import { StudentRisk } from './pages/StudentRisk';
import AttendanceIntelligence from './pages/AttendanceIntelligence';
import AcademicIntelligence from './pages/AcademicIntelligence';
import Insights from './pages/Insights';
import Reports from './pages/Reports';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<ExecutiveOverview />} />
          <Route path="departments" element={<DepartmentPerformance />} />
          <Route path="batches-sections" element={<BatchSectionPerformance />} />
          <Route path="students/risk" element={<StudentRisk />} />
          <Route path="courses-feedback" element={<CoursesFeedback />} />
          <Route path="attendance" element={<AttendanceIntelligence />} />
          <Route path="academic" element={<AcademicIntelligence />} />
          <Route path="insights" element={<Insights />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
