from datetime import datetime, timedelta
import pendulum
import os
import json
from pathlib import Path
import logging

from airflow.decorators import dag, task, task_group
from airflow.models.baseoperator import chain
from airflow.utils.trigger_rule import TriggerRule

logger = logging.getLogger(__name__)

TEMP_DIR_BASE = Path("/opt/airflow/logs/temp_data")

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        from decimal import Decimal
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

@dag(
    dag_id="generalized_weekly_hod_pipeline",
    start_date=pendulum.datetime(2026, 8, 20, tz="Asia/Kolkata"),
    schedule="0 8 * * 6",
    catchup=False,
    tags=["academic", "weekly", "hod", "v2-test"],
    render_template_as_native_obj=True
)
def weekly_hod_pipeline_v2():
    
    @task
    def determine_period(logical_date: pendulum.DateTime = None, data_interval_start: pendulum.DateTime = None, run_id: str = None, dag=None):
        from lib.weekly_period import get_previous_completed_week
        report_date = logical_date or data_interval_start or pendulum.now('UTC')
        run_identifier = run_id or f"manual_{report_date.isoformat()}"
        dag_id = dag.dag_id if dag else "generalized_weekly_hod_pipeline_v2_test"
        
        week_start, week_end = get_previous_completed_week(report_date)
        week_start_str = week_start.strftime("%Y-%m-%d")
        week_end_str = week_end.strftime("%Y-%m-%d")
        
        # Create temp dir for this run
        run_temp_dir = TEMP_DIR_BASE / run_identifier
        run_temp_dir.mkdir(parents=True, exist_ok=True)
        
        from lib.pipeline_monitoring import insert_pipeline_run
        run_db_id = insert_pipeline_run(
            dag_id=dag_id,
            logical_date=report_date,
            week_start=week_start,
            week_end=week_end,
            run_identifier=run_identifier
        )
        
        return {
            "week_start_str": week_start_str,
            "week_end_str": week_end_str,
            "run_db_id": run_db_id,
            "run_identifier": run_identifier
        }

    @task
    def discover_departments(period_info: dict, dag_run=None):
        from lib.weekly_department import get_all_departments
        try:
            departments = get_all_departments()
            # Support single-department test injection
            if dag_run and dag_run.conf and dag_run.conf.get('target_department'):
                target = dag_run.conf.get('target_department')
                departments = [d for d in departments if d['department_code'] == target]
        except Exception as e:
            from lib.pipeline_monitoring import update_pipeline_run
            from lib.exceptions import DepartmentLookupError
            update_pipeline_run(period_info["run_db_id"], 0, 0, 0, "FAILED", f"DEPARTMENT_LOOKUP_FAILURE: {str(e)}")
            raise DepartmentLookupError(f"DEPARTMENT_LOOKUP_FAILURE: {e}") from e
        
        return departments

    @task_group(group_id="process_department")
    def process_department_group(department: dict, period_info: dict):
        
        # Helper function to generate stable path
        def get_artifact_path(dept_code, artifact_name, period_dict):
            dir_path = TEMP_DIR_BASE / period_dict["run_identifier"] / dept_code
            dir_path.mkdir(parents=True, exist_ok=True)
            return str(dir_path / f"{artifact_name}.json")
            
        @task
        def extract_attendance(dept: dict, period: dict):
            department_id = dept["department_id"]
            week_start_str = period["week_start_str"]
            week_end_date = datetime.strptime(period["week_end_str"], "%Y-%m-%d").date()
            week_end_exclusive = (week_end_date + timedelta(days=1)).strftime("%Y-%m-%d")
            
            from lib.weekly_attendance import get_weekly_attendance
            records = get_weekly_attendance(department_id, week_start_str, week_end_exclusive)
            path = get_artifact_path(dept["department_code"], "attendance", period)
            with open(path, 'w') as f:
                json.dump(records, f, cls=DecimalEncoder)
            return path
            
        @task
        def extract_academic(dept: dict, period: dict):
            department_id = dept["department_id"]
            week_start_str = period["week_start_str"]
            week_end_date = datetime.strptime(period["week_end_str"], "%Y-%m-%d").date()
            week_end_exclusive = (week_end_date + timedelta(days=1)).strftime("%Y-%m-%d")
            
            from lib.weekly_academic import get_weekly_academic
            records = get_weekly_academic(department_id, week_start_str, week_end_exclusive)
            path = get_artifact_path(dept["department_code"], "academic", period)
            with open(path, 'w') as f:
                json.dump(records, f, cls=DecimalEncoder)
            return path
            
        @task
        def extract_feedback(dept: dict, period: dict):
            department_id = dept["department_id"]
            week_start_str = period["week_start_str"]
            week_end_date = datetime.strptime(period["week_end_str"], "%Y-%m-%d").date()
            week_end_exclusive = (week_end_date + timedelta(days=1)).strftime("%Y-%m-%d")
            
            from lib.weekly_feedback import get_weekly_feedback
            records = get_weekly_feedback(department_id, week_start_str, week_end_exclusive)
            path = get_artifact_path(dept["department_code"], "feedback", period)
            with open(path, 'w') as f:
                json.dump(records, f, cls=DecimalEncoder)
            return path
            
        @task
        def data_quality_validation(att_path: str, acad_path: str, feed_path: str):
            with open(att_path, 'r') as f: att = json.load(f)
            with open(acad_path, 'r') as f: acad = json.load(f)
            
            if len(att) == 0 and len(acad) == 0:
                from lib.exceptions import DataQualityError
                raise DataQualityError("0 attendance AND 0 academic records found.")
            return True
            
        @task
        def build_summary(dept: dict, period: dict, dq_passed: bool, att_path: str, acad_path: str, feed_path: str):
            with open(att_path, 'r') as f: att = json.load(f)
            with open(acad_path, 'r') as f: acad = json.load(f)
            with open(feed_path, 'r') as f: feed = json.load(f)
            
            from lib.weekly_summary_v2 import build_weekly_summary_v2
            summary = build_weekly_summary_v2(att, acad, feed)
            path = get_artifact_path(dept["department_code"], "summary", period)
            with open(path, 'w') as f:
                json.dump(summary, f, cls=DecimalEncoder)
            return path
            
        @task
        def generate_insights(dept: dict, period: dict, summary_path: str):
            with open(summary_path, 'r') as f: summary = json.load(f)
            from lib.weekly_insights import generate_weekly_insights
            insights = generate_weekly_insights(summary)
            path = get_artifact_path(dept["department_code"], "insights", period)
            with open(path, 'w') as f:
                json.dump(insights, f, cls=DecimalEncoder)
            return path

        @task_group(group_id="report_generation")
        def report_generation(dept: dict, period: dict, summary_path: str, insights_path: str):
            @task
            def generate_pdf(dept: dict, period: dict, summary_path: str, insights_path: str):
                with open(summary_path, 'r') as f: summary = json.load(f)
                with open(insights_path, 'r') as f: insights = json.load(f)
                
                from lib.weekly_pdf import create_weekly_pdf_report
                pdf_path = create_weekly_pdf_report(
                    department=dept,
                    week_start=period["week_start_str"],
                    week_end=period["week_end_str"],
                    summary=summary,
                    insights=insights
                )
                pdf_file = Path(pdf_path)
                if not pdf_file.exists() or pdf_file.stat().st_size == 0:
                    from lib.exceptions import ArtifactValidationError
                    raise ArtifactValidationError(f"PDF is missing or empty: {pdf_path}")
                return pdf_path

            @task
            def generate_excel(dept: dict, period: dict, summary_path: str, insights_path: str):
                with open(summary_path, 'r') as f: summary = json.load(f)
                with open(insights_path, 'r') as f: insights = json.load(f)
                
                from lib.weekly_excel import create_weekly_excel_report
                excel_path = create_weekly_excel_report(
                    department=dept,
                    week_start=period["week_start_str"],
                    week_end=period["week_end_str"],
                    summary=summary,
                    insights=insights
                )
                excel_file = Path(excel_path)
                if not excel_file.exists() or excel_file.stat().st_size == 0:
                    from lib.exceptions import ArtifactValidationError
                    raise ArtifactValidationError(f"Excel is missing or empty: {excel_path}")
                return excel_path

            pdf_path = generate_pdf(dept, period, summary_path, insights_path)
            excel_path = generate_excel(dept, period, summary_path, insights_path)
            return {"pdf_path": pdf_path, "excel_path": excel_path}
            
        @task
        def send_email(dept: dict, period: dict, paths: dict):
            pdf_path = paths["pdf_path"]
            excel_path = paths["excel_path"]
            
            from lib.weekly_email import send_weekly_email
            try:
                result = send_weekly_email(
                    department=dept,
                    week_start=period["week_start_str"],
                    week_end=period["week_end_str"],
                    pdf_path=pdf_path,
                    excel_path=excel_path,
                    test_recipient_override=os.environ.get("SMTP_TO")
                )
                return {"status": "SUCCESS", "department_code": dept["department_code"]}
            except Exception as delivery_err:
                from lib.exceptions import ReportGenerationError
                raise ReportGenerationError(f"Email delivery failed: {delivery_err}") from delivery_err

        # Internal dependencies
        att_path = extract_attendance(department, period_info)
        acad_path = extract_academic(department, period_info)
        feed_path = extract_feedback(department, period_info)
        
        dq_passed = data_quality_validation(att_path, acad_path, feed_path)
        
        summary_path = build_summary(department, period_info, dq_passed, att_path, acad_path, feed_path)
        
        insights_path = generate_insights(department, period_info, summary_path)
        
        paths = report_generation(department, period_info, summary_path, insights_path)
        
        email_result = send_email(department, period_info, paths)
        
        return email_result

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def finalize_pipeline(period_info: dict, email_results: list):
        import shutil
        
        # Cleanup temporary files
        run_temp_dir = TEMP_DIR_BASE / period_info["run_identifier"]
        if run_temp_dir.exists():
            try:
                shutil.rmtree(run_temp_dir)
                logger.info(f"Cleaned up temporary directory: {run_temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary directory {run_temp_dir}: {e}")
                
        # Determine status
        # If email_results are wrapped by XComArg, iterating over it during task execution returns the results
        total_departments = len(email_results)
        successful_departments = 0
        failed_departments = 0
        
        for res in email_results:
            if isinstance(res, dict) and res.get("status") == "SUCCESS":
                successful_departments += 1
            else:
                failed_departments += 1

        final_status = "SUCCESS"
        if failed_departments > 0:
            final_status = "PARTIAL_SUCCESS" if successful_departments > 0 else "FAILED"

        from lib.pipeline_monitoring import update_pipeline_run
        update_pipeline_run(
            run_id=period_info["run_db_id"],
            total_departments=total_departments,
            successful_departments=successful_departments,
            failed_departments=failed_departments,
            status=final_status,
            error_message=f"{failed_departments} departments failed." if failed_departments > 0 else None
        )
        
        if final_status == "FAILED":
            from lib.exceptions import UnexpectedError
            raise UnexpectedError("Pipeline failed for all departments.")
        
        return final_status

    # DAG Flow
    period_info = determine_period()
    departments = discover_departments(period_info)
    
    # Expand Process Department TaskGroup
    email_results = process_department_group.partial(period_info=period_info).expand(department=departments)
    
    finalize_pipeline(period_info, email_results)

weekly_hod_pipeline_v2()
