from airflow.providers.postgres.hooks.postgres import PostgresHook


def get_department(department_id):
    hook = PostgresHook(postgres_conn_id="local_postgres")

    sql = """
        SELECT
            department_id,
            department_code,
            department_name,
            hod_name,
            hod_email
        FROM departments
        WHERE department_id = %s;
    """

    records = hook.get_records(sql, parameters=(department_id,))

    if not records:
        raise ValueError(f"Department {department_id} not found")

    row = records[0]

    return {
        "department_id": row[0],
        "department_code": row[1],
        "department_name": row[2],
        "hod_name": row[3],
        "hod_email": row[4],
    }


def get_all_departments():
    hook = PostgresHook(postgres_conn_id="local_postgres")

    sql = """
        SELECT
            department_id,
            department_code,
            department_name,
            hod_name,
            hod_email
        FROM departments
        ORDER BY department_id;
    """

    records = hook.get_records(sql)

    departments = []

    for row in records:
        departments.append({
            "department_id": row[0],
            "department_code": row[1],
            "department_name": row[2],
            "hod_name": row[3],
            "hod_email": row[4],
        })

    if not departments:
        raise ValueError("No departments found")

    return departments
