from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class DepartmentPerformanceSummarySchema(BaseModel):
    department_id: Optional[int]
    department_code: Optional[str]
    department_name: Optional[str]
    hod_name: Optional[str]
    hod_email: Optional[str]
    total_students: Optional[int]
    average_assessment_percentage: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class StudentPerformanceSummarySchema(BaseModel):
    student_id: Optional[int]
    usn: Optional[str]
    student_name: Optional[str]
    branch_id: Optional[int]
    branch_name: Optional[str]
    batch_id: Optional[int]
    batch_name: Optional[str]
    academic_year: Optional[str]
    semester: Optional[int]
    assessment_count: Optional[int]
    average_assessment_percentage: Optional[float]
    courses_attended: Optional[int]
    average_attendance_percentage: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class CoursePerformanceSummarySchema(BaseModel):
    course_id: Optional[int]
    course_code: Optional[str]
    course_name: Optional[str]
    department_id: Optional[int]
    semester: Optional[int]
    credits: Optional[int]
    assessment_score_count: Optional[int]
    students_assessed: Optional[int]
    average_assessment_percentage: Optional[float]
    students_with_attendance: Optional[int]
    average_attendance_percentage: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class SectionPerformanceSummarySchema(BaseModel):
    section_id: Optional[int]
    section_name: Optional[str]
    course_id: Optional[int]
    branch_id: Optional[int]
    batch_id: Optional[int]
    academic_year: Optional[str]
    enrolled_students: Optional[int]
    students_assessed: Optional[int]
    average_assessment_percentage: Optional[float]
    students_with_attendance: Optional[int]
    average_attendance_percentage: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class BatchPerformanceSummarySchema(BaseModel):
    batch_id: Optional[int]
    batch_name: Optional[str]
    academic_year: Optional[str]
    semester: Optional[int]
    total_students: Optional[int]
    students_assessed: Optional[int]
    average_assessment_percentage: Optional[float]
    average_attendance_percentage: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class FeedbackSummarySchema(BaseModel):
    total_rating_responses: Optional[int]
    average_rating: Optional[float]
    minimum_rating: Optional[float]
    maximum_rating: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class ModuleFeedbackSummarySchema(BaseModel):
    module_id: Optional[int]
    course_id: Optional[int]
    module_name: Optional[str]
    module_order: Optional[int]
    rating_responses: Optional[int]
    average_rating: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class InstructorFeedbackSummarySchema(BaseModel):
    instructor_id: Optional[int]
    instructor_name: Optional[str]
    email: Optional[str]
    rating_responses: Optional[int]
    average_rating: Optional[float]
    minimum_rating: Optional[float]
    maximum_rating: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class RiskSummarySchema(BaseModel):
    student_id: Optional[int]
    usn: Optional[str]
    student_name: Optional[str]
    branch_name: Optional[str]
    batch_name: Optional[str]
    average_assessment_percentage: Optional[float]
    average_attendance_percentage: Optional[float]
    risk_category: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class RiskDistributionSchema(BaseModel):
    category: str
    count: int
    percentage: float

class InsightSummarySchema(BaseModel):
    insight_id: int
    insight_type: Optional[str]
    entity_type: Optional[str]
    entity_id: Optional[str]
    entity_name: Optional[str]
    academic_percentage: Optional[float]
    attendance_percentage: Optional[float]
    feedback_average: Optional[float]
    response_count: Optional[int]
    rule_name: Optional[str]
    threshold_used: Optional[str]
    insight: Optional[str]
    recommendation: Optional[str]
    generated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class InsightDistributionSchema(BaseModel):
    insight_type: str
    entity_type: str
    count: int
    model_config = ConfigDict(from_attributes=True)

# Pagination Schemas
class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Any]

class DepartmentPerformanceExtendedSchema(BaseModel):
    department_id: int
    department_name: str
    total_students: int
    average_assessment_percentage: float
    average_attendance_percentage: float
    students_at_risk: int
    average_feedback_rating: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class BatchPerformanceExtendedSchema(BaseModel):
    batch_id: int
    batch_name: str
    department_id: Optional[int] = None
    total_students: int
    average_assessment_percentage: float
    average_attendance_percentage: float
    model_config = ConfigDict(from_attributes=True)

class SectionPerformanceExtendedSchema(BaseModel):
    section_id: int
    section_name: str
    batch_id: int
    batch_name: Optional[str] = None
    department_id: Optional[int] = None
    total_students: int
    average_assessment_percentage: float
    average_attendance_percentage: float
    model_config = ConfigDict(from_attributes=True)

class DepartmentRiskDistributionSchema(BaseModel):
    department_name: str
    category: str
    count: int
    model_config = ConfigDict(from_attributes=True)

class StudentRiskExtendedSchema(BaseModel):
    student_id: int
    usn: str
    student_name: str
    department_id: Optional[int] = None
    department_name: str
    batch_id: Optional[int] = None
    batch_name: str
    academic_percentage: Optional[float] = None
    attendance_percentage: Optional[float] = None
    risk_category: str
    risk_reason: str
    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel
from typing import Optional

class AttendanceOverviewSchema(BaseModel):
    total_students: int
    students_below_75: int
    average_attendance: float
    total_courses_analyzed: int

class AcademicOverviewSchema(BaseModel):
    total_students: int
    students_below_50: int
    average_academic: float
    total_courses_analyzed: int
