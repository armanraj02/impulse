from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

# Colors
PRIMARY = colors.HexColor("#0A2540")       # Deep Navy
SECONDARY = colors.HexColor("#637A91")     # Blue-gray
HEALTHY = colors.HexColor("#008A00")       # Green
WARNING = colors.HexColor("#FF8C00")       # Amber/Orange
CRITICAL = colors.HexColor("#D32F2F")      # Red
BG_LIGHT = colors.HexColor("#F4F6F8")      # Light Gray
BG_WHITE = colors.HexColor("#FFFFFF")

def _get_status_color(status_text):
    text = status_text.lower()
    if "healthy" in text or "pass" in text:
        return HEALTHY
    if "monitor" in text or "attention" in text or "risk" in text or "concern" in text or "fail" in text or "low" in text:
        if "critical" in text or "action required" in text or "high priority" in text:
            return CRITICAL
        return WARNING
    return SECONDARY

def create_weekly_pdf_report(
    department,
    week_start,
    week_end,
    summary,
    insights,
    output_dir="/opt/airflow/reports",
):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    department_code = department["department_code"]
    department_name = department["department_name"]
    filename = f"{department_code}_Weekly_Report_{week_start}_to_{week_end}.pdf"
    filepath = output_path / filename

    document = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        textColor=PRIMARY,
        fontName="Helvetica-Bold",
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=12,
        textColor=SECONDARY,
        spaceAfter=4,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=PRIMARY,
        fontName="Helvetica-Bold",
        spaceBefore=15,
        spaceAfter=10,
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.black,
    )

    bold_style = ParagraphStyle(
        "BoldCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        fontName="Helvetica-Bold",
        textColor=colors.black,
    )

    story = []

    # 1. REPORT HEADER
    story.append(Paragraph("InPulse Academic Intelligence Platform", title_style))
    story.append(Paragraph("Weekly HOD Report", subtitle_style))
    story.append(Paragraph(f"Department: {department_name} ({department_code})", subtitle_style))
    story.append(Paragraph(f"Reporting Period: {week_start} through {week_end}", subtitle_style))
    story.append(Paragraph(f"Generation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
    story.append(Spacer(1, 15))

    # Calculate Overall Status
    dept = summary["department"]
    att_pct = dept["average_attendance_percentage"]
    acad_pct = dept["average_academic_percentage"]
    
    overall_status = "Healthy"
    priority_issues = []
    
    if dept["students_with_attendance_risk"] > 0:
        priority_issues.append(f"{dept['students_with_attendance_risk']} students with high attendance risk (<75%).")
        
    risk_batches = [b for b in summary.get("batches", []) if b["attendance_concern"] or b["academic_concern"]]
    if risk_batches:
        priority_issues.append(f"{len(risk_batches)} batches flagged for academic or attendance concerns.")
        
    risk_courses = [c for c in summary.get("courses", []) if c["average_academic_percentage"] is not None and c["average_academic_percentage"] < 50]
    if risk_courses:
        priority_issues.append(f"{len(risk_courses)} courses showing low academic performance (<50%).")

    if len(priority_issues) >= 3 or (att_pct is not None and att_pct < 75):
        overall_status = "Attention Required"
    elif len(priority_issues) > 0:
        overall_status = "Monitor"

    # 2. EXECUTIVE SUMMARY & DEPARTMENT STATUS
    story.append(Paragraph("Executive Summary & Department Status", section_style))
    
    summary_data = [
        ["Metric", "Value", "Metric", "Value"],
        ["Total Students", dept["student_count"], "Average Attendance", f"{att_pct}%" if att_pct is not None else "N/A"],
        ["Total Courses", dept["course_count"], "Average Academic", f"{acad_pct}%" if acad_pct is not None else "N/A"],
        ["Batches", len(summary.get("batches", [])), "Average Feedback Rating", f"{dept['average_feedback_rating']} / 5" if dept["average_feedback_rating"] is not None else "N/A"],
        ["Sections", len(summary.get("sections", [])), "Feedback Responses", dept["feedback_response_count"]],
        ["Facilitators", len(summary.get("facilitators", [])), "Attendance Risk Students", dept["students_with_attendance_risk"]],
    ]
    
    table = Table(summary_data, colWidths=[45 * mm, 30 * mm, 50 * mm, 30 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("ALIGN", (3, 0), (3, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))
    
    # Status
    status_color = _get_status_color(overall_status)
    status_para = ParagraphStyle("StatusPara", parent=normal_style, textColor=status_color, fontName="Helvetica-Bold", fontSize=12)
    story.append(Paragraph(f"Overall Department Status: {overall_status}", status_para))
    story.append(Spacer(1, 15))

    # 3. PRIORITY ISSUES
    story.append(Paragraph("Priority Issues", section_style))
    if not priority_issues:
        story.append(Paragraph("No immediate priority issues detected.", normal_style))
    else:
        for i, issue in enumerate(priority_issues, 1):
            story.append(Paragraph(f"• {issue}", normal_style))
            story.append(Spacer(1, 3))
            
    story.append(PageBreak())

    # 4. COURSE PERFORMANCE
    story.append(Paragraph("Course Performance", section_style))
    course_data = [["Course", "Att %", "Acad %", "Feedback", "Resp", "Risk Stdnts"]]
    for course in summary["courses"]:
        academic = course["average_academic_percentage"]
        att = course["average_attendance_percentage"]
        fb = course["average_feedback_rating"]
        course_data.append([
            (course["course_name"][:25] + '..') if len(course["course_name"]) > 25 else course["course_name"],
            f"{att}%" if att is not None else "N/A",
            f"{academic}%" if academic is not None else "N/A",
            f"{fb} / 5" if fb is not None else "N/A",
            course["feedback_response_count"],
            course["attendance_risk_students"],
        ])
    if len(course_data) > 1:
        course_table = Table(course_data, colWidths=[65 * mm, 18 * mm, 18 * mm, 20 * mm, 15 * mm, 25 * mm], repeatRows=1)
        course_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, SECONDARY),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(course_table)
    else:
        story.append(Paragraph("No course data available.", normal_style))

    story.append(Spacer(1, 15))

    # 5. BATCH / SECTION CONCERNS
    story.append(Paragraph("Batch / Section Concerns", section_style))
    risk_entities = []
    for b in summary.get("batches", []):
        if b["attendance_concern"] or b["academic_concern"]:
            c_type = []
            if b["attendance_concern"]: c_type.append("Attendance")
            if b["academic_concern"]: c_type.append("Academic")
            risk_entities.append([f"Batch: {b['batch_name']}", f"{b['average_attendance_percentage']}%" if b['average_attendance_percentage'] is not None else "N/A", f"{b['average_academic_percentage']}%" if b['average_academic_percentage'] is not None else "N/A", ", ".join(c_type)])
            
    for s in summary.get("sections", []):
        if s["attendance_concern"] or s["academic_concern"]:
            c_type = []
            if s["attendance_concern"]: c_type.append("Attendance")
            if s["academic_concern"]: c_type.append("Academic")
            risk_entities.append([f"Section: {s['section_name']}", f"{s['average_attendance_percentage']}%" if s['average_attendance_percentage'] is not None else "N/A", f"{s['average_academic_percentage']}%" if s['average_academic_percentage'] is not None else "N/A", ", ".join(c_type)])

    if not risk_entities:
        story.append(Paragraph("No batches or sections flagged for concern.", normal_style))
    else:
        batch_data = [["Entity", "Attendance %", "Academic %", "Concern Type"]] + risk_entities
        batch_table = Table(batch_data, colWidths=[65 * mm, 30 * mm, 30 * mm, 40 * mm], repeatRows=1)
        batch_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, SECONDARY),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))
        story.append(batch_table)

    story.append(PageBreak())

    # 6. ATTENDANCE RISK
    story.append(Paragraph("Attendance Risk (< 75%)", section_style))
    raw_data = summary.get("raw_data", [])
    att_risks = [r for r in raw_data if r["data_type"] == "Attendance" and r["metric_3_value"] is not None and float(r["metric_3_value"]) < 75]
    if not att_risks:
        story.append(Paragraph("No students flagged for attendance risk.", normal_style))
    else:
        att_data = [["Student", "Course", "Batch", "Section", "Att %"]]
        for r in att_risks[:50]: # limit to 50 for PDF
            att_data.append([
                (r["student_name"][:20] + '..') if r["student_name"] and len(r["student_name"]) > 20 else (r["student_name"] or "Unknown"),
                r["course_code"],
                r["batch_name"] or "-",
                r["section_name"] or "-",
                f"{r['metric_3_value']}%"
            ])
        att_table = Table(att_data, colWidths=[45 * mm, 30 * mm, 30 * mm, 30 * mm, 25 * mm], repeatRows=1)
        att_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, SECONDARY),
            ("ALIGN", (4, 1), (4, -1), "CENTER"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TEXTCOLOR", (4, 1), (4, -1), CRITICAL),
        ]))
        story.append(att_table)
        if len(att_risks) > 50:
            story.append(Paragraph(f"... and {len(att_risks) - 50} more records (see Excel for full list).", normal_style))

    story.append(Spacer(1, 15))

    # 7. ACADEMIC CONCERNS
    story.append(Paragraph("Academic Concerns (< 50%)", section_style))
    acad_risks = [r for r in raw_data if r["data_type"] == "Academic" and r["metric_2_value"] is not None and float(r["metric_2_value"]) < 50]
    if not acad_risks:
        story.append(Paragraph("No students flagged for academic concern.", normal_style))
    else:
        acad_data = [["Student", "Course", "Batch", "Section", "Acad %"]]
        for r in acad_risks[:50]:
            acad_data.append([
                (r["student_name"][:20] + '..') if r["student_name"] and len(r["student_name"]) > 20 else (r["student_name"] or "Unknown"),
                r["course_code"],
                r["batch_name"] or "-",
                r["section_name"] or "-",
                f"{r['metric_2_value']}%"
            ])
        acad_table = Table(acad_data, colWidths=[45 * mm, 30 * mm, 30 * mm, 30 * mm, 25 * mm], repeatRows=1)
        acad_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, SECONDARY),
            ("ALIGN", (4, 1), (4, -1), "CENTER"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TEXTCOLOR", (4, 1), (4, -1), WARNING),
        ]))
        story.append(acad_table)
        if len(acad_risks) > 50:
            story.append(Paragraph(f"... and {len(acad_risks) - 50} more records (see Excel for full list).", normal_style))

    story.append(PageBreak())

    # 8. FEEDBACK
    story.append(Paragraph("Feedback Analysis", section_style))
    feedback = summary.get("feedback", [])
    if not feedback:
        story.append(Paragraph("No feedback data available.", normal_style))
    else:
        fb_data = [["Course", "Module", "Instructor", "Responses", "Rating"]]
        for fb in feedback:
            fb_data.append([
                fb["course_code"],
                (fb["module_name"][:25] + '..') if fb["module_name"] and len(fb["module_name"]) > 25 else (fb["module_name"] or "-"),
                (fb["instructor_name"][:20] + '..') if fb["instructor_name"] and len(fb["instructor_name"]) > 20 else (fb["instructor_name"] or "-"),
                fb["response_count"],
                f"{fb['average_feedback_rating']} / 5" if fb['average_feedback_rating'] is not None else "N/A"
            ])
        fb_table = Table(fb_data, colWidths=[25 * mm, 50 * mm, 45 * mm, 20 * mm, 20 * mm], repeatRows=1)
        fb_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, SECONDARY),
            ("ALIGN", (3, 1), (-1, -1), "CENTER"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ]))
        story.append(fb_table)

    story.append(Spacer(1, 15))

    # 9. HOD ACTIONS
    story.append(Paragraph("HOD Actions & Recommendations", section_style))
    recs = insights.get("recommendations", [])
    if not recs:
        story.append(Paragraph("No specific actions recommended at this time.", normal_style))
    else:
        for i, rec in enumerate(recs, 1):
            story.append(Paragraph(f"• {rec}", normal_style))
            story.append(Spacer(1, 4))
            
    # 10. FINAL STATUS
    story.append(Spacer(1, 20))
    story.append(Paragraph("Final Department Status", section_style))
    story.append(Paragraph(f"Overall Status: {overall_status}", status_para))

    document.build(story)
    return str(filepath)
