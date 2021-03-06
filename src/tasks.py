import vax_runner
from .celery_app import app


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls run() every 60 seconds
    sender.add_periodic_task(60.0, scrape_appointments.s(), expires=10)


@app.task
def scrape_appointments():
    vax_runner.run()

