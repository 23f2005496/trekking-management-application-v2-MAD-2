from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


def make_celery(app):

    celery = Celery(
        app.import_name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )

    celery.conf.update(app.config)

    celery.conf.beat_schedule = {

            "daily-reminder": {
                "task": "app.tasks.daily_reminder.send_daily_reminders",
                "schedule": crontab(hour=9, minute=0),
                },

            "monthly-report": {
                "task": "app.tasks.monthly_report.send_monthly_report",
                "schedule": crontab(
                    hour=9,
                    minute=0,
                    day_of_month=1),
                }
    }

    celery.conf.timezone = "Asia/Kolkata"

    class ContextTask(celery.Task):

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery