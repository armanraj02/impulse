import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import json

db_host = os.getenv("DB_HOST", "host.docker.internal")
db_user = os.getenv("POSTGRES_USER", os.getenv("DB_USER", "postgres"))
db_password = os.getenv("POSTGRES_PASSWORD", os.getenv("DB_PASSWORD", "postgres"))
readonly_password = os.getenv("ANALYTICS_DB_PASSWORD", "readonly123")

try:
    # Connect to the default database to create the role if it doesn't exist
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password, dbname='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_roles WHERE rolname='analytics_readonly'")
    exists = cur.fetchone()
    if not exists:
        print("Creating role analytics_readonly...")
        cur.execute(f"CREATE ROLE analytics_readonly WITH LOGIN PASSWORD '{readonly_password}'")
    else:
        print("Role analytics_readonly already exists, resetting password...")
        cur.execute(f"ALTER ROLE analytics_readonly WITH PASSWORD '{readonly_password}'")
    
    cur.close()
    conn.close()

    # Now connect to academic_analytics_db and grant permissions
    conn_db = psycopg2.connect(host=db_host, user=db_user, password=db_password, dbname='academic_analytics_db')
    conn_db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur_db = conn_db.cursor()

    print("Granting CONNECT on academic_analytics_db to analytics_readonly...")
    cur_db.execute("GRANT CONNECT ON DATABASE academic_analytics_db TO analytics_readonly")
    
    print("Granting USAGE on schema public...")
    cur_db.execute("GRANT USAGE ON SCHEMA public TO analytics_readonly")
    
    print("Granting SELECT on all tables in public...")
    cur_db.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_readonly")
    
    print("Altering default privileges...")
    cur_db.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO analytics_readonly")

    # Fetch schema of relevant tables to output as JSON
    tables_to_inspect = [
        'department_performance_summary',
        'student_performance_summary',
        'course_performance_summary',
        'section_performance_summary',
        'batch_performance_summary',
        'feedback_summary',
        'module_feedback_summary',
        'instructor_feedback_summary',
        'risk_summary',
        'insight_summary'
    ]

    schema_info = {}
    for table in tables_to_inspect:
        cur_db.execute(f"SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name='{table}'")
        columns = cur_db.fetchall()
        
        cur_db.execute(f"""
            SELECT a.attname
            FROM   pg_index i
            JOIN   pg_attribute a ON a.attrelid = i.indrelid
                                AND a.attnum = ANY(i.indkey)
            WHERE  i.indrelid = '{table}'::regclass
            AND    i.indisprimary;
        """)
        pks = [row[0] for row in cur_db.fetchall()]

        schema_info[table] = {
            'columns': [{'name': col[0], 'type': col[1], 'nullable': col[2] == 'YES'} for col in columns],
            'primary_keys': pks
        }
    
    print("SCHEMA_JSON_START")
    print(json.dumps(schema_info))
    print("SCHEMA_JSON_END")

    cur_db.close()
    conn_db.close()
    print("Success.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
