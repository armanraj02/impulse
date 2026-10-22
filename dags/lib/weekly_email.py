from pathlib import Path
import smtplib
from email.message import EmailMessage
from datetime import datetime

from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook


def send_weekly_email(
    department,
    week_start,
    week_end,
    pdf_path,
    excel_path,
    smtp_conn_id="smtp_reporting",
    pg_conn_id="local_postgres",
    test_recipient_override=None
):
    """
    Send weekly academic intelligence report with duplicate protection.
    """

    # -----------------------------------------
    # 1. Validate department / recipient
    # -----------------------------------------
    department_id = department.get("department_id")
    if not department_id:
        raise ValueError("Department ID is required")

    recipient = test_recipient_override if test_recipient_override else department.get("hod_email")
    if not recipient:
        raise ValueError("Recipient email is empty")

    # -----------------------------------------
    # 3 & 4. Atomic Concurrency-Safe Check & Insert
    # -----------------------------------------
    pg_hook = PostgresHook(postgres_conn_id=pg_conn_id)
    
    pdf_file = Path(pdf_path)
    excel_file = Path(excel_path)
    
    insert_sql = """
        INSERT INTO report_deliveries (
            department_id, week_start, week_end, recipient_email,
            pdf_path, excel_path, status, attempted_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, 'SENDING', %s
        ) 
        ON CONFLICT (department_id, week_start, week_end) WHERE status IN ('SUCCESS', 'SENDING')
        DO NOTHING
        RETURNING delivery_id
    """
    attempted_at = datetime.now()
    record = pg_hook.get_first(
        insert_sql, 
        parameters=(department_id, week_start, week_end, recipient, str(pdf_file), str(excel_file), attempted_at)
    )

    if not record:
        check_sql = """
            SELECT status FROM report_deliveries
            WHERE department_id = %s AND week_start = %s AND week_end = %s
            AND status IN ('SUCCESS', 'SENDING')
        """
        existing_records = pg_hook.get_records(check_sql, parameters=(department_id, week_start, week_end))
        for row in existing_records:
            status = row[0]
            if status == "SUCCESS":
                return {
                    "recipient": recipient,
                    "status": "already_sent",
                    "pdf": str(pdf_file),
                    "excel": str(excel_file),
                    "message": "Delivery skipped: SUCCESS record already exists."
                }
            elif status == "SENDING":
                return {
                    "recipient": recipient,
                    "status": "delivery_in_progress",
                    "pdf": str(pdf_file),
                    "excel": str(excel_file),
                    "message": "Delivery skipped: SENDING record already exists."
                }
        raise RuntimeError("Failed to insert SENDING record, but no conflicting record was found.")

    delivery_id = record[0]

    try:
        # -----------------------------------------
        # 2. Validate files
        # -----------------------------------------
        if not pdf_file.exists() or pdf_file.stat().st_size == 0:
            raise ValueError(f"PDF report is missing or empty: {pdf_path}")

        if not excel_file.exists() or excel_file.stat().st_size == 0:
            raise ValueError(f"Excel report is missing or empty: {excel_path}")

        # -----------------------------------------
        # 5. SMTP connection & Send
        # -----------------------------------------
        import os
        smtp_host = os.environ.get("SMTP_HOST")
        smtp_port = int(os.environ.get("SMTP_PORT", 587))
        smtp_username = os.environ.get("SMTP_USERNAME")
        smtp_password = os.environ.get("SMTP_PASSWORD")
        smtp_from = os.environ.get("SMTP_FROM", smtp_username)

        if not all([smtp_host, smtp_username, smtp_password]):
            raise ValueError("SMTP configuration is incomplete")

        message = EmailMessage()
        message["Subject"] = (
            f"Weekly Academic Intelligence Report - "
            f"{department['department_code']} - "
            f"{week_start} to {week_end}"
        )
        message["From"] = smtp_from
        message["To"] = recipient

        message.set_content(
            f"""Dear {department['hod_name']},

Please find attached the Weekly Academic Intelligence Report
for {department['department_name']}.

Reporting Period:
{week_start} to {week_end}

The email contains:
1. Weekly PDF report
2. Detailed Excel report

Please review the identified attendance risks and
recommended improvement actions.

Regards,
Academic Intelligence System
"""
        )

        with open(pdf_file, "rb") as file:
            message.add_attachment(
                file.read(),
                maintype="application",
                subtype="pdf",
                filename=pdf_file.name,
            )

        with open(excel_file, "rb") as file:
            message.add_attachment(
                file.read(),
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=excel_file.name,
            )

        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(message)

        # -----------------------------------------
        # 6. Mark SUCCESS
        # -----------------------------------------
        update_sql = """
            UPDATE report_deliveries 
            SET status = 'SUCCESS', delivered_at = %s
            WHERE delivery_id = %s
        """
        pg_hook.run(update_sql, parameters=(datetime.now(), delivery_id))

        return {
            "recipient": recipient,
            "status": "sent",
            "pdf": str(pdf_file),
            "excel": str(excel_file),
        }

    except Exception as e:
        # -----------------------------------------
        # 7. Mark FAILED
        # -----------------------------------------
        error_message = str(e)[:1000] # Truncate to avoid extremely long errors
        update_fail_sql = """
            UPDATE report_deliveries 
            SET status = 'FAILED', error_message = %s
            WHERE delivery_id = %s
        """
        # Using a new connection/hook just in case the transaction is aborted
        pg_hook.run(update_fail_sql, parameters=(error_message, delivery_id))
        raise
