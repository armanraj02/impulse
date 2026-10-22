from collections import defaultdict


def build_weekly_summary_v2(attendance_records, academic_records, feedback_records):
    """
    Build department-level, course-level, batch-level, section-level, and 
    facilitator-level weekly summaries from independent dataset records.
    """

    department = {
        "student_count": 0,
        "course_count": 0,
        "total_classes": 0,
        "attended_classes": 0,
        "average_attendance_percentage": None,
        "average_academic_percentage": None,
        "feedback_response_count": 0,
        "average_feedback_rating": None,
        "attendance_risk_records": 0,
        "students_with_attendance_risk": 0,
    }

    students = set()
    courses = set()
    attendance_percentages = []
    academic_percentages = []
    attendance_risk_students = set()

    course_data = defaultdict(
        lambda: {
            "course_id": None,
            "course_code": None,
            "course_name": None,
            "students": set(),
            "total_classes": 0,
            "attended_classes": 0,
            "attendance_percentages": [],
            "academic_percentages": [],
            "feedback_response_count": 0,
            "feedback_rating_sum": 0.0,
            "attendance_risk_students": set(),
        }
    )

    batch_data = defaultdict(
        lambda: {
            "batch_name": None,
            "total_classes": 0,
            "attended_classes": 0,
            "academic_percentages": []
        }
    )

    section_data = defaultdict(
        lambda: {
            "section_name": None,
            "total_classes": 0,
            "attended_classes": 0,
            "academic_percentages": []
        }
    )

    facilitator_data = defaultdict(
        lambda: {
            "instructor_id": None,
            "instructor_name": None,
            "response_count": 0,
            "feedback_rating_sum": 0.0
        }
    )

    raw_data = []

    # -----------------------------
    # 1. Process Attendance Records
    # -----------------------------
    for row in attendance_records:
        (
            student_id, usn, student_name, course_id, course_code, course_name,
            batch_name, section_name, total_classes, attended_classes, attendance_percentage
        ) = row

        students.add(student_id)
        courses.add(course_id)

        department["total_classes"] += total_classes or 0
        department["attended_classes"] += attended_classes or 0

        if attendance_percentage is not None:
            pct = float(attendance_percentage)
            attendance_percentages.append(pct)
            if pct < 75:
                attendance_risk_students.add(student_id)

        course = course_data[course_id]
        course["course_id"] = course_id
        course["course_code"] = course_code
        course["course_name"] = course_name
        course["students"].add(student_id)
        course["total_classes"] += total_classes or 0
        course["attended_classes"] += attended_classes or 0
        if attendance_percentage is not None:
            pct = float(attendance_percentage)
            course["attendance_percentages"].append(pct)
            if pct < 75:
                course["attendance_risk_students"].add(student_id)

        if batch_name:
            batch = batch_data[batch_name]
            batch["batch_name"] = batch_name
            batch["total_classes"] += total_classes or 0
            batch["attended_classes"] += attended_classes or 0

        if section_name:
            section = section_data[section_name]
            section["section_name"] = section_name
            section["total_classes"] += total_classes or 0
            section["attended_classes"] += attended_classes or 0

        raw_data.append({
            "data_type": "Attendance",
            "student_id": student_id,
            "usn": usn,
            "student_name": student_name,
            "course_id": course_id,
            "course_code": course_code,
            "course_name": course_name,
            "batch_name": batch_name,
            "section_name": section_name,
            "metric_1_name": "Total Classes",
            "metric_1_value": total_classes,
            "metric_2_name": "Attended Classes",
            "metric_2_value": attended_classes,
            "metric_3_name": "Attendance %",
            "metric_3_value": float(attendance_percentage) if attendance_percentage is not None else None,
            "instructor_name": None,
            "module_name": None
        })

    # -----------------------------
    # 2. Process Academic Records
    # -----------------------------
    for row in academic_records:
        (
            student_id, usn, student_name, course_id, course_code, course_name,
            batch_name, section_name, assessment_count, academic_percentage
        ) = row

        students.add(student_id)
        courses.add(course_id)

        if academic_percentage is not None:
            pct = float(academic_percentage)
            academic_percentages.append(pct)

        course = course_data[course_id]
        if course["course_id"] is None:
            course["course_id"] = course_id
            course["course_code"] = course_code
            course["course_name"] = course_name

        course["students"].add(student_id)
        if academic_percentage is not None:
            course["academic_percentages"].append(float(academic_percentage))

        if batch_name and academic_percentage is not None:
            batch = batch_data[batch_name]
            batch["batch_name"] = batch_name
            batch["academic_percentages"].append(float(academic_percentage))

        if section_name and academic_percentage is not None:
            section = section_data[section_name]
            section["section_name"] = section_name
            section["academic_percentages"].append(float(academic_percentage))

        raw_data.append({
            "data_type": "Academic",
            "student_id": student_id,
            "usn": usn,
            "student_name": student_name,
            "course_id": course_id,
            "course_code": course_code,
            "course_name": course_name,
            "batch_name": batch_name,
            "section_name": section_name,
            "metric_1_name": "Assessment Count",
            "metric_1_value": assessment_count,
            "metric_2_name": "Academic %",
            "metric_2_value": float(academic_percentage) if academic_percentage is not None else None,
            "metric_3_name": None,
            "metric_3_value": None,
            "instructor_name": None,
            "module_name": None
        })

    # -----------------------------
    # 3. Process Feedback Records
    # -----------------------------
    feedback_list = []
    dept_feedback_responses = 0
    dept_feedback_sum = 0.0

    for row in feedback_records:
        (
            course_id, course_code, course_name,
            module_id, module_name,
            instructor_id, instructor_name,
            batch_name, section_name,
            response_count, average_feedback_rating
        ) = row

        courses.add(course_id)

        course = course_data[course_id]
        if course["course_id"] is None:
            course["course_id"] = course_id
            course["course_code"] = course_code
            course["course_name"] = course_name

        if response_count is not None and average_feedback_rating is not None:
            count = int(response_count)
            avg = float(average_feedback_rating)

            dept_feedback_responses += count
            dept_feedback_sum += avg * count

            course["feedback_response_count"] += count
            course["feedback_rating_sum"] += avg * count
            
            facilitator = facilitator_data[instructor_id]
            facilitator["instructor_id"] = instructor_id
            facilitator["instructor_name"] = instructor_name
            facilitator["response_count"] += count
            facilitator["feedback_rating_sum"] += avg * count

        feedback_list.append({
            "course_id": course_id,
            "course_code": course_code,
            "course_name": course_name,
            "module_id": module_id,
            "module_name": module_name,
            "instructor_id": instructor_id,
            "instructor_name": instructor_name,
            "response_count": response_count,
            "average_feedback_rating": average_feedback_rating
        })

        raw_data.append({
            "data_type": "Feedback",
            "student_id": None,
            "usn": None,
            "student_name": None,
            "course_id": course_id,
            "course_code": course_code,
            "course_name": course_name,
            "batch_name": batch_name,
            "section_name": section_name,
            "metric_1_name": "Response Count",
            "metric_1_value": response_count,
            "metric_2_name": "Average Rating",
            "metric_2_value": float(average_feedback_rating) if average_feedback_rating is not None else None,
            "metric_3_name": None,
            "metric_3_value": None,
            "instructor_name": instructor_name,
            "module_name": module_name
        })

    # -----------------------------
    # 4. Department Calculations
    # -----------------------------
    department["student_count"] = len(students)
    department["course_count"] = len(courses)

    if department["total_classes"] > 0:
        department["average_attendance_percentage"] = round(
            100.0 * department["attended_classes"] / department["total_classes"], 2
        )

    if academic_percentages:
        department["average_academic_percentage"] = round(
            sum(academic_percentages) / len(academic_percentages), 2
        )

    department["feedback_response_count"] = dept_feedback_responses
    if dept_feedback_responses > 0:
        department["average_feedback_rating"] = round(dept_feedback_sum / dept_feedback_responses, 2)
    else:
        department["average_feedback_rating"] = None

    department["attendance_risk_records"] = sum(1 for value in attendance_percentages if value < 75)
    department["students_with_attendance_risk"] = len(attendance_risk_students)

    # -----------------------------
    # 5. Course Calculations
    # -----------------------------
    courses_summary = []

    for course_id, course in sorted(course_data.items()):
        total_classes = course["total_classes"]
        attended_classes = course["attended_classes"]

        if total_classes > 0:
            avg_attendance = round(100.0 * attended_classes / total_classes, 2)
        else:
            avg_attendance = None

        if course["academic_percentages"]:
            avg_academic = round(
                sum(course["academic_percentages"]) / len(course["academic_percentages"]), 2
            )
        else:
            avg_academic = None

        if course["feedback_response_count"] > 0:
            avg_feedback = round(course["feedback_rating_sum"] / course["feedback_response_count"], 2)
        else:
            avg_feedback = None

        courses_summary.append({
            "course_id": course["course_id"],
            "course_code": course["course_code"],
            "course_name": course["course_name"],
            "student_count": len(course["students"]),
            "total_classes": total_classes,
            "attended_classes": attended_classes,
            "average_attendance_percentage": avg_attendance,
            "average_academic_percentage": avg_academic,
            "feedback_response_count": course["feedback_response_count"],
            "average_feedback_rating": avg_feedback,
            "attendance_risk_students": len(course["attendance_risk_students"])
        })
        
    # -----------------------------
    # 6. Batch Calculations
    # -----------------------------
    batches_summary = []
    for b_name, batch in sorted(batch_data.items()):
        total_classes = batch["total_classes"]
        attended_classes = batch["attended_classes"]

        avg_attendance = None
        if total_classes > 0:
            avg_attendance = round(100.0 * attended_classes / total_classes, 2)

        avg_academic = None
        if batch["academic_percentages"]:
            avg_academic = round(
                sum(batch["academic_percentages"]) / len(batch["academic_percentages"]), 2
            )
            
        attendance_concern = False
        if avg_attendance is not None and avg_attendance < 75:
            attendance_concern = True
            
        academic_concern = False
        if avg_academic is not None and avg_academic < 50:
            academic_concern = True

        batches_summary.append({
            "batch_name": batch["batch_name"],
            "total_classes": total_classes,
            "attended_classes": attended_classes,
            "average_attendance_percentage": avg_attendance,
            "average_academic_percentage": avg_academic,
            "attendance_concern": attendance_concern,
            "academic_concern": academic_concern
        })

    # -----------------------------
    # 7. Section Calculations
    # -----------------------------
    sections_summary = []
    for s_name, section in sorted(section_data.items()):
        total_classes = section["total_classes"]
        attended_classes = section["attended_classes"]

        avg_attendance = None
        if total_classes > 0:
            avg_attendance = round(100.0 * attended_classes / total_classes, 2)

        avg_academic = None
        if section["academic_percentages"]:
            avg_academic = round(
                sum(section["academic_percentages"]) / len(section["academic_percentages"]), 2
            )
            
        attendance_concern = False
        if avg_attendance is not None and avg_attendance < 75:
            attendance_concern = True
            
        academic_concern = False
        if avg_academic is not None and avg_academic < 50:
            academic_concern = True

        sections_summary.append({
            "section_name": section["section_name"],
            "total_classes": total_classes,
            "attended_classes": attended_classes,
            "average_attendance_percentage": avg_attendance,
            "average_academic_percentage": avg_academic,
            "attendance_concern": attendance_concern,
            "academic_concern": academic_concern
        })

    # -----------------------------
    # 8. Facilitator Calculations
    # -----------------------------
    facilitators_summary = []
    for i_id, fac in sorted(facilitator_data.items()):
        avg_feedback = None
        if fac["response_count"] > 0:
            avg_feedback = round(fac["feedback_rating_sum"] / fac["response_count"], 2)
            
        facilitators_summary.append({
            "instructor_id": fac["instructor_id"],
            "instructor_name": fac["instructor_name"],
            "response_count": fac["response_count"],
            "average_feedback_rating": avg_feedback
        })
        
    # Sort facilitators by average feedback rating (descending), then response count (descending)
    # None ratings are pushed to the bottom
    facilitators_summary.sort(
        key=lambda x: (x["average_feedback_rating"] or -1, x["response_count"]),
        reverse=True
    )

    return {
        "department": department,
        "courses": courses_summary,
        "batches": batches_summary,
        "sections": sections_summary,
        "facilitators": facilitators_summary,
        "feedback": feedback_list,
        "raw_data": raw_data
    }
