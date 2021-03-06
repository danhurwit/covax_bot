# covax-bot

### running
from within the top level directory
* start the beat scheduler `celery -A src.main beat`
* start the workers `celery -A src.main worker -l INFO`