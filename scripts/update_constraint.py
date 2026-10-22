import os
import psycopg

db_host = os.getenv("DB_HOST", "127.0.0.1")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "inpulse_db")
db_user = os.getenv("DB_USER", os.getenv("POSTGRES_USER", "postgres"))
db_password = os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD", "postgres"))

conn = psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}')
conn.autocommit = True
cur = conn.cursor()
cur.execute("ALTER TABLE pipeline_runs DROP CONSTRAINT IF EXISTS pipeline_runs_status_check;")
cur.execute("ALTER TABLE pipeline_runs ADD CONSTRAINT pipeline_runs_status_check CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED', 'PARTIAL_SUCCESS'));")
print('Constraint updated.')
