from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import timedelta

def get_weekly_feedback(department_id, week_start, week_end):
    hook = PostgresHook(postgres_conn_id="local_postgres")

    sql = """
        SELECT
            f.course_id,
            c.course_code,
            c.course_name,
            f.module_id,
            m.module_name,
            f.instructor_id,
            i.instructor_name,
            bat.batch_name,
            sec.section_name,
            COUNT(r.valid_rating) AS response_count,
            ROUND(AVG(r.valid_rating)::numeric, 2)
                AS average_feedback_rating
        FROM feedback_forms f
        JOIN feedback_ratings_normalized r
            ON f.feedback_form_id = r.feedback_form_id
        JOIN courses c
            ON f.course_id = c.course_id
        JOIN modules m
            ON f.module_id = m.module_id
        JOIN instructors i
            ON f.instructor_id = i.instructor_id
        JOIN sections sec
            ON f.section_id = sec.section_id
        JOIN branches b
            ON sec.branch_id = b.branch_id
        LEFT JOIN batches bat
            ON sec.batch_id = bat.batch_id
        WHERE b.department_id = %s
          AND f.feedback_date >= %s
          AND f.feedback_date < %s
          AND r.valid_rating IS NOT NULL
        GROUP BY
            f.course_id,
            c.course_code,
            c.course_name,
            f.module_id,
            m.module_name,
            f.instructor_id,
            i.instructor_name,
            bat.batch_name,
            sec.section_name
        ORDER BY
            f.course_id,
            f.module_id,
            f.instructor_id;
    """

    records = hook.get_records(
        sql,
        parameters=(department_id, week_start, week_end)
    )

    return records
