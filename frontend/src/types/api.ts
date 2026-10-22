export interface OverviewData {
  total_students: number;
  students_at_risk: number;
  average_academic_performance: number;
  average_attendance: number;
  average_feedback_rating: number;
  total_insights: number;
  total_departments: number;
  total_courses: number;
}

export interface AttendanceOverview {
  total_students: number;
  students_below_75: number;
  average_attendance: number;
  total_courses_analyzed: number;
}

export interface AcademicOverview {
  total_students: number;
  students_below_50: number;
  average_academic: number;
  total_courses_analyzed: number;
}

export interface Department {
  department_id: number;
  department_code: string;
  department_name: string;
  hod_name: string;
  hod_email: string;
  total_students: number;
  average_assessment_percentage: number;
}

export interface DepartmentPerformanceExtended {
  department_id: number;
  department_name: string;
  total_students: number;
  average_assessment_percentage: number;
  average_attendance_percentage: number;
  students_at_risk: number;
  average_feedback_rating?: number;
}

export interface BatchPerformanceExtended {
  batch_id: number;
  batch_name: string;
  department_id?: number;
  total_students: number;
  average_assessment_percentage: number;
  average_attendance_percentage: number;
}

export interface SectionPerformanceExtended {
  section_id: number;
  section_name: string;
  batch_id: number;
  batch_name?: string;
  department_id?: number;
  total_students: number;
  average_assessment_percentage: number;
  average_attendance_percentage: number;
}

export interface Course {
  course_id: number;
  course_code: string;
  course_name: string;
  department_id: number;
  semester: number;
  credits: number;
  assessment_score_count: number;
  students_assessed: number;
  average_assessment_percentage: number;
  students_with_attendance: number;
  average_attendance_percentage: number;
}

export interface Student {
  student_id: number;
  usn: string;
  student_name: string;
  branch_id: number;
  branch_name: string;
  batch_id: number;
  batch_name: string;
  academic_year: string;
  semester: number;
  assessment_count: number;
  average_assessment_percentage: number;
  courses_attended: number;
  average_attendance_percentage: number;
}

export interface StudentRisk {
  student_id: number;
  usn: string;
  student_name: string;
  branch_name: string;
  batch_name: string;
  average_assessment_percentage: number;
  average_attendance_percentage: number;
  risk_category: string;
}

export interface RiskDistribution {
  category: string;
  count: number;
  percentage: number;
}

export interface StudentRiskExtended {
  student_id: number;
  usn: string;
  student_name: string;
  department_id?: number;
  department_name: string;
  batch_id?: number;
  batch_name: string;
  academic_percentage?: number;
  attendance_percentage?: number;
  risk_category: string;
  risk_reason: string;
}

export interface DepartmentRiskDistribution {
  department_name: string;
  category: string;
  count: number;
}

export interface Insight {
  insight_id: number;
  insight_type: string;
  entity_type: string;
  entity_id: string;
  entity_name: string;
  academic_percentage: number;
  attendance_percentage: number;
  feedback_average: number;
  response_count: number;
  rule_name: string;
  threshold_used: string;
  insight: string;
  recommendation: string;
  generated_at: string;
}

export interface InsightDistributionItem {
  insight_type: string;
  entity_type: string;
  count: number;
}

export interface PaginatedResponse<T> {
  total: number;
  page: number;
  page_size: number;
  items: T[];
}

export interface FeedbackSummary {
  total_rating_responses: number;
  average_rating: number;
  minimum_rating: number;
  maximum_rating: number;
}

export interface ModuleFeedback {
  module_id: number;
  course_id: number;
  module_name: string;
  module_order: number;
  rating_responses: number;
  average_rating: number;
}

export interface InstructorFeedback {
  instructor_id: number;
  instructor_name: string;
  email: string;
  rating_responses: number;
  average_rating: number;
  minimum_rating: number;
  maximum_rating: number;
}
