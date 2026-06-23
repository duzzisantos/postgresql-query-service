from celery import Celery
from celery.schedules import crontab
import pandas as pd
from io import BytesIO
from app.core.config import settings

celery_app = Celery("database_query_interface", broker=settings.CELERY_BROKER_URL)

celery_app.conf.beat_schedule = {
    "weekly-query-report": {
        "task": "app.tasks.celery_app.send_query_report",
        "schedule": crontab(hour=8, minute=0, day_of_week=1),
    },
}
celery_app.conf.timezone = "UTC"


@celery_app.task(name="app.tasks.celery_app.send_query_report")
def send_query_report(
    query_result: list[dict],
    recipient: str | list[str],
    subject: str = "Scheduled Query Report",
    message: str = "Please find the attached query report.",
    sender: str = None,
    password: str = None,
    email_server: str = None,
    email_port: int = None,
    use_tls: bool = None,
):
    """
    Celery task — must be synchronous (Celery doesn't support async).
    Converts query results to an Excel file and emails it.
    SMTP settings fall back to env vars when omitted.
    """
    from app.models.emailing_model import SendQueryFileToEmail

    df = pd.DataFrame(query_result)
    stream = BytesIO()
    with pd.ExcelWriter(stream, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    stream.seek(0)  # rewind so the attachment reader starts from the beginning

    email = SendQueryFileToEmail(
        recipient=recipient,
        sender=sender or settings.SMTP_USER,
        password=password or settings.SMTP_PASSWORD,
        role=None,
        subject=subject,
        message=message,
        email_server=email_server,
        email_port=email_port,
        use_tls=use_tls,
        attachment=stream,
        attachment_filename="query_report.xlsx",
    )
    return email.send()
