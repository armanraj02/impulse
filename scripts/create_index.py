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
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_active_delivery ON report_deliveries (department_id, week_start, week_end) WHERE status IN ('SUCCESS', 'SENDING');")
print('Index created.')
