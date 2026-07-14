from app import create_app

app = create_app()

celery = app.celery

# Import all Celery tasks so they get registered
import app.tasks.export_csv
import app.tasks.daily_reminder
import app.tasks.monthly_report