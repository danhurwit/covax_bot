import os
import sys

from celery import Celery

sys.path.append(os.path.abspath('src'))

app = Celery('src',
             broker='amqp://localhost:5672',
             include=['src.tasks'])

if __name__ == "__main__":
    app.start()
