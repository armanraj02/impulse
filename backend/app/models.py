from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from app.database import Base

class DepartmentPerformanceSummary(Base):
    __tablename__ = "department_performance_summary"
    
    # Tables from views or summary tables might not have primary keys in DB, 
    # but SQLAlchemy needs one. We'll use department_id.
    department_id = Column(Integer, primary_key=True)
    department_code = Column(String)
    department_name = Column(String)
    hod_name = Column(String)
    hod_email = Column(String)
    total_students = Column(Integer)
    average_assessment_percentage = Column(Float)

class StudentPerformanceSummary(Base):
    __tablename__ = "student_performance_summary"
    
    student_id = Column(Integer, primary_key=True)
    usn = Column(String)
    student_name = Column(String)
    branch_id = Column(Integer)
    branch_name = Column(String)
    batch_id = Column(Integer)
    batch_name = Column(String)
    academic_year = Column(String)
    semester = Column(Integer)
    assessment_count = Column(Integer)
    average_assessment_percentage = Column(Float)
    courses_attended = Column(Integer)
    average_attendance_percentage = Column(Float)

class CoursePerformanceSummary(Base):
    __tablename__ = "course_performance_summary"
    
    course_id = Column(Integer, primary_key=True)
    course_code = Column(String)
    course_name = Column(String)
    department_id = Column(Integer)
    semester = Column(Integer)
    credits = Column(Integer)
    assessment_score_count = Column(Integer)
    students_assessed = Column(Integer)
    average_assessment_percentage = Column(Float)
    students_with_attendance = Column(Integer)
    average_attendance_percentage = Column(Float)

class SectionPerformanceSummary(Base):
    __tablename__ = "section_performance_summary"
    
    section_id = Column(Integer, primary_key=True)
    section_name = Column(String)
    course_id = Column(Integer)
    branch_id = Column(Integer)
    batch_id = Column(Integer)
    academic_year = Column(String)
    enrolled_students = Column(Integer)
    students_assessed = Column(Integer)
    average_assessment_percentage = Column(Float)
    students_with_attendance = Column(Integer)
    average_attendance_percentage = Column(Float)

class BatchPerformanceSummary(Base):
    __tablename__ = "batch_performance_summary"
    
    batch_id = Column(Integer, primary_key=True)
    batch_name = Column(String)
    academic_year = Column(String)
    semester = Column(Integer)
    total_students = Column(Integer)
    students_assessed = Column(Integer)
    average_assessment_percentage = Column(Float)
    average_attendance_percentage = Column(Float)

class FeedbackSummary(Base):
    __tablename__ = "feedback_summary"
    
    total_rating_responses = Column(Integer, primary_key=True) # Fake PK for sqlalchemy
    average_rating = Column(Float)
    minimum_rating = Column(Float)
    maximum_rating = Column(Float)

class ModuleFeedbackSummary(Base):
    __tablename__ = "module_feedback_summary"
    
    module_id = Column(Integer, primary_key=True)
    course_id = Column(Integer)
    module_name = Column(String)
    module_order = Column(Integer)
    rating_responses = Column(Integer)
    average_rating = Column(Float)

class InstructorFeedbackSummary(Base):
    __tablename__ = "instructor_feedback_summary"
    
    instructor_id = Column(Integer, primary_key=True)
    instructor_name = Column(String)
    email = Column(String)
    rating_responses = Column(Integer)
    average_rating = Column(Float)
    minimum_rating = Column(Float)
    maximum_rating = Column(Float)

class RiskSummary(Base):
    __tablename__ = "risk_summary"
    
    student_id = Column(Integer, primary_key=True)
    usn = Column(String)
    student_name = Column(String)
    branch_name = Column(String)
    batch_name = Column(String)
    average_assessment_percentage = Column(Float)
    average_attendance_percentage = Column(Float)
    risk_category = Column(String)

class InsightSummary(Base):
    __tablename__ = "insight_summary"
    
    insight_id = Column(Integer, primary_key=True)
    insight_type = Column(String)
    entity_type = Column(String)
    entity_id = Column(String)
    entity_name = Column(String)
    academic_percentage = Column(Float)
    attendance_percentage = Column(Float)
    feedback_average = Column(Float)
    response_count = Column(Integer)
    rule_name = Column(String)
    threshold_used = Column(String)
    insight = Column(String)
    recommendation = Column(String)
    generated_at = Column(DateTime)
