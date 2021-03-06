# covax-bot

### running manually
from within the top level directory
* start the beat scheduler `celery -A src.celery_app beat`
* start the workers `celery -A src.celery_app worker -l INFO`
* run once `celery call src.appointment_runner.run`

### run scheduled
`overmind start (-D)`

### within IDE
`python main.py`
