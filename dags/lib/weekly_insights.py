def generate_weekly_insights(summary):
    department = summary["department"]
    courses = summary["courses"]

    insights = []
    recommendations = []

    # ------------------------------------
    # 1. ATTENDANCE INSIGHTS
    # ------------------------------------

    attendance_courses = [
        c for c in courses
        if c["average_attendance_percentage"] is not None
    ]

    if attendance_courses:
        lowest_attendance = min(
            attendance_courses,
            key=lambda x: x["average_attendance_percentage"]
        )

        highest_risk = max(
            attendance_courses,
            key=lambda x: x["attendance_risk_students"]
        )

        insights.append(
            f"{lowest_attendance['course_code']} - "
            f"{lowest_attendance['course_name']} has the lowest "
            f"weekly attendance at "
            f"{lowest_attendance['average_attendance_percentage']}%."
        )

        insights.append(
            f"{highest_risk['course_code']} - "
            f"{highest_risk['course_name']} has the highest number "
            f"of attendance-risk students at "
            f"{highest_risk['attendance_risk_students']}."
        )

        if department["average_attendance_percentage"] is not None:
            insights.append(
                f"Department weekly attendance is "
                f"{department['average_attendance_percentage']}%."
            )

    else:
        insights.append(
            "Weekly attendance data was unavailable."
        )

    # ------------------------------------
    # 2. ATTENDANCE RISK
    # ------------------------------------

    risk_courses = [
        c for c in courses
        if c["attendance_risk_students"] > 0
    ]

    if risk_courses:
        recommendations.append(
            "Prioritize attendance intervention for courses "
            "with the highest number of risk students."
        )

        recommendations.append(
            "Review students below the 75% attendance threshold "
            "and initiate appropriate academic follow-up."
        )

    # ------------------------------------
    # 3. ACADEMIC INSIGHTS
    # ------------------------------------

    academic_courses = [
        c for c in courses
        if c["average_academic_percentage"] is not None
    ]

    if academic_courses:
        lowest_academic = min(
            academic_courses,
            key=lambda x: x["average_academic_percentage"]
        )

        insights.append(
            f"{lowest_academic['course_code']} - "
            f"{lowest_academic['course_name']} has the lowest "
            f"weekly academic performance at "
            f"{lowest_academic['average_academic_percentage']}%."
        )

        academic_risk_courses = [
            c for c in academic_courses
            if c["average_academic_percentage"] < 50
        ]

        if academic_risk_courses:
            recommendations.append(
                "Review academic performance in courses below "
                "the 50% threshold and plan targeted support."
            )

    else:
        insights.append(
            "Weekly academic assessment data was unavailable "
            "for this reporting period."
        )

    # ------------------------------------
    # 4. FEEDBACK INSIGHTS
    # ------------------------------------

    feedback_courses = [
        c for c in courses
        if (
            c["average_feedback_rating"] is not None
            and c["feedback_response_count"] >= 10
        )
    ]

    if feedback_courses:
        lowest_feedback = min(
            feedback_courses,
            key=lambda x: x["average_feedback_rating"]
        )

        insights.append(
            f"{lowest_feedback['course_code']} - "
            f"{lowest_feedback['course_name']} has the lowest "
            f"feedback rating at "
            f"{lowest_feedback['average_feedback_rating']}/5."
        )

        feedback_risk_courses = [
            c for c in feedback_courses
            if c["average_feedback_rating"] < 3
        ]

        if feedback_risk_courses:
            recommendations.append(
                "Review courses with feedback ratings below "
                "3/5 and identify improvement actions."
            )

    else:
        insights.append(
            "Weekly feedback data was unavailable or did not "
            "meet the minimum response requirement."
        )

    # ------------------------------------
    # 5. OVERALL RECOMMENDATION
    # ------------------------------------

    if department["students_with_attendance_risk"] > 0:
        recommendations.append(
            f"Monitor the {department['students_with_attendance_risk']} "
            f"students identified with attendance risk."
        )

    return {
        "insights": insights,
        "recommendations": recommendations,
    }
