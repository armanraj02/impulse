from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Optional
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api")

@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    total_students = db.query(func.count(models.StudentPerformanceSummary.student_id)).scalar() or 0
    students_at_risk = db.query(func.count(models.RiskSummary.student_id)).filter(models.RiskSummary.risk_category == 'High Risk').scalar() or 0
    
    avg_academic = db.query(func.avg(models.StudentPerformanceSummary.average_assessment_percentage)).scalar() or 0.0
    avg_attendance = db.query(func.avg(models.StudentPerformanceSummary.average_attendance_percentage)).scalar() or 0.0
    
    feedback = db.query(models.FeedbackSummary).first()
    avg_feedback = feedback.average_rating if feedback else 0.0
    
    total_insights = db.query(func.count(models.InsightSummary.insight_id)).scalar() or 0
    total_departments = db.query(func.count(models.DepartmentPerformanceSummary.department_id)).scalar() or 0
    total_courses = db.query(func.count(models.CoursePerformanceSummary.course_id)).scalar() or 0
    
    return {
        "total_students": total_students,
        "students_at_risk": students_at_risk,
        "average_academic_performance": round(avg_academic, 2),
        "average_attendance": round(avg_attendance, 2),
        "average_feedback_rating": round(avg_feedback, 2),
        "total_insights": total_insights,
        "total_departments": total_departments,
        "total_courses": total_courses
    }

@router.get("/departments", response_model=List[schemas.DepartmentPerformanceSummarySchema])
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.DepartmentPerformanceSummary).all()

@router.get("/departments/performance", response_model=List[schemas.DepartmentPerformanceExtendedSchema])
def get_departments_performance(db: Session = Depends(get_db)):
    departments = db.query(models.DepartmentPerformanceSummary).all()
    results = []
    
    for dept in departments:
        # Get attendance by aggregating students in this branch
        avg_att = db.query(func.avg(models.StudentPerformanceSummary.average_attendance_percentage))\
                    .filter(models.StudentPerformanceSummary.branch_id == dept.department_id).scalar() or 0.0
                    
        # Get risk count
        high_risk_count = db.query(func.count(models.RiskSummary.student_id))\
                       .filter(models.RiskSummary.branch_name == dept.department_name)\
                       .filter(models.RiskSummary.risk_category == 'High Risk').scalar() or 0
                       
        results.append({
            "department_id": dept.department_id,
            "department_name": dept.department_name,
            "total_students": dept.total_students,
            "average_assessment_percentage": round(dept.average_assessment_percentage or 0, 2),
            "average_attendance_percentage": round(avg_att, 2),
            "students_at_risk": high_risk_count,
            "average_feedback_rating": None # Defaulting to None unless joined with module feedback
        })
        
    return results

@router.get("/departments/risk", response_model=List[schemas.DepartmentRiskDistributionSchema])
def get_departments_risk_distribution(db: Session = Depends(get_db)):
    distribution = db.query(
        models.RiskSummary.branch_name,
        models.RiskSummary.risk_category,
        func.count(models.RiskSummary.student_id).label("count")
    ).group_by(
        models.RiskSummary.branch_name,
        models.RiskSummary.risk_category
    ).all()
    
    result = []
    for row in distribution:
        result.append({
            "department_name": row[0] or "Unknown",
            "category": row[1] or "Unknown",
            "count": row[2]
        })
        
    return result

@router.get("/departments/{department_id}", response_model=schemas.DepartmentPerformanceSummarySchema)
def get_department(department_id: int, db: Session = Depends(get_db)):
    dept = db.query(models.DepartmentPerformanceSummary).filter(models.DepartmentPerformanceSummary.department_id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.get("/courses", response_model=schemas.PaginatedResponse)
def get_courses(
    department_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.CoursePerformanceSummary)
    if department_id is not None:
        query = query.filter(models.CoursePerformanceSummary.department_id == department_id)
        
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # We must construct a dict matching PaginatedResponse since items can be ORM models
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.CoursePerformanceSummarySchema.model_validate(i) for i in items]
    }

@router.get("/students", response_model=schemas.PaginatedResponse)
def get_students(
    search: Optional[str] = None,
    branch_name: Optional[str] = None,
    batch_name: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.StudentPerformanceSummary)
    
    if search:
        query = query.filter(models.StudentPerformanceSummary.student_name.ilike(f"%{search}%") | models.StudentPerformanceSummary.usn.ilike(f"%{search}%"))
    if branch_name:
        query = query.filter(models.StudentPerformanceSummary.branch_name == branch_name)
    if batch_name:
        query = query.filter(models.StudentPerformanceSummary.batch_name == batch_name)
        
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.StudentPerformanceSummarySchema.model_validate(i) for i in items]
    }

@router.get("/students/risk", response_model=schemas.PaginatedResponse)
def get_students_risk(
    department_id: Optional[int] = None,
    batch_id: Optional[int] = None,
    section_id: Optional[int] = None,
    risk_category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.StudentPerformanceSummary, models.RiskSummary)\
              .outerjoin(models.RiskSummary, models.StudentPerformanceSummary.student_id == models.RiskSummary.student_id)
    
    if department_id:
        query = query.filter(models.StudentPerformanceSummary.branch_id == department_id)
    if batch_id:
        query = query.filter(models.StudentPerformanceSummary.batch_id == batch_id)
    if section_id:
        query = query.filter(
            text("EXISTS (SELECT 1 FROM enrollment_details e WHERE e.student_id = student_performance_summary.student_id AND e.section_id = :section_id)")
            .params(section_id=section_id)
        )
    if search:
        query = query.filter(
            models.StudentPerformanceSummary.student_name.ilike(f"%{search}%") | 
            models.StudentPerformanceSummary.usn.ilike(f"%{search}%")
        )
        
    if risk_category:
        if risk_category == 'No Risk':
            query = query.filter(models.RiskSummary.risk_category == None)
        else:
            query = query.filter(models.RiskSummary.risk_category == risk_category)
            
    total = query.count()
    query = query.order_by(models.StudentPerformanceSummary.usn.asc())
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for student, risk in items:
        cat = risk.risk_category if risk else 'No Risk'
        reason = risk.risk_category if risk else 'No active risk identified'
        
        result.append({
            "student_id": student.student_id,
            "usn": student.usn,
            "student_name": student.student_name,
            "department_id": student.branch_id,
            "department_name": student.branch_name,
            "batch_id": student.batch_id,
            "batch_name": student.batch_name,
            "academic_percentage": round(student.average_assessment_percentage or 0.0, 2),
            "attendance_percentage": round(student.average_attendance_percentage or 0.0, 2),
            "risk_category": cat,
            "risk_reason": reason
        })
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.StudentRiskExtendedSchema(**i) for i in result]
    }

@router.get("/students/risk/distribution", response_model=List[schemas.RiskDistributionSchema])
def get_students_risk_distribution(db: Session = Depends(get_db)):
    total_students = db.query(func.count(models.StudentPerformanceSummary.student_id)).scalar() or 1
    
    distribution = db.query(
        models.RiskSummary.risk_category,
        func.count(models.RiskSummary.student_id).label("count")
    ).group_by(models.RiskSummary.risk_category).all()
    
    result = []
    at_risk_total = 0
    
    for row in distribution:
        category = row[0]
        if not category:
            continue
        count = row[1]
        at_risk_total += count
        percentage = round((count / total_students) * 100, 2)
        result.append({
            "category": category,
            "count": count,
            "percentage": percentage
        })
        
    no_risk_count = total_students - at_risk_total
    result.append({
        "category": "No Risk",
        "count": no_risk_count,
        "percentage": round((no_risk_count / total_students) * 100, 2)
    })
        
    return result

@router.get("/feedback", response_model=schemas.FeedbackSummarySchema)
def get_feedback_overview(db: Session = Depends(get_db)):
    feedback = db.query(models.FeedbackSummary).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback summary not found")
    return feedback

from sqlalchemy import or_

@router.get("/insights/distribution", response_model=List[schemas.InsightDistributionSchema])
def get_insights_distribution(db: Session = Depends(get_db)):
    query = db.query(
        models.InsightSummary.insight_type,
        models.InsightSummary.entity_type,
        func.count(models.InsightSummary.insight_id).label("count")
    ).group_by(
        models.InsightSummary.insight_type,
        models.InsightSummary.entity_type
    ).all()
    return query

@router.get("/insights", response_model=schemas.PaginatedResponse)
def get_insights(
    insight_type: Optional[str] = None,
    entity_type: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.InsightSummary)
    
    if insight_type:
        query = query.filter(models.InsightSummary.insight_type == insight_type)
    if entity_type:
        query = query.filter(models.InsightSummary.entity_type == entity_type)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.InsightSummary.entity_name.ilike(search_term),
                models.InsightSummary.insight.ilike(search_term),
                models.InsightSummary.recommendation.ilike(search_term)
            )
        )
        
    # Sort by most recent
    query = query.order_by(models.InsightSummary.generated_at.desc())
        
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.InsightSummarySchema.model_validate(i) for i in items]
    }



@router.get("/batches/performance", response_model=List[schemas.BatchPerformanceExtendedSchema])
def get_batches_performance(
    department_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        models.StudentPerformanceSummary.batch_id,
        models.StudentPerformanceSummary.batch_name,
        func.count(models.StudentPerformanceSummary.student_id).label("total_students"),
        func.avg(models.StudentPerformanceSummary.average_assessment_percentage).label("avg_academic"),
        func.avg(models.StudentPerformanceSummary.average_attendance_percentage).label("avg_attendance")
    )
    
    if department_id:
        query = query.filter(models.StudentPerformanceSummary.branch_id == department_id)
        
    query = query.group_by(
        models.StudentPerformanceSummary.batch_id,
        models.StudentPerformanceSummary.batch_name
    ).all()
    
    results = []
    for row in query:
        results.append({
            "batch_id": row[0],
            "batch_name": row[1] or "Unknown",
            "department_id": department_id,
            "total_students": row[2] or 0,
            "average_assessment_percentage": round(row[3] or 0.0, 2),
            "average_attendance_percentage": round(row[4] or 0.0, 2)
        })
        
    return results

@router.get("/sections/performance", response_model=List[schemas.SectionPerformanceExtendedSchema])
def get_sections_performance(
    department_id: Optional[int] = None,
    batch_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.SectionPerformanceSummary)
    
    if department_id:
        query = query.filter(models.SectionPerformanceSummary.branch_id == department_id)
    if batch_id:
        query = query.filter(models.SectionPerformanceSummary.batch_id == batch_id)
        
    sections = query.all()
    
    results = []
    for sec in sections:
        results.append({
            "section_id": sec.section_id,
            "section_name": sec.section_name or "Unknown",
            "batch_id": sec.batch_id or 0,
            "batch_name": None, # Could join if needed
            "department_id": sec.branch_id,
            "total_students": sec.enrolled_students or 0,
            "average_assessment_percentage": round(sec.average_assessment_percentage or 0.0, 2),
            "average_attendance_percentage": round(sec.average_attendance_percentage or 0.0, 2)
        })
        
    return results

@router.get("/courses/performance", response_model=schemas.PaginatedResponse)
def get_courses_performance(
    department_id: Optional[int] = None,
    course_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.CoursePerformanceSummary)
    if department_id is not None:
        query = query.filter(models.CoursePerformanceSummary.department_id == department_id)
    if course_id is not None:
        query = query.filter(models.CoursePerformanceSummary.course_id == course_id)
        
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.CoursePerformanceSummarySchema.model_validate(i) for i in items]
    }

@router.get("/feedback/module", response_model=schemas.PaginatedResponse)
def get_feedback_module(
    course_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.ModuleFeedbackSummary)
    if course_id is not None:
        query = query.filter(models.ModuleFeedbackSummary.course_id == course_id)
        
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.ModuleFeedbackSummarySchema.model_validate(i) for i in items]
    }

@router.get("/feedback/instructor", response_model=schemas.PaginatedResponse)
def get_feedback_instructor(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.InstructorFeedbackSummary)
        
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.InstructorFeedbackSummarySchema.model_validate(i) for i in items]
    }

@router.get("/attendance/overview", response_model=schemas.AttendanceOverviewSchema)
def get_attendance_overview(db: Session = Depends(get_db)):
    total_students = db.query(func.count(models.StudentPerformanceSummary.student_id)).scalar() or 0
    students_below_75 = db.query(func.count(models.StudentPerformanceSummary.student_id))\
        .filter(models.StudentPerformanceSummary.average_attendance_percentage < 75).scalar() or 0
    avg_attendance = db.query(func.avg(models.StudentPerformanceSummary.average_attendance_percentage)).scalar() or 0.0
    total_courses_analyzed = db.query(func.count(models.CoursePerformanceSummary.course_id)).scalar() or 0

    return {
        "total_students": total_students,
        "students_below_75": students_below_75,
        "average_attendance": round(avg_attendance, 2),
        "total_courses_analyzed": total_courses_analyzed
    }

@router.get("/academic/overview", response_model=schemas.AcademicOverviewSchema)
def get_academic_overview(db: Session = Depends(get_db)):
    total_students = db.query(func.count(models.StudentPerformanceSummary.student_id)).scalar() or 0
    students_below_50 = db.query(func.count(models.StudentPerformanceSummary.student_id))\
        .filter(models.StudentPerformanceSummary.average_assessment_percentage < 50).scalar() or 0
    avg_academic = db.query(func.avg(models.StudentPerformanceSummary.average_assessment_percentage)).scalar() or 0.0
    total_courses_analyzed = db.query(func.count(models.CoursePerformanceSummary.course_id)).scalar() or 0

    return {
        "total_students": total_students,
        "students_below_50": students_below_50,
        "average_academic": round(avg_academic, 2),
        "total_courses_analyzed": total_courses_analyzed
    }

@router.get("/attendance/students", response_model=schemas.PaginatedResponse)
def get_attendance_students(
    department_id: Optional[int] = None,
    batch_id: Optional[int] = None,
    section_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.StudentPerformanceSummary)
    
    if department_id:
        query = query.filter(models.StudentPerformanceSummary.branch_id == department_id)
    if batch_id:
        query = query.filter(models.StudentPerformanceSummary.batch_id == batch_id)
    if section_id:
        query = query.filter(
            text("EXISTS (SELECT 1 FROM enrollment_details e WHERE e.student_id = student_performance_summary.student_id AND e.section_id = :section_id)")
            .params(section_id=section_id)
        )
        
    total = query.count()
    items = query.order_by(models.StudentPerformanceSummary.usn.asc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.StudentPerformanceSummarySchema.model_validate(i) for i in items]
    }

@router.get("/academic/students", response_model=schemas.PaginatedResponse)
def get_academic_students(
    department_id: Optional[int] = None,
    batch_id: Optional[int] = None,
    section_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.StudentPerformanceSummary)
    
    if department_id:
        query = query.filter(models.StudentPerformanceSummary.branch_id == department_id)
    if batch_id:
        query = query.filter(models.StudentPerformanceSummary.batch_id == batch_id)
    if section_id:
        query = query.filter(
            text("EXISTS (SELECT 1 FROM enrollment_details e WHERE e.student_id = student_performance_summary.student_id AND e.section_id = :section_id)")
            .params(section_id=section_id)
        )
        
    total = query.count()
    items = query.order_by(models.StudentPerformanceSummary.usn.asc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [schemas.StudentPerformanceSummarySchema.model_validate(i) for i in items]
    }
