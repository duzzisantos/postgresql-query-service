from celery import Celery
from celery.schedules import crontab
import pandas as pd
from io import BytesIO
from models.emailing_model import SendQueryFileToEmail
from models.email_properties import EmailProperties


celery_app = Celery()
@celery_app.on_after_configure.connect
def set_up_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=0, day_of_week=1),
        send_weekly_query_report.s()
    )



@celery_app.task
async def send_weekly_query_report(model: EmailProperties, query_result):
    df = pd.DataFrame(query_result)
    stream = BytesIO()

    with pd.ExcelWriter(stream, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    stream.seek()

    import asyncio

    ## One may need to set email properties safely somewhere instead to have details readily available during schedule
    email = SendQueryFileToEmail(model.recipient, model.sender, model.password, model.role,
                                  model.subject, model.message, model.email_server, attachment=stream)

    asyncio.run(
     await email.send_to_recipients()
    )
