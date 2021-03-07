import os
import sys

from celery import Celery

sys.path.append(os.path.abspath('src'))

app = Celery('src',
             broker='amqp://localhost:5672',
             backend='redis://localhost:6379',
             include=['src.tasks'])

if __name__ == "__main__":
    app.start()
