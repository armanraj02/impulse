from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging

logger = logging.getLogger(__name__)

def insert_pipeline_run(dag_id, logical_date, week_start, week_end, run_identifier):
    """Inserts a new pipeline run and returns the run_id."""
    hook = PostgresHook(postgres_conn_id="local_postgres")
    sql = """
        INSERT INTO pipeline_runs (
            run_identifier, dag_id, logical_date, week_start, week_end,
            start_time, status
        ) VALUES (
            %s, %s, %s, %s, %s, %s, 'RUNNING'
        ) RETURNING run_id
    """
    start_time = datetime.now()
    # Initially status can be anything valid, we will update it later.
    result = hook.get_first(sql, parameters=(
        run_identifier, dag_id, logical_date, week_start, week_end, start_time
    ))
    return result[0] if result else None

def update_pipeline_run(run_id, total_departments, successful_departments, failed_departments, status, error_message=None):
    """Updates the pipeline run record at completion."""
    hook = PostgresHook(postgres_conn_id="local_postgres")
    sql = """
        UPDATE pipeline_runs
        SET end_time = %s,
            duration_seconds = EXTRACT(EPOCH FROM (%s - start_time)),
            total_departments = %s,
            successful_departments = %s,
            failed_departments = %s,
            status = %s,
            error_message = %s
        WHERE run_id = %s
    """
    end_time = datetime.now()
    hook.run(sql, parameters=(
        end_time, end_time,
        total_departments, successful_departments, failed_departments,
        status, error_message, run_id
    ))
