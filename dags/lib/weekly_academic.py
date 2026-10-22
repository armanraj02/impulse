from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import timedelta

def get_weekly_academic(department_id, week_start, week_end):
    hook = PostgresHook(postgres_conn_id="local_postgres")

    sql = """
        SELECT
            s_scores.student_id,
            s.usn,
            s.student_name,
            assess.course_id,
            c.course_code,
            c.course_name,
            bat.batch_name,
            ed.section_name,
            COUNT(*) AS assessment_count,
            ROUND(AVG((s_scores.marks_obtained::numeric / assess.max_marks::numeric) * 100)::numeric, 2) AS academic_percentage
        FROM assessment_scores s_scores
        JOIN assessments assess
            ON s_scores.assessment_id = assess.assessment_id
        JOIN students s
            ON s_scores.student_id = s.student_id
        JOIN courses c
            ON assess.course_id = c.course_id
        JOIN branches b
            ON s.branch_id = b.branch_id
        LEFT JOIN batches bat
            ON s.batch_id = bat.batch_id
        LEFT JOIN enrollment_details ed
            ON s_scores.student_id = ed.student_id AND assess.course_id = ed.course_id
        WHERE b.department_id = %s
          AND assess.assessment_date >= %s
          AND assess.assessment_date < %s
        GROUP BY
            s_scores.student_id,
            s.usn,
            s.student_name,
            assess.course_id,
            c.course_code,
            c.course_name,
            bat.batch_name,
            ed.section_name
        ORDER BY
            s_scores.student_id,
            assess.course_id;
    """

    records = hook.get_records(
        sql,
        parameters=(department_id, week_start, week_end)
    )

    return records
