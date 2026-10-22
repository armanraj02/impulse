import axios from 'axios';
import type {
  OverviewData,
  Department,
  DepartmentPerformanceExtended,
  BatchPerformanceExtended,
  SectionPerformanceExtended,
  Course,
  Student,
  StudentRiskExtended,
  RiskDistribution,
  DepartmentRiskDistribution,
  Insight,
  InsightDistributionItem,
  PaginatedResponse,
  FeedbackSummary,
  ModuleFeedback,
  InstructorFeedback,
  AttendanceOverview,
  AcademicOverview,
} from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const healthUrl = API_BASE_URL.startsWith('http')
    ? `${API_BASE_URL.replace(/\/api\/?$/, '')}/health`
    : '/health';
  const response = await axios.get(healthUrl, { timeout: 5000 });
  return response.data;
};

export const getOverview = async (): Promise<OverviewData> => {
  const response = await api.get('/overview');
  return response.data;
};

export const getDepartments = async (): Promise<Department[]> => {
  const response = await api.get('/departments');
  return response.data;
};

export const getDepartment = async (id: number): Promise<Department> => {
  const response = await api.get(`/departments/${id}`);
  return response.data;
};

export const getDepartmentsPerformance = async (): Promise<DepartmentPerformanceExtended[]> => {
  const response = await api.get('/departments/performance');
  return response.data;
};

export const getBatchesPerformance = async (params?: any): Promise<BatchPerformanceExtended[]> => {
  const response = await api.get('/batches/performance', { params });
  return response.data;
};

export const getSectionsPerformance = async (params?: any): Promise<SectionPerformanceExtended[]> => {
  const response = await api.get('/sections/performance', { params });
  return response.data;
};

export const getCourses = async (params?: any): Promise<PaginatedResponse<Course>> => {
  const response = await api.get('/courses', { params });
  return response.data;
};

export const getStudents = async (params?: any): Promise<PaginatedResponse<Student>> => {
  const response = await api.get('/students', { params });
  return response.data;
};

export const getStudentsRisk = async (
  page = 1,
  pageSize = 10,
  departmentId?: number,
  batchId?: number,
  sectionId?: number,
  riskCategory?: string,
  search?: string
) => {
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  });
  if (departmentId) params.append('department_id', departmentId.toString());
  if (batchId) params.append('batch_id', batchId.toString());
  if (sectionId) params.append('section_id', sectionId.toString());
  if (riskCategory && riskCategory !== 'All') params.append('risk_category', riskCategory);
  if (search) params.append('search', search);

  const response = await api.get<PaginatedResponse<StudentRiskExtended>>(`/students/risk?${params.toString()}`);
  return response.data;
};

export const getStudentRiskDistribution = async (): Promise<RiskDistribution[]> => {
  const response = await api.get('/students/risk/distribution');
  return response.data;
};

export const getDepartmentRiskDistribution = async (): Promise<DepartmentRiskDistribution[]> => {
  const response = await api.get('/departments/risk');
  return response.data;
};

export const getFeedback = async (params?: any): Promise<FeedbackSummary> => {
  const response = await api.get('/feedback', { params });
  return response.data;
};

export const getModuleFeedback = async (params?: any): Promise<PaginatedResponse<ModuleFeedback>> => {
  const response = await api.get('/feedback/module', { params });
  return response.data;
};

export const getInstructorFeedback = async (params?: any): Promise<PaginatedResponse<InstructorFeedback>> => {
  const response = await api.get('/feedback/instructor', { params });
  return response.data;
};

export const getCoursesPerformance = async (params?: any): Promise<PaginatedResponse<Course>> => {
  const response = await api.get('/courses/performance', { params });
  return response.data;
};

export const getInsights = async (params?: any): Promise<PaginatedResponse<Insight>> => {
  const response = await api.get('/insights', { params });
  return response.data;
};

export const getInsightsDistribution = async (): Promise<InsightDistributionItem[]> => {
  const response = await api.get('/insights/distribution');
  return response.data;
};

export const getAttendanceOverview = async (): Promise<AttendanceOverview> => {
  const response = await api.get('/attendance/overview');
  return response.data;
};

export const getAcademicOverview = async (): Promise<AcademicOverview> => {
  const response = await api.get('/academic/overview');
  return response.data;
};

export const getAttendanceStudents = async (params?: any): Promise<PaginatedResponse<Student>> => {
  const response = await api.get('/attendance/students', { params });
  return response.data;
};

export const getAcademicStudents = async (params?: any): Promise<PaginatedResponse<Student>> => {
  const response = await api.get('/academic/students', { params });
  return response.data;
};

export default api;
