from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import timedelta

def get_weekly_attendance(
    department_id,
    week_start,
    week_end
):
    """
    Retrieve weekly student-course attendance
    for a specific department.
    """

    hook = PostgresHook(
        postgres_conn_id="local_postgres"
    )

    sql = """
        SELECT
            a.student_id,
            s.usn,
            s.student_name,
            a.course_id,
            c.course_code,
            c.course_name,
            bat.batch_name,
            sec.section_name,

            COUNT(*) AS total_classes,

            SUM(
                CASE
                    WHEN a.status = 'Present' THEN 1
                    ELSE 0
                END
            ) AS attended_classes,

            ROUND(
                100.0 *
                SUM(
                    CASE
                        WHEN a.status = 'Present' THEN 1
                        ELSE 0
                    END
                ) / NULLIF(COUNT(*), 0),
                2
            ) AS attendance_percentage

        FROM attendance a

        JOIN students s
            ON a.student_id = s.student_id

        JOIN courses c
            ON a.course_id = c.course_id

        JOIN branches b
            ON s.branch_id = b.branch_id

        LEFT JOIN batches bat
            ON s.batch_id = bat.batch_id

        LEFT JOIN sections sec
            ON a.section_id = sec.section_id

        WHERE b.department_id = %s

          AND a.attendance_date >= %s

          AND a.attendance_date < %s

        GROUP BY
            a.student_id,
            s.usn,
            s.student_name,
            a.course_id,
            c.course_code,
            c.course_name,
            bat.batch_name,
            sec.section_name

        ORDER BY
            a.student_id,
            a.course_id;
    """

    records = hook.get_records(
        sql,
        parameters=(
            department_id,
            week_start,
            week_end
        )
    )

    return records
