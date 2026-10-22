from dags.lib.weekly_academic import get_weekly_academic
from dags.lib.weekly_summary_v2 import build_weekly_summary_v2
from dags.lib.weekly_attendance import get_weekly_attendance
from dags.lib.weekly_feedback import get_weekly_feedback

department_id = 2
week_start = '2026-08-31'
week_end = '2026-09-06'
week_end_boundary = '2026-09-07'

attendance_data = get_weekly_attendance(department_id, week_start, week_end_boundary)
academic_data = get_weekly_academic(department_id, week_start, week_end_boundary)
feedback_data = get_weekly_feedback(department_id, week_start, week_end_boundary)

summary = build_weekly_summary_v2(attendance_data, academic_data, feedback_data)
raw_data = summary['raw_data']

# Audit for N/A or NULL
academic_records = [r for r in raw_data if r['data_type'] == 'Academic']
null_academic = [r for r in academic_records if r['metric_2_value'] is None]

print('Total AIML students in summary with academic records:', len(academic_records))
print('Students with N/A academic percentage:', len(null_academic))
if len(null_academic) > 0:
    print('Sample of students with N/A academic percentage:')
    for r in null_academic[:5]:
        print(f"ID: {r['student_id']}, USN: {r['usn']}, Name: {r['student_name']}, Assessment Count: {r['metric_1_value']}")
