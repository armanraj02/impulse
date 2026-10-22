import os
import psycopg2
import sys

db_host = os.getenv("DB_HOST", "host.docker.internal")
db_user = os.getenv("POSTGRES_USER", os.getenv("DB_USER", "postgres"))
db_password = os.getenv("POSTGRES_PASSWORD", os.getenv("DB_PASSWORD", "postgres"))

try:
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password, dbname='academic_analytics_db')
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cur.fetchall()
    print("Tables in academic_analytics_db:")
    for table in tables:
        print(f"- {table[0]}")
        cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table[0]}'")
        columns = cur.fetchall()
        for col in columns:
            print(f"  * {col[0]} ({col[1]})")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
